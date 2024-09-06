from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
import loci_client
import pendulum

import loci.utils as utils

app = typer.Typer()
console = Console()


@app.callback()
def callback():
    """
    Manage Loci Notes projects.
    """
    pass


@app.command()
def add(
    server: Optional[str] = typer.Option(default_factory=utils.default_server_factory),
    name: str = typer.Argument(..., help="The name of the project to create."),
    force: bool = typer.Option(False, help="Force the creation of the project."),
):
    """
    Create a new project, or inform of the better way to create projects.
    """
    if not force:
        utils.print_fatal(
            "Use [bold]loci setup[/bold] to create a new project and automatically associate it with a working "
            "directory. If you're very sure you want to create a project here without associating to a local "
            f'directory, use [bold]loci add "{name}" --force[/bold].'
        )

    # A lot of what follows is similar to the setup command.
    # Usually, a lot of the API setup would be covered by a ProjectConfig obj, but here we're doing it manually
    # since we need to know what server in which to create the project.
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

    with loci_client.ApiClient(authd_config) as api_client:
        api_instance = loci_client.ProjectsApi(api_client)

        project_create = loci_client.models.ProjectBase(name=name)
        api_response = api_instance.projects_create_project(project_create)
        project_out = loci_client.ProjectOut.from_dict(api_response.to_dict())
        utils.print_success(f"Project [bold]{project_out.name}[/bold] created.")


@app.command()
def list(
    server: Optional[str] = typer.Option(default_factory=utils.default_server_factory),
    sort: Optional[loci_client.ProjectSortEnum] = typer.Option(
        loci_client.ProjectSortEnum.CREATED_AT,
        help="Sort the projects by name or date.",
    ),
    reverse: bool = typer.Option(False, help="Reverse the sort order."),
):
    """
    List all projects to which the user has access.
    """
    # Usually, a lot of the API setup would be covered by a ProjectConfig obj, but here we're doing it manually
    # since we need to know what server in which to create the project.
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

    with loci_client.ApiClient(authd_config) as api_client:
        api_instance = loci_client.ProjectsApi(api_client)

        projects = []
        total_project_count = -1
        if reverse:
            order = loci_client.OrderByEnum.DESC
        else:
            order = loci_client.OrderByEnum.ASC

        while len(projects) != total_project_count:
            api_response = api_instance.projects_read_projects(
                skip=len(projects), sort=sort, order=order
            )
            projects_out_obj = loci_client.ProjectsOut.from_dict(api_response.to_dict())
            total_project_count = projects_out_obj.count
            for project_obj in projects_out_obj.data:
                projects.append(project_obj)

    table = Table(title="Projects")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Created")

    for project in projects:
        table.add_row(
            str(project.id),
            project.name,
            pendulum.instance(project.created_at).diff_for_humans(),
        )

    console.print(table)


@app.command()
def get(
    server: Optional[str] = typer.Option(default_factory=utils.default_server_factory),
    project_id: int = typer.Argument(..., help="The ID of the project."),
):
    """
    Get the full details of a project.
    """
    # Remove trailing slash from server URL
    if server[-1] == "/":
        # This doesn't account for jokers who put a bunch, but I'll fix it later TODO
        server = server[:-1]

    # Usually, a lot of the API setup would be covered by a ProjectConfig obj, but here we're doing it manually
    # since we need to know what server in which to create the project.
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

    with loci_client.ApiClient(authd_config) as api_client:
        api_instance = loci_client.ProjectsApi(api_client)

        try:
            api_response = api_instance.projects_read_project(project_id)
        except Exception as e:
            utils.handle_exception(e)

        project = loci_client.ProjectFullOut.from_dict(api_response.to_dict())
        if project is None:
            utils.print_fatal(f"Project with ID [bold]{project_id}[/bold] not found.")

    table = Table(title="Project Details")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Created")
    table.add_row(
        str(project.id),
        project.name,
        pendulum.instance(project.created_at).diff_for_humans(),
    )
    console.print(table)

    table = Table(title="Project Managers")
    table.add_column("ID", justify="right")
    table.add_column("Email")
    table.add_column("Name")
    manager_count = len(project.managers)
    for manager in project.managers:
        table.add_row(str(manager.id), manager.email, manager.full_name)
    if manager_count > 0:
        console.print(table)

    table = Table(title="Project Members")
    table.add_column("ID", justify="right")
    table.add_column("Email")
    table.add_column("Name")
    user_count = 0
    for user in project.users:
        if user not in project.managers:
            user_count += 1
            table.add_row(str(user.id), user.email, user.full_name)
    if user_count > 0:
        console.print(table)
