"""Module to list deployed resources on AWS.

This module contains a function to display deployed models and endpoints on AWS.
The resources are listed by type (Model, Endpoint), and the `list` function
can be executed directly from the command-line interface to view all AWS
deployed resources.

Functions:
    list: Function to list deployed resources on AWS SageMaker.

AWS Services:
    - AWS SageMaker: Used to retrieve information about deployed models and endpoints.
    - AWS API Gateway: Use to create and manage API Endpoints.

Dependencies:
    - boto3: AWS SDK for Python, used to interface with AWS services.
    - click: Command Line Interface Creation Kit, used for CLI interaction.
"""

import boto3
import click

from .utils.credentials import load_credentials
from .utils.resources import get_resources


def list() -> None:
    """List deployed resources on AWS SageMaker.

    This function retrieves and prints the names of deployed models and endpoints
    on and their public API Gateways. It uses the `get_resources`
    function from the `utils.resources` module to fetch the resources,
    specifically targeting AWS SageMaker services, and prints them in
    a user-friendly format.
    """
    load_credentials()

    resource_types = ["Model", "Endpoint", "API Gateway"]
    for resource_type in resource_types:
        client = (
            boto3.client("sagemaker")
            if resource_type != "API Gateway"
            else boto3.client("apigateway")
        )
        resources = get_resources(resource_type, client)
        click.secho(f"Deployed {resource_type}s:", fg="yellow")
        for resource in resources:
            click.secho(resource, fg="green")
    click.secho("\n", nl=False)


if __name__ == "__main__":
    list()
