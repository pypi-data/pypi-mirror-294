import typer
from typing import Optional, List
from pathlib import Path
import os
import tempfile
import zipfile
import mimetypes
from rich.progress import track
import shutil
import chardet

import loci_client
from loci_client.models import (
    ArtifactDescriptor,
    ArtifactInPriority,
    ArtifactInStatus,
    ArtifactInType,
    ArtifactNoteIn,
    ArtifactNoteTypeEnum,
    ArtifactStatusEnum,
    ArtifactPriorityEnum,
    ArtifactTypeEnum,
    SubmissionTool,
)

from loci import utils


def upload(
    zipfiles: List[Path] = typer.Argument(
        ..., help="One or more zip files containing source code to upload."
    ),
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
    dry_run: bool = typer.Option(
        False, help="Show detailed info about what files will be uploaded."
    ),
):
    """
    Upload a zip file full of source code to the Loci Notes server.
    """
    # First get project info.
    project_info = utils.get_project_info(project_dir)

    # Check and make sure each file passed is a zip file.
    for src_code_zipfile in zipfiles:
        if not src_code_zipfile.is_file():
            utils.print_fatal(f"File [bold]{src_code_zipfile}[/bold] does not exist.")
        if src_code_zipfile.suffix != ".zip":
            utils.print_fatal(
                f"File [bold]{src_code_zipfile}[/bold] is not a zip file."
            )

    for src_code_zipfile in zipfiles:
        if not dry_run:
            utils.print_info(f"Uploading {src_code_zipfile}...")
        else:
            utils.print_info(f"Uploading {src_code_zipfile}... (dry run)")

        # Make a new tmp folder to store the unzipped files before upload
        # We put each zip file in its own folder to avoid conflicts in case two zip files have the same repo
        # in them (they will be resolved server-side)
        tmp_dir = Path(tempfile.mkdtemp())
        with zipfile.ZipFile(src_code_zipfile, mode="r") as archive:
            try:
                archive.extractall(tmp_dir)
            except zipfile.BadZipFile:
                utils.print_fatal(
                    f"File [bold]{src_code_zipfile}[/bold] is not a valid zip file."
                )

        # Go through all files and ignore any that are not text files

        fq_file_list = []

        # Build a list of all files.
        for root, _, walkfiles in os.walk(tmp_dir):
            for file in walkfiles:
                file_path = Path(root) / file

                fq_file_list.append(file_path)

        uploaded_files = []
        ignored_binary_files = []

        for file in track(fq_file_list, description="Uploading files..."):
            # Try to figure out if the file is binary or text. We ignore any binary files.
            mime_type, _ = mimetypes.guess_type(file)

            # If the file is text, read it and upload it
            # Weirdly, usually if the mimetype can't be detected, and returns "none", it means it's (usually)
            # a text file.
            if (
                mime_type is None
                or mime_type.startswith("text")
                or "xml" in mime_type
                or "json" in mime_type
            ):

                with open(file, "rb") as f:
                    file_content = f.read()

                if b"\x00" in file_content:
                    utils.print_warning(
                        f"File {file.relative_to(tmp_dir)} contains null bytes. It will be ignored."
                    )
                    ignored_binary_files.append(file)
                    continue

                # Try to detect the encoding of the file
                encoding = chardet.detect(file_content)["encoding"]

                if encoding is None:
                    encoding = "utf-8"

                # Decode it to a string
                try:
                    file_content = file_content.decode(encoding)
                except UnicodeDecodeError:
                    utils.print_warning(
                        f"File {file.relative_to(tmp_dir)} is not a valid text file. It will be ignored."
                    )
                    ignored_binary_files.append(file)
                    continue

                # If the contents are larger than 100 MB, warn the user and ignore the file
                if len(file_content) > 100000000:
                    utils.print_warning(
                        f"File {file.relative_to(tmp_dir)} is larger than 100 MB. It will be ignored."
                    )
                    ignored_binary_files.append(file)
                    continue

                uploaded_files.append(file)

                # Get the source code descriptor, including the file hash
                full_artifact_descriptor = utils.get_source_file_descriptor_with_hash(
                    file, tmp_dir
                )

                with utils.get_api_client(project_info) as api_client:
                    api_instance = loci_client.DefaultApi(api_client)
                    artifact_note_in = ArtifactNoteIn(
                        type=ArtifactNoteTypeEnum.SNAPSHOT_TXT,
                        submission_tool=SubmissionTool("loci-cli"),
                        artifact_status=ArtifactInStatus(ArtifactStatusEnum.TODO),
                        artifact_priority=ArtifactInPriority(ArtifactPriorityEnum.LOW),
                        artifact_descriptor=ArtifactDescriptor(
                            full_artifact_descriptor
                        ),
                        contents=file_content,
                        artifact_type=ArtifactInType(ArtifactTypeEnum.SOURCE_CODE_FILE),
                    )

                    if not dry_run:
                        try:
                            api_instance.create_note(
                                project_info.project_id, artifact_note_in
                            )
                        except loci_client.ApiException as e:
                            utils.print_fatal(f"Error uploading {file_path}: {e}")
                            continue
            else:
                ignored_binary_files.append(file)

        utils.print_info(f"Finished uploading [bold]{src_code_zipfile}[/bold]")

        if dry_run:
            utils.print_info(f"  Will upload {len(uploaded_files)} files.")

            for file in uploaded_files:
                utils.print_info(f"    - {file.relative_to(tmp_dir)}")
        else:
            utils.print_info(f"  Uploaded {len(uploaded_files)} files.")

        if dry_run:
            utils.print_info(f"  Will ignore {len(ignored_binary_files)} files.")
            for file in ignored_binary_files:
                utils.print_info(f"    - {file.relative_to(tmp_dir)}")
        else:
            utils.print_info(f"  Ignored {len(ignored_binary_files)} files.")

        # Clean up the tmp folder
        shutil.rmtree(tmp_dir)
