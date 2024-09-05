from typing import Annotated, Optional
import typer
import warnings

from loci import project
from loci.upload import upload
from loci.login import login
from loci.setup import setup
from loci.sync import sync
from loci.semgrep import semgrep
from loci.config import config
from loci.check import check
from loci.version import __version__ as version

app = typer.Typer()
app.command()(upload)
app.command()(login)
app.command()(setup)
app.command()(sync)
app.command()(semgrep)
app.command()(config)
app.command()(check)

app.add_typer(project.app, name="project")


@app.callback(name="version")
def version_callback(value: bool):
    if value:
        print(f"Loci Notes CLI Tool v{version}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
):
    """
    Interact with a Loci Notes server, CLI-style.
    """
    # Disable Pydantic warnings that are spit out to the console.
    warnings.filterwarnings("ignore", category=UserWarning)
