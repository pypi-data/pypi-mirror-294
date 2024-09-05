import loci_client.models
import typer
from typing import Optional
from pathlib import Path
import os
from rich.progress import track


import loci_client
from loci_client.models.artifact_note_type_enum import ArtifactNoteTypeEnum
from loci import utils


def sync(
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
    dry_run: bool = typer.Option(
        False, help="Show detailed info about what files will be downloaded."
    ),
):
    """
    Sync the local code folder with all code from the Loci Notes server.
    """
    # First get project info.
    project_info = utils.get_project_info(project_dir)

    # Get a listing of all source code files in the project.
    api_client = utils.get_api_client(project_info)
    with api_client:
        api_instance = loci_client.DefaultApi(api_client)
        total_count = 1
        artifacts = []

        while len(artifacts) < total_count:
            id = project_info.project_id
            skip = len(artifacts)
            limit = 100
            type = loci_client.ArtifactTypeEnum.SOURCE_CODE_FILE
            sort = loci_client.ArtifactSortEnum.CREATED_AT
            order = loci_client.OrderByEnum.DESC

            try:
                # Read Project Artifacts
                api_response = api_instance.read_project_artifacts(
                    id,
                    skip=skip,
                    limit=limit,
                    type=type,
                    sort=sort,
                    order=order,
                )
                total_count = api_response.count

                for artifact in api_response.data:
                    artifacts.append(artifact)

            except loci_client.ApiException as e:
                utils.handle_exception(e)

        src_code_dir = Path(project_dir) / "_src"
        src_code_dir.mkdir(parents=True, exist_ok=True)

        for artifact in track(artifacts, description="Syncing artifacts..."):
            src_code_filename_with_hash = artifact.descriptor
            src_code_filename = src_code_filename_with_hash.split("#")[0]
            short_hash = src_code_filename_with_hash.split("#")[1]
            if not short_hash or len(short_hash) != 8:
                utils.print_warning(
                    f"The file {src_code_filename} was uploaded without an included hash. This "
                    "may cause some unexpected behavior, especially in cases where several versions"
                    " of the same file are included in the project."
                )

            # This is the ultimate location of the source code file.
            src_code_file_fq = src_code_dir / src_code_filename

            # See if the file already exists. If it does, compare the hashes to see if it's the right version.
            if src_code_file_fq.exists() and not src_code_file_fq.is_dir():
                # Check if the file is the correct version.
                local_file_hash = utils.get_short_file_hash_by_file(src_code_file_fq)
                if local_file_hash == short_hash:
                    # This means we already have a good local copy of the file.
                    continue
                else:
                    # This means we have the wrong version of the file.
                    # We'll need to download the correct version of the file.
                    utils.print_warning(
                        f"The file {src_code_filename} is already present, but the local version "
                        "of the file is incorrect. The latest version of the file will be downloaded"
                        ", and replace the local copy. In the future, multiple versions of the same "
                        "file will be maintained."
                    )

            # Download the file. It's stored as a note attached to the artifact as a SNAPSHOT_TXT.
            try:
                if dry_run:
                    utils.print_info(
                        f"The file [bold]{src_code_filename}[/bold] will be downloaded (dry run)"
                    )
                    continue

                artifact_obj = api_instance.read_artifact(artifact.id)

                for note_id in artifact_obj.note_ids:
                    note_info = api_instance.read_note(note_id)
                    if note_info.type == ArtifactNoteTypeEnum.SNAPSHOT_TXT:
                        os.makedirs(os.path.dirname(src_code_file_fq), exist_ok=True)
                        with open(src_code_file_fq, "w") as f:
                            f.write(note_info.contents)
                    # Ignore other note types for now

            except loci_client.ApiException as e:
                utils.handle_exception(e)
    # TODO Detect and possibly delete extra files in the local directory that are not in the project.
    utils.print_success("Sync complete.")
    utils.print_info(f"Downloaded {len(artifacts)} files.")
