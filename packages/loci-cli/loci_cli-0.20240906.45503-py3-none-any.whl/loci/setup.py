import typer
import os
from typing import Optional

import loci_client

from loci import utils, LOCI_SRC_DIRECTORY
from loci.resources import SRC_README_MD


def setup(
    server: Optional[str] = typer.Option(
        prompt=True, default_factory=utils.default_server_factory
    ),
    # TODO there's a bug where if you set the project_dir, the default name is wrong
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
    project: Optional[str] = typer.Option(
        prompt=True,
        default=os.path.basename(os.getcwd()),
        help="The name or ID of the project.",
    ),
) -> None:
    """
    Setup a directory as a Loci Notes project workspace.
    """

    # Remove trailing slash from server URL
    if server[-1] == "/":
        # This doesn't account for jokers who put a bunch, but I'll fix it later TODO
        server = server[:-1]

    # Make sure the project directory exists
    fq_project_dir = os.path.abspath(project_dir)
    if not os.path.isdir(fq_project_dir):
        utils.print_fatal(
            f"The directory [bold]{fq_project_dir}[/bold] does not exist."
        )

    # First see if this directory is already a Loci project
    project_config = utils.get_project_config(fq_project_dir)
    if project_config is not None:
        utils.print_fatal(
            f"Directory [bold]{fq_project_dir}[/bold] is already a Loci project."
        )

    # Get the API key for this server
    client_id = utils.get_local_config_value(server, "client_id")
    secret_key = utils.get_local_config_value(server, "secret_key")

    if client_id is None or secret_key is None:
        utils.print_fatal(
            f"No API key found for server [bold]{server}[/bold]. Please run [bold]loci login[/bold] first."
        )

    # Check to see if a project by the given name already exists on the server
    authd_config = loci_client.Configuration()
    authd_config.host = server
    authd_config.access_token = f"{client_id}:{secret_key}"

    matching_project = None
    with loci_client.ApiClient(authd_config) as api_client:
        api_instance = loci_client.DefaultApi(api_client)

        # Check to see if an integer or string was given
        try:
            # Try to convert the project to an integer
            project_id = int(project)
            project_name = None

            # Get the project by ID
            matching_project = api_instance.read_project(project_id)

        except ValueError:
            # If it's not an integer, it must be a string
            # Get a list of all projects, then search for the project by name.
            # If it's not found, create it.
            project_id = None
            project_name = project

            projects = []
            total_projects_count = -1
            while len(projects) != total_projects_count:
                api_response = api_instance.read_projects()
                projects_out_obj = loci_client.ProjectsOut.from_dict(
                    api_response.to_dict()
                )
                total_projects_count = projects_out_obj.count
                for project_obj in projects_out_obj.data:
                    projects.append(project_obj)

            for project_obj in projects:
                if project_obj.name == project_name:
                    matching_project = project_obj
                    break

            if matching_project is None:
                utils.print_info(
                    f"The project [bold]{project_name}[/bold] could not be found..."
                )

                typer.confirm(f"Create the project {project_name}?", abort=True)

                project_create = loci_client.models.ProjectIn(name=project_name)
                api_response = api_instance.create_project(project_create)
                project_out = loci_client.ProjectOut.from_dict(api_response.to_dict())
                matching_project = project_out
                utils.print_success(f"Project [bold]{project_name}[/bold] created!")

        except loci_client.ApiException as e:
            utils.print_fatal(f"Error reading project: {e}")

        # Create the project config file
        project_config = utils.ProjectUnauthdConfig(
            server=server,
            project_id=matching_project.id,
        )

        utils.set_project_config(
            project_config=project_config, project_dir=fq_project_dir
        )
        utils.print_success(
            f"Project [bold]{project_name}[/bold] saved to [bold]{fq_project_dir}[/bold]."
        )

        fq_src_dir = os.path.join(fq_project_dir, LOCI_SRC_DIRECTORY)
        if not os.path.isdir(fq_src_dir):
            os.mkdir(fq_src_dir)
            utils.print_success(
                f"Loci Notes source directory [bold]{fq_src_dir}[/bold] created."
            )
            utils.print_info(
                "Store your Loci Notes source files in this directory. See the README for more information."
            )

        src_readme_path = os.path.join(fq_src_dir, "README-LOCI.md")
        with open(src_readme_path, "w") as f:
            f.write(SRC_README_MD)
