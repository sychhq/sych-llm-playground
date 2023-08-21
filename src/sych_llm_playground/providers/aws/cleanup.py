"""Module for cleaning up deployed resources on AWS.

This module provides functions to delete deployed resources such as models,
endpoints, and API Gateways from the cloud. It includes functions to
select resources and initiate their cleanup.

Functions:
    choose_resource: Helps the user select a resource for deletion.
    cleanup_resource: Deletes the selected resource.
    cleanup: Main function for cleaning up resources.
"""

import boto3
import click
import inquirer

from ...utils.loader import start_loader
from ...utils.loader import stop_loader
from .utils.credentials import load_credentials
from .utils.resources import choose_resource


def cleanup_resource(resource_type: str) -> None:
    """Delete a selected resource from AWS.

    This function deletes a selected resource of the given type, either a model,
    an endpoint, or an API Gateway. It manages the deletion process,
    including error handling and success messaging.

    Args:
        resource_type (str): The type of resource to delete
            (e.g., "Model", "Endpoint", "API Gateway").
    """
    client = (
        boto3.client("sagemaker")
        if resource_type != "API Gateway"
        else boto3.client("apigateway")
    )
    selected_resource = choose_resource(resource_type, client, "cleanup")

    try:
        loader_thread = start_loader(
            message=f"Deleting selected {resource_type.lower()}...", color="green"
        )
        if resource_type == "Model":
            client.delete_model(ModelName=selected_resource["name"])
        elif resource_type == "Endpoint":
            client.delete_endpoint(EndpointName=selected_resource["name"])
        elif resource_type == "API Gateway":
            client.delete_rest_api(restApiId=selected_resource["id"])
        stop_loader(loader_thread)

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(
            f"An error occurred while deleting {resource_type.lower()}s: {e}", fg="red"
        )
        exit(1)

    click.secho(f"{resource_type} cleaned up successfully. \n", fg="green")


def cleanup() -> None:
    """Main function for cleaning up AWS resources.

    This function is the main function to remove deployed models,
    endpoints, and API Gateways from AWS. It loads credentials,
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
                "API Gateway",
            ],
        ),
    ]

    answers = inquirer.prompt(questions)
    selected_option = answers["cleanup_options"]

    cleanup_resource(selected_option)
