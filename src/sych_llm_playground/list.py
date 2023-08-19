"""Module to list deployed resources with the chosen provider.

This module contains a function to display deployed resources,
allowing the user to choose the provider for listing.

Functions:
    list: CLI function to list deployed resources with the selected provider.
"""

import click

from .utils.provider_selection import select_provider_and_call_function


@click.command(help="Display deployed resources.")
def list() -> None:
    """List deployed resources with the chosen provider.

    This function prompts the user to select a provider.
    Then, it retrieves and prints the names of deployed resources.
    """
    select_provider_and_call_function("list")


if __name__ == "__main__":
    list()
