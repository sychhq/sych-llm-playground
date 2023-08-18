"""Module to list deployed resources on the cloud.

This module contains a function to display deployed models and endpoints.
The resources are listed by type, and the list function
can be executed directly from the command-line interface.

Functions:
    list: Command-line interface function to list deployed resources.
"""

import boto3
import click

from .utils.credentials import load_credentials
from .utils.resources import get_resources


@click.command(help="Display resources deployed on the cloud.")
def list() -> None:
    """List deployed resources on the cloud.

    This function retrieves and prints the names of deployed models and endpoints.
    It uses the `get_resources` function from the `utils.resources`
    module to fetch the resources and prints them in a user-friendly format.
    """
    load_credentials()
    sagemaker_client = boto3.client("sagemaker")

    resource_types = ["Model", "Endpoint"]
    for resource_type in resource_types:
        resources = get_resources(resource_type, sagemaker_client)
        click.secho(f"Deployed {resource_type}s:", fg="yellow")
        for resource in resources:
            click.secho(resource, fg="green")
    click.secho("\n", nl=False)


if __name__ == "__main__":
    list()
