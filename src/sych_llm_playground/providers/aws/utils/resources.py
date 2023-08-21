"""Utility module for fetching specific AWS resources.

This module contains functions to get deployed cloud resources
such as models and endpoints, and api gateways.
"""

import os
from typing import Any
from typing import Dict
from typing import List

import click
import inquirer

from ....utils.loader import start_loader
from ....utils.loader import stop_loader


def choose_resource(resource_type: str, client: Any, purpose: str) -> Dict[str, Any]:
    """Choose a specific resource from AWS for an purpose.

    This function lists the available resources of the specified type and prompts
    the user to select one with an purpose message.

    Args:
        resource_type (str): The type of resource to choose
            (e.g., "Model", "Endpoint", "API Gateway").
        client (Any): The client to use to interact with AWS.
        purpose (str): The purpose to choose a resource, e.g. interact.

    Returns:
        dict: The dictionary of the selected resource.
    """
    resources = get_resources(resource_type, client)

    if len(resources) == 0:
        exit(0)

    choices = [resource["name"] for resource in resources]
    questions = [
        inquirer.List(
            resource_type.lower(),
            message=f"Select a {resource_type.lower()} to {purpose}:",
            choices=choices,
        ),
    ]

    answers = inquirer.prompt(questions)
    selected_name = answers[resource_type.lower()]
    selected_resource = next(
        resource for resource in resources if resource["name"] == selected_name
    )

    return selected_resource


def get_resources(
    resource_type: str, client: Any, max_results: int = 99
) -> List[Dict[str, str]]:
    """Fetch deployed AWS resources based on resource type.

    This function retrieves specified resource including models,
    endpoints, or API Gateways, returning them as a list of
    dictionaries. Raises ValueError if resource type is invalid.
    Prints error message and exits with status code 1 if an
    error occurs during fetching.

    Args:
        resource_type (str): Type of resource, either "Model",
            "Endpoint", or "API Gateway".
        client (Any): Client to use for fetching resources.
        max_results (int): Max number of results, default 99.

    Returns:
        list[dict[str, str]]: List of dictionaries representing
            deployed resources.

    Raises:
        ValueError: If the provided resource_type is invalid.
    """
    try:
        loader_thread = start_loader(
            message=f"Fetching deployed {resource_type}s...", color="green"
        )
        region = os.environ["AWS_DEFAULT_REGION"]
        resources = []

        if resource_type == "Model":
            response = client.list_models(MaxResults=max_results)
            resources = [{"name": item["ModelName"]} for item in response["Models"]]

        elif resource_type == "Endpoint":
            response = client.list_endpoints(MaxResults=max_results)
            for item in response["Endpoints"]:
                url = (
                    f"https://runtime.sagemaker.{region}"
                    f".amazonaws.com/endpoints/"
                    f"{item['EndpointName']}/invocations"
                )
                resources.append({"name": item["EndpointName"], "url": url})

        elif resource_type == "API Gateway":
            response = client.get_rest_apis()
            for item in response["items"]:
                url = (
                    f"https://{item['id']}.execute-api."
                    f"{region}.amazonaws.com/prod/predict"
                )
                resources.append(
                    {
                        "name": item["name"],
                        "id": item["id"],
                        "method": "POST",
                        "url": url,
                    }
                )

        else:
            raise ValueError("Invalid resource type")

        stop_loader(loader_thread)

        if not resources:
            click.secho(f"No {resource_type}s deployed so far.\n", fg="red")

        return resources

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(f"Error fetching {resource_type}s: {e}", fg="red")
        exit(1)
