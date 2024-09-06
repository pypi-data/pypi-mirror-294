import loci_client.models
import typer
from typing import Optional
from pathlib import Path
import os
from rich.progress import track
import concurrent.futures

import loci_client
from loci_client.models.artifact_note_type_enum import ArtifactNoteTypeEnum
from loci import utils


def _sync_single_file(
    artifact: loci_client.models.ArtifactOut,
    src_code_dir: str,
    dry_run: bool,
    project_info: utils.ProjectConfig,
) -> None:
    api_client = utils.get_api_client(project_info)
    with api_client:

        api_instance = loci_client.DefaultApi(api_client)

        src_code_filename = artifact.descriptor

        # Get the latest hash of the file.
        for note_id in artifact.note_ids:
            note = api_instance.read_note(note_id)

            if note.type == ArtifactNoteTypeEnum.SNAPSHOT_TXT:
                # TODO here may be a bug here where we need to grab the latest version of the hash, if there are
                # multiples.
                short_hash = note.contents
                break

        if not short_hash:
            utils.print_warning(
                f"Could not find a hash for {src_code_filename}. This may cause issues with file versioning, if there "
                "are multiple versions of the same file."
            )

        # This is the ultimate location of the source code file.
        src_code_file_fq = src_code_dir / src_code_filename

        # See if the file already exists. If it does, compare the hashes to see if it's the right version.
        if src_code_file_fq.exists() and not src_code_file_fq.is_dir():
            if not short_hash:
                # We don't have a hash to compare to, so we'll just download the file.
                utils.print_warning(
                    f"Could not compare the hash of {src_code_filename} because the hash is missing. The latest "
                    "version of the file will be downloaded."
                )
            else:
                # Check if the file is the correct version.
                local_file_hash = utils.get_short_file_hash_by_file(src_code_file_fq)
                if local_file_hash == short_hash:
                    # This means we already have a good local copy of the file.
                    return
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
                return

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

        # "But you should have a dynamic thread pool size!" I hear you say. Yes, I should. But I don't want to deal with
        # multiple people pulling down 1000s of files at once, and maxing out the server DB connection pool again.
        # So I'm setting a hard limit of 16 threads.
        thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=16)

        futures_list = []

        for artifact in artifacts:
            future = thread_pool.submit(
                _sync_single_file,
                artifact=artifact,
                src_code_dir=src_code_dir,
                dry_run=dry_run,
                project_info=project_info,
            )
            futures_list.append(future)

        for future in track(
            futures_list,
            description="Syncing artifacts...",
        ):
            # This is actually terrible, but better than nothing. Technically we are waiting for the OLDEST future in
            # each iteration, not the first one that completes.
            future.result()

        thread_pool.shutdown(wait=True)

    utils.print_success("Sync complete.")
    utils.print_info(f"Downloaded {len(artifacts)} files.")
