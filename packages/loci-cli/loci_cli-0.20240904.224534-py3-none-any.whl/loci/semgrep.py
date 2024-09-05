from typing import List, Optional
import typer
from rich.console import Console
import os
import json
import loci_client
from rich.progress import track
from enum import Enum
import loci.utils as utils

app = typer.Typer()
console = Console()


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@app.command()
def semgrep(
    files: List[typer.FileText] = typer.Argument(
        ..., help="One or more Semgrep JSON files"
    ),
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
    min_severity: Severity = typer.Option(
        Severity.medium, help="Minimum severity level to upload"
    ),
    verbose: bool = typer.Option(
        False, help="Show detailed info about what results will be uploaded"
    ),
    dry_run: bool = typer.Option(False, help="Do not upload results to server"),
    force: bool = typer.Option(
        False, help="Force upload results to server even with errors"
    ),
):
    """
    Process and import Semgrep JSON scan results.
    """
    # First get project info.
    project_info = utils.get_project_info(project_dir)

    severity_count_map = {}
    severity_count_map["HIGH"] = 0
    severity_count_map["MEDIUM"] = 0
    severity_count_map["LOW"] = 0

    results_count_map = {}

    for semgrep_json_file in files:
        semgrep_json_file_name = semgrep_json_file.name
        if not dry_run:
            utils.print_info(f"Processing [bold]{semgrep_json_file_name}[/bold]...")
        else:
            utils.print_info(
                f"Processing [bold]{semgrep_json_file_name}[/bold]... (dry run)"
            )

        with semgrep_json_file as f:
            semgrep_results_str = f.read()
            try:
                semgrep_results = json.loads(semgrep_results_str)
            except json.JSONDecodeError:
                utils.print_fatal(f"Invalid JSON file {semgrep_json_file}.")

        try:
            version = semgrep_results["version"]
            if version != "1.67.0":
                utils.print_warning(
                    f"Semgrep JSON file version {version} is not officially supported. There may be some "
                    "errors in how this file is processed."
                )
            semgrep_results["interfile_languages_used"]
            semgrep_results["errors"]
            semgrep_results["paths"]
            semgrep_results["results"]

        except KeyError:
            utils.print_fatal(
                "Invalid Semgrep JSON file: some required key was not found."
            )

        if verbose:
            error_map = {}
            for error in semgrep_results["errors"]:
                if not error["message"] in error_map:
                    error_map[error["message"]] = []
                error_map[error["message"]].append(error["path"])

            for error in error_map:
                utils.print_error(f"{error}")
                for path in error_map[error]:
                    utils.print_error(f"    - {path}")

        for result_dict in track(
            semgrep_results["results"], description="Processing Semgrep results..."
        ):
            check_id = result_dict["check_id"]
            full_path = result_dict["path"]
            if "_src" in full_path:
                artifact_path = full_path.split("_src", 1)[1][1:]
            else:
                utils.print_warning(
                    f"Could not determine artifact path for [bold]{check_id}[/bold] in [bold]{full_path}[/bold]."
                )
                if not force:
                    utils.print_fatal(
                        "If the path is correct, re-run with the [bold]--force[/bold] option."
                    )
                else:
                    artifact_path = full_path

            description = result_dict["extra"]["message"]

            # Try to figure out severity.
            try:
                severity = result_dict["extra"]["metadata"]["impact"]
            except KeyError:
                severity_tmp = result_dict["extra"]["severity"]
                if severity_tmp == "INFO":
                    severity = "LOW"
                elif severity_tmp == "WARNING":
                    severity = "MEDIUM"
                elif severity_tmp == "ERROR":
                    severity = "HIGH"
                else:
                    utils.print_warning(
                        f"Unknown severity {severity_tmp} for {check_id} in {artifact_path}."
                    )
                    severity = "MEDIUM"

            try:
                line = result_dict["start"]["line"]
            except KeyError:
                try:
                    line = result_dict["end"]["line"]
                except KeyError:
                    utils.print_warning(
                        f"No line information found for {check_id} in {artifact_path}."
                    )
            try:
                references = result_dict["extra"]["metadata"]["references"]
            except KeyError:
                references = []

            if severity not in severity_count_map:
                severity_count_map[severity] = 0
            severity_count_map[severity] += 1

            if check_id not in results_count_map:
                results_count_map[check_id] = 0
            results_count_map[check_id] += 1

            if not dry_run:
                if severity == "LOW" and (
                    min_severity == Severity.medium or min_severity == Severity.high
                ):
                    # Don't upload it
                    if verbose:
                        utils.print_warning(
                            f"Skipping {check_id} in {artifact_path} with [bold]{severity}[/bold] severity."
                        )
                    continue
                if severity == "MEDIUM" and min_severity == Severity.high:
                    # Don't upload it
                    if verbose:
                        utils.print_warning(
                            f"Skipping {check_id} in {artifact_path} with [bold]{severity}[/bold] severity."
                        )
                    continue

                api_client = utils.get_api_client(project_info)
                with api_client:
                    api_instance = loci_client.DefaultApi(api_client)

                    # TODO Make sure we actually have a record of the source code file that we want to attach to
                    # this artifact.
                    # skip = 0
                    # limit = 100
                    # filter = artifact_path
                    # type = loci_client.ArtifactTypeEnum.SOURCE_CODE_FILE
                    #
                    # try:
                    #     api_response = api_instance.read_project_artifacts(
                    #         id, skip=skip, limit=limit, filter=filter, type=type
                    #     )
                    # except loci_client.ApiException as e:
                    #     utils.print_fatal(
                    #         f"Exception when calling DefaultApi->read_project_artifacts: {e}"
                    #     )

                    contents = f"**{check_id}**\n\n"
                    contents += f"{description}\n\n\n\n"
                    if len(references) > 0:
                        contents += "References:\n\n"
                        for reference in references:
                            contents += f"  * [{reference}]({reference})\n"

                    artifact_note_in = loci_client.ArtifactNoteIn(
                        artifact_descriptor=loci_client.ArtifactDescriptor(
                            artifact_path + ":" + str(line)
                        ),
                        type=loci_client.ArtifactNoteTypeEnum.COMMENT.value,
                        artifact_type=loci_client.ArtifactInType(
                            loci_client.ArtifactTypeEnum.SOURCE_CODE_LOCATION
                        ),
                        contents=contents,
                        artifact_priority=loci_client.ArtifactInPriority(severity),
                        submission_tool=loci_client.SubmissionTool("Semgrep"),
                    )
                    try:
                        api_instance.create_note(
                            id=project_info.project_id,
                            artifact_note_in=artifact_note_in,
                        )
                    except loci_client.ApiException as e:
                        utils.print_fatal(
                            f"Exception when calling DefaultApi->create_note: {e}"
                        )

    # Print summary
    utils.print_info("Results Summary:")
    for severity in severity_count_map:
        utils.print_info(f"    {severity}: {severity_count_map[severity]}")

    if verbose:
        utils.print_info("Results by check:")
        for check_id in results_count_map:
            utils.print_info(f"    {check_id}: {results_count_map[check_id]}")

    utils.print_success("Semgrep results processed successfully!")
