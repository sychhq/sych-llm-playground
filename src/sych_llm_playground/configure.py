"""Module for CLI configuration.

This module provides functions and a CLI command for Playground setup.
Users can select a provider and configure credentials.

Functions:
    print_welcome: Prints a welcome message.
"""

import click

from .utils.provider_selection import select_provider_and_call_function


def print_welcome() -> None:
    """Print a welcome message.

    This function prints a welcome message and introductory text for
    the Sych LLM Playground CLI configuration.
    """
    welcome_message = """
                 ******
            *******  ******
        *******          *******
      ****,      *****       *****
      ***    **************    ***   @@@@@@@@@                    @@@
      ***    ***       ****    ***   @@@       @@@   @@@  @@@@@@@ @@@@@@@@
      ***    ***       ****    ***    @@@@@@@@  @@@ @@@  @@@      @@@   @@@
      **     *****    *****    ***  @&     @@@   @@@@@   @@@      @@@   @@@
          **************       ***   @@@@@@@      @@@      @@@@@@ @@@   @@@
      *******              *******               @@@
          *******      ******
               **********
                   ** \n"""
    click.secho(welcome_message, fg="yellow")
    click.secho(
        "Welcome to the Sych LLM Playground CLI.\n"
        + "This tool is part of our efforts to "
        + "contribute to the open-source community.\n"
        + "Explore more at https://sych.io\n\n"
        + "For detailed documentation, visit "
        + "https://sych-llm-playground.readthedocs.io\n\n"
        + "Let's begin with the configuration.\n",
        fg="cyan",
    )


@click.command(help="Set up CLI.")
def configure() -> None:
    """Configure CLI for the Playground.

    Print welcome, prompt for provider selection,
    and set up credentials by calling the
    provider-specific function.
    """
    print_welcome()

    select_provider_and_call_function("configure")
