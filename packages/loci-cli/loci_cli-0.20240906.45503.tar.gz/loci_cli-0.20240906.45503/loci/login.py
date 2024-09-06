import typer
import os
import socket
from typing import Optional

import loci_client
from loci_client.models.description import Description

from loci import utils


def login(
    server: Optional[str] = typer.Option(prompt=True, default="http://localhost"),
    username: Optional[str] = typer.Option(prompt=True),
    password: Optional[str] = typer.Option(prompt=True, hide_input=True),
    force: bool = typer.Option(False),
):
    """
    Login to a Loci Notes server, and obtain an API token for use with the CLI and other clients.
    """
    # Remove trailing slash from server URL
    if server[-1] == "/":
        # This doesn't account for jokers who put a bunch, but I'll fix it later TODO
        server = server[:-1]

    # First make sure we don't already have creds for this server, if so we need to overwrite them.
    client_id = utils.get_local_config_value(server, "client_id")
    secret_key = utils.get_local_config_value(server, "secret_key")
    if client_id is not None and secret_key is not None:
        if not force:
            utils.print_fatal(
                "API key already exists for this server. Use --force to overwrite."
            )
        else:
            utils.print_warning("Overwriting existing API key for this server.")

    utils.print_info(f"Logging in to Loci Notes server at {server} as {username}...")

    unauthd_config = loci_client.Configuration()
    unauthd_config.host = server

    tmp_access_token = None

    with loci_client.ApiClient(unauthd_config) as api_client:
        # Create an instance of the API class
        api_instance = loci_client.DefaultApi(api_client)
        api_response = api_instance.login_access_token(
            username=username,
            password=password,
        )
        res_dict = api_response.to_dict()
        tmp_access_token = res_dict["access_token"]
        utils.print_success("Login successful!")

    authd_config = loci_client.Configuration()
    authd_config.host = server
    authd_config.access_token = tmp_access_token

    with loci_client.ApiClient(authd_config) as api_client:
        # Call the API Keys endpoint to get a new API key
        local_user = os.getlogin()
        local_hostname = socket.gethostname()
        desc_str = f"{local_user}@{local_hostname}"
        utils.print_info(
            f"Creating and saving a new API key [bold]{desc_str}[/bold]..."
        )

        api_instance = loci_client.DefaultApi(api_client)

        api_key_create = loci_client.ApiKeyIn(
            description=Description(
                desc_str,
            ),
        )

        api_key_out = api_instance.create_api_key(api_key_create)
        client_id = api_key_out.client_id

        if (
            api_key_out.secret_key is None
            and api_key_out.secret_key.actual_instance is None
        ):
            utils.print_fatal(
                "Secret key was not returned from server. This is unexpected."
            )
        # This is idiotic.
        secret_key = api_key_out.secret_key.actual_instance

        # Save the API key to the local config file
        utils.set_local_config_value(server, "client_id", client_id)
        utils.set_local_config_value(server, "secret_key", secret_key)

        utils.print_success(
            "API key created and saved to " + utils.get_loci_config_file_path()
        )
