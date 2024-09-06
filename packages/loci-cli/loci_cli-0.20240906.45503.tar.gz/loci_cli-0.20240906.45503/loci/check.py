from typing import Optional
import typer
import os
import loci_client as lnc
import json

from loci import utils


def check(
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
):
    """
    Check the local configuration of Loci Notes.
    """
    utils.print_info("Checking the Loci Notes local configuration...")
    project_config = utils.get_project_info(project_dir)
    if project_config is None:
        utils.print_fatal(
            f"The directory [bold]{project_dir}[/bold] is not a Loci project."
        )
    else:
        if not isinstance(project_config, utils.ProjectConfig):
            utils.print_fatal(
                f"The project in directory [bold]{project_dir}[/bold] is not "
                "authenticated. Use [bold]loci login[/bold] to authenticate."
            )
        # Get the user's information
        # Check the creds by getting the project information
        with utils.get_api_client(project_config) as api_client:
            api_instance = lnc.DefaultApi(api_client)
            try:
                user = api_instance.read_user_me()

            except lnc.ApiException as e:
                details = json.loads(e.body)["detail"]
                utils.print_fatal(
                    f"Error getting user information from {project_config.server}: {details}"
                )
            try:
                project = api_instance.read_project(project_config.project_id)
            except lnc.ApiException as e:
                details = json.loads(e.body)["detail"]
                utils.print_fatal(
                    f"Error getting project information from {project_config.server}: {details}"
                )

        utils.print_success("Loci project configuration:")
        name = (
            user.full_name
            if user.full_name is not None and user.full_name != ""
            else user.email
        )
        utils.print_success(f"Server: [bold]{project_config.server}[/bold]")
        utils.print_success(f"User: [bold]{name}[/bold]")
        utils.print_success(f"Project: [bold]{project.name}[/bold]")
        utils.print_success(f"Directory: [bold]{project_dir}[/bold]")
