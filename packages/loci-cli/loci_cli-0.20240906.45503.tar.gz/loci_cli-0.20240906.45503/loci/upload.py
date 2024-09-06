import typer
from typing import Optional, List
from pathlib import Path
import os

import loci_client

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
        if dry_run:
            utils.print_info(f"Uploading {src_code_zipfile}... (dry run)")
            continue

        utils.print_info(f"Uploading {src_code_zipfile}...")

        with utils.get_api_client(project_info) as api_client:
            api_instance = loci_client.DefaultApi(api_client)

            # with BytesIO(src_code_zipfile.read_bytes()) as f:
            # file_bytes = f.read()

            try:
                api_instance.upload_project_zipfile(
                    project_info.project_id, bytes(src_code_zipfile)
                )
                utils.print_success(f"Uploaded {src_code_zipfile}.")

            except loci_client.ApiException as e:
                utils.handle_exception(e)
                utils.print_error(f"Failed to upload {src_code_zipfile}.")

    utils.print_info("Please wait for the server to process the files.")
