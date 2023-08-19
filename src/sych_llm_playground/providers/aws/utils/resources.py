"""Utility module for fetching specific AWS resources.

This module contains functions to get deployed cloud resources
such as models and endpoints.
"""

from typing import Any

import click

from ....utils.loader import start_loader
from ....utils.loader import stop_loader


def get_resources(
    resource_type: str, sagemaker_client: Any, max_results: int = 99
) -> list[str]:
    """Fetch deployed AWS resources based on the resource type.

    This function retrieves the specified resource,
    either models or endpoints, and returns them as a list of strings. If the
    specified resource type is invalid, a ValueError is raised.
    If an error occurs during fetching, it prints an error message and exits with
    a status code of 1.

    Args:
        resource_type (str): The type of resource to fetch.
            Either "Model" or "Endpoint".
        sagemaker_client (Any): The client to use
            for fetching resources.
        max_results (int): The maximum number of
            results to return. Defaults to 99.

    Returns:
        list[str]: A list of strings representing the names of the deployed resources.

    Raises:
        ValueError: If the specified resource type is not "Model" or "Endpoint".
    """
    try:
        loader_thread = start_loader(
            message=f"Fetching deployed {resource_type}s...", color="green"
        )
        if resource_type == "Model":
            response = sagemaker_client.list_models(MaxResults=max_results)
        elif resource_type == "Endpoint":
            response = sagemaker_client.list_endpoints(MaxResults=max_results)
        else:
            raise ValueError("Invalid resource type")
        stop_loader(loader_thread)
        resources = [
            item[f"{resource_type}Name"] for item in response[resource_type + "s"]
        ]

        if not resources:
            click.secho(f"No {resource_type}s have been deployed so far. \n", fg="red")

        return resources

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(f"An error occurred while fetching {resource_type}s: {e}", fg="red")
        exit(1)
