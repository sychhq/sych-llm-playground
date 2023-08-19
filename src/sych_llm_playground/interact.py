"""This module enables interaction with deployed models.

The module provides functions to select and communicate
with models deployed on various cloud providers.

Functions:
    interact: CLI function to interact with deployed models.
"""

import click

from .utils.provider_selection import select_provider_and_call_function


@click.command(help="Communicate with deployed models.")
def interact() -> None:
    """Interact with deployed models on the cloud.

    This function allows users to select and interact with
    models, delegating specific provider handling to the
    `select_provider_and_call_function` method.
    """
    select_provider_and_call_function("interact")
