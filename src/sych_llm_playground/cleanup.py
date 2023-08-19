"""Module for cleaning up deployed resources with chosen provider.

This module provides the main function to delete deployed resources.
"""

import click

from .utils.provider_selection import select_provider_and_call_function


@click.command(help="Remove deployed resources.")
def cleanup() -> None:
    """Clean up resources with the chosen provider.

    This function initiates the cleanup process for deployed resources
    by calling the provider-specific function.
    """
    select_provider_and_call_function("cleanup")
