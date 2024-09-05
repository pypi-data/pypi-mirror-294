# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer",
#   "rich",
#   "httpx",
#   "shellingham",
#   "html2text",
#   "python-dotenv",
#   "ollama",
#   "openai",
#   "groq"
# ]
# ///
import asyncio

from civitai_models_manager.__version__ import __version__
from civitai_models_manager import (
    MODELS_DIR,
    CIVITAI_TOKEN,
    CIVITAI_MODELS,
    CIVITAI_DOWNLOAD,
    CIVITAI_VERSIONS,
    TYPES,
    FILE_TYPES,
    OLLAMA_OPTIONS,
    OPENAI_OPTIONS,
    GROQ_OPTIONS,
)
from typing import List
from .modules.helpers import feedback_message, display_readme
from .modules.tools import sanity_check_cli
from .modules.stats import inspect_models_cli
from .modules.details import get_model_details_cli
from .modules.list import list_models_cli, local_search_cli
from .modules.download import download_model_cli
from .modules.ai import explain_model_cli
from .modules.search import search_cli_sync
from .modules.remove import remove_models_cli
from .modules.create import create_image_cli
import typer

from rich.traceback import install

install()

"""
====================================================================
Civitai Model Manager - Simplified Model Retrieval and Management
====================================================================

Simple CLI tool that streamlines the process of managing AI models from the
CivitAI platform. It offers functionalities to list available models,it
view their details, search, download selected variants, and remove models from
local storage. It also provides a summary of the model description using
Ollama or OpenAI.

Usage:
$ pipx install civitai-models or pip install civitai-models [not on pip yet]
$ pip install . or pipx install . # To install the package locally (recommended)
$ civitai-model-manager [OPTIONS] [COMMAND] [ARGS]

Options:
    details INT                   Get detailed information about a specific model by ID.
    download INT                  Download a specific model variant by ID.
    explain INT                   Get a summary of a specific model by ID.
    list                          List available models along with their types and paths.
    stats                         Stats on the parent models directory.
    sanity-check                  Check to see if the app is ready to run.
    search TEXT --query           Search for models by query, tag, or types, which are optional via the API.
    remove                        Remove specified models from local storage.
    --help                        Show this message and exit.

Examples:

$ civitai-models list
$ civitai-models stats
$ civitai-models details 12345 [desc] [images]
$ civitai-models download 54321 [--select]
$ civitai-models remove
$ civitai-models explain 12345 [--service ollama]
$ civitai-models search "text" [--tag "tag1"] [--types "Checkpoint"] [--limit 20] [--sort "Highest Rated"] [--period "AllTime"]
$ civitai-models sanity-check
$ civitai-models help
$ civitai-models version
"""

__version__ = __version__

__all__ = ["civitai_cli"]

civitai_cli = typer.Typer()
create_cli = typer.Typer()
civitai_cli.add_typer(
    create_cli, name="generate", help="Services on the CivitAI platform."
)


@civitai_cli.command(
    "search",
    help="Search for models by query, tag, or types, which are optional via the API.",
)
def search_models_command(
    query: str = "",
    tag: str = None,
    types: str = "Checkpoint",
    limit: int = 20,
    sort: str = "Highest Rated",
    period: str = "AllTime",
):
    search_cli_sync(
        query,
        tag,
        types,
        limit,
        sort,
        period,
        CIVITAI_MODELS=CIVITAI_MODELS,
        TYPES=TYPES,
    )


@civitai_cli.command(
    "explain",
    help="Get a summary of a specific model by ID using the specified service (default is Ollama).",
)
def explain_model_command(identifier: str, service: str = "ollama"):
    """
    Get a summary of a specific model by ID using the specified service (default is Ollama).
    :param identifier: The ID of the model.
    :param service: The specified service to use (default is "ollama").
    """
    explain_model_cli(
        identifier,
        service,
        CIVITAI_MODELS=CIVITAI_MODELS,
        CIVITAI_VERSIONS=CIVITAI_VERSIONS,
        OLLAMA_OPTIONS=OLLAMA_OPTIONS,
        OPENAI_OPTIONS=OPENAI_OPTIONS,
        GROQ_OPTIONS=GROQ_OPTIONS,
    )


@civitai_cli.command("local-search", help="Search for models stored on disk.")
def local_search_command(query: str):
    return local_search_cli(query, MODELS_DIR=MODELS_DIR, FILE_TYPES=FILE_TYPES)


@civitai_cli.command("sanity-check", help="Check to see if the app is ready to run.")
def sanity_check_command():
    """
    Check to see if the app is ready to run.
    :return: The result of the sanity check.
    """
    return sanity_check_cli(
        CIVITAI_MODELS=CIVITAI_MODELS,
        CIVITAI_VERSIONS=CIVITAI_VERSIONS,
        OLLAMA_OPTIONS=OLLAMA_OPTIONS,
        OPENAI_OPTIONS=OPENAI_OPTIONS,
        GROQ_OPTIONS=GROQ_OPTIONS,
    )


@create_cli.command("image", help="Generate a image on the CivitAI platform.")
def create_image_command(
    model: int,
):
    """
    Generate a image on the CivitAI platform.
    :return: The result of the image creation.
    """
    #create_image_cli(CIVITAI_MODELS, CIVITAI_VERSIONS, model)
    feedback_message("Coming in v0.8.2", "info")


@create_cli.command("check-jobs", help="Fetch jobs details based on token or Job ID.")
def fetch_job_command(
    token: str = None, is_job_id: bool = False, query: str = None, cancel: bool = False
):
    """
    Fetch jobs details based on token or Job ID.
    :return: The result of the job details.
    """
    feedback_message("Coming in v0.8.2", "info")


@civitai_cli.command(
    "list", help="List available models along with their types and paths."
)
def list_models_command():
    """
    List available models along with their types and paths.
    :return: The list of available models.
    """
    list_models_cli()


@civitai_cli.command("stats", help="Stats on the parent models directory.")
def stats_command():
    """
    Stats on the parent models directory.
    :return: The stats on the parent models directory.
    """
    return inspect_models_cli(MODELS_DIR=MODELS_DIR)


@civitai_cli.command(
    "details", help="Get detailed information about a specific model by ID."
)
def details_command(identifier: str, desc: bool = False, images: bool = False):
    """
    Get detailed information about a specific model by ID.
    :param identifier: The ID of the model.
    :param desc: The description of the model.
    :param images: The images of the model.
    :return: The detailed information about the model.
    """
    get_model_details_cli(
        identifier,
        desc,
        images,
        CIVITAI_MODELS=CIVITAI_MODELS,
        CIVITAI_VERSIONS=CIVITAI_VERSIONS,
    )


@civitai_cli.command("download", help="Download up to 3 specific model variants by ID.")
def download_model_command(
    identifiers: List[str] = typer.Argument(
        ..., help="The IDs of the models to download (up to 3)"
    ),
    select: bool = typer.Option(
        False, "--select", "-s", help="Enable version selection for each model"
    ),
):
    """
    Download up to 3 specific model variants by ID.
    :param identifiers: The IDs of the models to download (up to 3).
    :param select: Enable version selection for each model.
    :return: None
    """
    if len(identifiers) > 3:
        typer.echo(
            "You can download a maximum of 3 models at a time. Only the first 3 will be processed."
        )
        identifiers = identifiers[:3]

    typer.echo(f"Preparing to download {len(identifiers)} model(s)...")

    download_model_cli(
        identifiers,
        select,
        MODELS_DIR=MODELS_DIR,
        CIVITAI_MODELS=CIVITAI_MODELS,
        CIVITAI_DOWNLOAD=CIVITAI_DOWNLOAD,
        CIVITAI_VERSIONS=CIVITAI_VERSIONS,
        CIVITAI_TOKEN=CIVITAI_TOKEN,
        TYPES=TYPES,
        FILE_TYPES=FILE_TYPES,
    )


@civitai_cli.command("remove", help="Remove specified models from local storage.")
def remove_models_command():
    """
    Remove specified models from local storage.
    :return: The removal of the models.
    """
    remove_models_cli(MODELS_DIR=MODELS_DIR, TYPES=TYPES, FILE_TYPES=FILE_TYPES)


@civitai_cli.command("version", help="Current version of the CLI.")
def version_command():
    """
    Current version of the CLI.
    :return: The current version of the CLI.
    """
    feedback_message(f"Current version: {__version__}", "info")


@civitai_cli.command("about", help="Show README.md content.")
def about_command():
    """
    Show README.md content.
    :return: The README.md content.
    """
    display_readme("README.md")
