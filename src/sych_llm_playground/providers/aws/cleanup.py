"""Module for cleaning up deployed resources on AWS.

This module provides functions to delete deployed resources such as models
and endpoints from the cloud. It includes functions to
select resources and initiate their cleanup.

Functions:
    choose_resource: Helps the user select a resource for deletion.
    cleanup_resource: Deletes the selected resource.
    cleanup: Main function for cleaning up resources.
"""

from typing import Any
from typing import cast

import boto3
import click
import inquirer

from ...utils.loader import start_loader
from ...utils.loader import stop_loader
from .utils.credentials import load_credentials
from .utils.resources import get_resources


def choose_resource(resource_type: str, sagemaker_client: Any) -> str:
    """Choose a specific resource for cleanup from AWS.

    This function lists the available resources of the specified type and prompts
    the user to select one for deletion.

    Args:
        resource_type (str): The type of resource to delete (e.g., "Model", "Endpoint").
        sagemaker_client (Any): The client to use to interact with AWS SageMaker.

    Returns:
        str: The name of the selected resource.
    """
    resources = get_resources(resource_type, sagemaker_client)
    if len(resources) == 0:
        exit(0)

    questions = [
        inquirer.List(
            resource_type.lower(),
            message=f"Select a {resource_type.lower()} to cleanup:",
            choices=resources,
        ),
    ]

    answers = inquirer.prompt(questions)
    return cast(str, answers[resource_type.lower()])


def cleanup_resource(resource_type: str) -> None:
    """Delete a selected resource from AWS.

    This function deletes a selected resource of the given type, either a model
    or an endpoint. It manages the deletion process, including error handling
    and success messaging.

    Args:
        resource_type (str): The type of resource to delete (e.g., "Model", "Endpoint").
    """
    sagemaker_client = boto3.client("sagemaker")
    selected_resource = choose_resource(resource_type, sagemaker_client)

    try:
        loader_thread = start_loader(
            message=f"Deleting selected {resource_type.lower()}...", color="green"
        )
        if resource_type == "Model":
            sagemaker_client.delete_model(ModelName=selected_resource)
        elif resource_type == "Endpoint":
            sagemaker_client.delete_endpoint(EndpointName=selected_resource)
        stop_loader(loader_thread)

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(
            f"An error occurred while deleting {resource_type.lower()}s: {e}", fg="red"
        )
        exit(1)

    click.secho(
        f"{resource_type} {selected_resource} cleaned up successfully.", fg="green"
    )


def cleanup() -> None:
    """Main function for cleaning up AWS resources.

    This function is the main function to remove deployed models
    and endpoints from AWS. It loads credentials,
    asks the user what they'd like to clean up,
    and then calls the appropriate cleanup function.
    """
    load_credentials()

    questions = [
        inquirer.List(
            "cleanup_options",
            message="What would you like to cleanup?",
            choices=[
                "Model",
                "Endpoint",
            ],
        ),
    ]

    answers = inquirer.prompt(questions)
    selected_option = answers["cleanup_options"]

    if selected_option == "Model":
        cleanup_resource("Model")
    elif selected_option == "Endpoint":
        cleanup_resource("Endpoint")
