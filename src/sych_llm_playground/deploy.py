"""This module provides a CLI to deploy models with the chosen provider.

It utilizes the `click` library to create a user-friendly CLI and prompts
the user to select a provider. The deployment is then handled by calling
the provider-specific function through the
`select_provider_and_call_function` method from the
`utils.provider_selection` module.
"""

import click

from .utils.provider_selection import select_provider_and_call_function


@click.command(help="Deploy models.")
def deploy() -> None:
    """Deploy the selected model with the chosen provider.

    This function prompts the user to select a provider.
    It handles the deployment process by calling the
    provider-specific function.
    """
    select_provider_and_call_function("deploy")
