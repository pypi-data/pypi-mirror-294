import typer

from loci import utils


def config():
    """
    Show the local configuration file for the Loci CLI.
    """
    utils.print_info("Locating the Loci Notes local configuration file...")
    config_file_location = utils.get_loci_config_file_path()
    typer.launch(config_file_location, locate=True)
