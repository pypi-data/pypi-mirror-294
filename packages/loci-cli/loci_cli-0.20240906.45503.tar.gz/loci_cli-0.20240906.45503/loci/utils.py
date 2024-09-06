import os
import rich
import typer
import pathlib
import configparser
import datetime
from pydantic import BaseModel
import json
import hashlib

import loci_client as lnc
from loci import LOCI_CONFIG_DIR, LOCI_CONFIG_FILENAME, LOCI_PROJECT_FILENAME


class ProjectUnauthdConfig(BaseModel):
    """
    A project configuration object that does not include the client ID and secret key.
    """

    server: str
    project_id: int


class ProjectConfig(ProjectUnauthdConfig):
    """
    A full project configuration, including the client ID and secret key.
    """

    client_id: str
    secret_key: str
    created_at: datetime.datetime = datetime.datetime.now()


def escape(msg: str) -> str:
    """
    Escape a message for rich printing.
    """
    return rich.escape(msg)


def _print(header: str, msg: any) -> None:
    """
    A helper function to print a message with a header.
    """
    rich.print(header, msg)


def print_info(msg: any) -> None:
    """
    Print an info message.
    """
    _print(
        header="[white][[/white][bold blue]INFO[/bold blue][white]][/white]", msg=msg
    )


def print_warning(msg: any) -> None:
    """
    Print a warning message.
    """
    _print(
        header="[white][[/white][bold yellow]WARNING[/bold yellow][white]][/white]",
        msg=msg,
    )


def print_success(msg: any) -> None:
    """
    Print a success message.
    """
    _print(
        header="[white][[/white][bold green]SUCCESS[/bold green][white]][/white]",
        msg=msg,
    )


def print_error(msg: any) -> None:
    """
    Print an error message.
    """
    _print(header="[white][[/white][bold red]ERROR[/bold red][white]][/white]", msg=msg)


def print_fatal(msg: any) -> None:
    """
    Print a fatal error message and exit the program with a status code of 1.
    """
    _print(header="[white][[/white][bold red]ERROR[/bold red][white]][/white]", msg=msg)
    raise typer.Exit(code=1)


def get_loci_config_file_path() -> str:
    """
    Returns the path to the Loci config file, which is stored in the user's app directory. This is not the same as
    the project config file.
    """
    app_config_dir = typer.get_app_dir(app_name=LOCI_CONFIG_DIR)
    app_config_dir = pathlib.Path(app_config_dir)
    app_config_dir.mkdir(parents=True, exist_ok=True)
    config_file_path: pathlib.Path = pathlib.Path(app_config_dir) / LOCI_CONFIG_FILENAME
    return str(config_file_path)


def get_local_config() -> configparser.ConfigParser:
    """
    This will get a configparser object for the local Loci config file, which stores access tokens for each of the
    Loci Notes server configured on this system.
    """
    try:
        config = configparser.ConfigParser()
        config.sections()
        config.read(get_loci_config_file_path())
        return config
    except configparser.Error:
        print_fatal(
            "Error reading Loci config file at [bold]"
            + get_loci_config_file_path()
            + "[/bold]"
        )


def get_local_config_servers() -> list[str]:
    """
    This will get a list of servers from the local Loci config file.
    """
    config = get_local_config()
    return config.sections()


def get_local_config_value(server: str, key: str) -> str:
    """
    This will get a value from the local Loci config file, or None if it doesn't exist in the file.
    """
    config = get_local_config()

    # Escape periods in the server name
    server = server.replace(".", "\\.")

    if server not in config:
        return None
    if key not in config[server]:
        return None
    return config[server][key]


def set_local_config_value(server: str, key: str, value: str) -> None:
    """
    This will set a value in the local Loci config file.
    """
    try:
        config = configparser.ConfigParser()
        config.sections()
        config.read(get_loci_config_file_path())
    except configparser.Error:
        # This is a new file, so we need to create it. This is fine.
        pass

    # Escape periods in the server name
    server = server.replace(".", "\\.")

    if server not in config:
        config[server] = {}
    config[server][key] = value

    with open(get_loci_config_file_path(), "w") as configfile:
        config.write(configfile)


def set_project_config(
    project_config: ProjectConfig | ProjectUnauthdConfig, project_dir: str = None
) -> None:
    """
    Set the project configuration for a project in a directory. This will write a .loci-project.ini file in the
    project directory, which defaults to the current directory. If the project configuration includes access
    credentials, it will also write those to a separate Loci config file, stored in the user's config directory.
    """
    config = configparser.ConfigParser()
    config.sections()
    config["default"] = {}
    config["default"]["server"] = project_config.server
    config["default"]["project_id"] = str(project_config.project_id)

    if project_dir is None:
        project_dir = os.getcwd()

    with open(pathlib.Path(project_dir, LOCI_PROJECT_FILENAME), "w") as configfile:
        config.write(configfile)

    if isinstance(project_config, ProjectConfig):
        set_local_config_value(
            project_config.server, "client_id", project_config.client_id
        )
        set_local_config_value(
            project_config.server,
            "secret_key",
            project_config.secret_key,
        )


def get_project_config(
    project_dir: str = None, check_parents: bool = False
) -> ProjectConfig | ProjectUnauthdConfig | None:
    """
    This will get the project information from a directory. If `check_parents` is True, it will
    recurse up through directories until a project file is found or a top level directory is hit.
    If nothing is found, it will return None.
    """
    config = configparser.ConfigParser()
    config.sections()

    if project_dir is None:
        # If no dir is passed, use the current directory.
        project_dir = os.getcwd()

    current_dir = project_dir
    last_dir = ""

    while True:
        try:
            config.read(pathlib.Path(current_dir, LOCI_PROJECT_FILENAME))
            pc = ProjectUnauthdConfig(
                server=config["default"]["server"],
                project_id=int(config["default"]["project_id"]),
            )

            # Try to see if we can get access credentials from the local user's config file.
            client_id = get_local_config_value(pc.server, "client_id")
            secret_key = get_local_config_value(pc.server, "secret_key")

            if client_id is None or secret_key is None:
                return pc

            pc_new = ProjectConfig(
                server=pc.server,
                project_id=pc.project_id,
                client_id=client_id,
                secret_key=secret_key,
            )
            return pc_new

        except KeyError:
            if not check_parents:
                # Do NOT recurse up through directories.
                return None
            if current_dir == pathlib.Path.home() or current_dir == last_dir:
                return None
            # Recurse up one directory
            last_dir = current_dir
            current_dir = os.path.dirname(current_dir)


def get_api_client(project_config: ProjectConfig) -> lnc.ApiClient:
    """
    This returns an API client for the Loci Notes project in the current directory, or the directory passed via
    parameter. This API client uses the local config file to get the access token and server location.
    """
    config = lnc.Configuration()
    config.host = project_config.server
    config.access_token = project_config.client_id + ":" + project_config.secret_key
    return lnc.ApiClient(configuration=config)


def default_server_factory():
    """
    This is a simple function used to get the first server URL for the setup command.
    """
    servers = get_local_config_servers()
    if len(servers) == 0:
        return "http://localhost"
    else:
        return servers[0].replace("\\.", ".")


def handle_exception(e: Exception):
    """
    This function will handle an exception and print a message to the user.
    """
    if isinstance(e, lnc.ApiException):
        if e.status == 500:
            print_fatal(
                "API Error: 500 - Internal Server Error. Something went wrong, check server logs."
            )
        body_dict = json.loads(e.body)
        print_fatal(f"API Error: {e.status} - {e.reason} - {body_dict['detail']}")
    else:
        print_fatal(e)


def get_project_info(project_dir: str) -> ProjectConfig:
    """
    This function will check to see if the project directory exists, and has valid credentials. If it does not,
    it will print a fatal error message and exit the program.
    """
    fq_project_dir = os.path.abspath(project_dir)
    if not os.path.isdir(fq_project_dir):
        print_fatal(f"The directory [bold]{fq_project_dir}[/bold] does not exist.")

    project_config = get_project_config(fq_project_dir)
    if project_config is None:
        print_fatal(
            f"No Loci project found in [bold]{fq_project_dir}[/bold]. Please run [bold]loci setup[/bold] first."
        )
    if not isinstance(project_config, ProjectConfig):
        print_fatal(
            f"Project in [bold]{fq_project_dir}[/bold] does not have valid credentials. Please run "
            "[bold]loci login[/bold] first."
        )

    # Check the creds by getting the project information
    with get_api_client(project_config) as api_client:
        api_instance = lnc.DefaultApi(api_client)
        try:
            api_instance.read_project(project_config.project_id)
        except lnc.ApiException as e:
            details = json.loads(e.body)["detail"]
            print_fatal(
                f"Error getting project information for project ID {project_config.project_id}: {details}"
            )

    return project_config


def get_short_file_hash_by_contents(contents: bytes) -> str:
    """
    Get the SHA-256 hash of some file contents. Must be read in via open(file "rb").
    """
    file_hash = hashlib.sha256(contents).hexdigest()[:8]
    return file_hash


def get_short_file_hash_by_file(file_path: pathlib.Path) -> str:
    """
    Get the SHA-256 hash of a local file.
    """
    with open(file_path, "rb") as f:
        file_content = f.read()
        file_hash = get_short_file_hash_by_contents(file_content)

    return file_hash


def get_source_file_descriptor_with_hash(
    fq_file_path: pathlib.Path, containing_dir_path: pathlib.Path
) -> str:
    """
    Get the full descriptor of a file, including a short hash. This is not for security purposes, but
    for a quick way to identify a file.
    Examples:
    - "repo/src/main.py#abcdef123"
    """
    file_hash = get_short_file_hash_by_file(fq_file_path)

    return str(fq_file_path.relative_to(containing_dir_path)) + "#" + file_hash
