"""This module provides a CLI to deploy models to AWS Sagemaker.

It utilizes the `click` library to create a user-friendly CLI
and the `inquirer` library for interactive user input.
The available models, represented by the constant `MODEL_CHOICES`,
can be selected for deployment. The deployment process includes a loading
animation provided by the `start_loader` and `stop_loader` functions from
the `utils.loader` module.

Functions:
    deploy: Main function that orchestrates the deployment process.

Usage:
    The `deploy` command can be run via the CLI to deploy the selected
    model to the cloud. After selecting a model from the predefined
    choices, the script will handle the deployment, including error handling.

Models:
    Predefined models are provided in the `MODEL_CHOICES` list.

Dependencies:
    - click: Command Line Interface Creation Kit
    - inquirer: Asking for parameters through inquiry sessions
    - time: Standard library to handle time-related tasks
    - sagemaker.jumpstart.model: AWS SageMaker JumpStart Model deployment
    - .utils.loader: Utility functions for loading animations
    - .utils.credentials: Utility functions for loading credentials
"""

import os
import time
from typing import Dict
from typing import List
from typing import Tuple

import boto3
import click
import inquirer
from sagemaker.jumpstart.model import JumpStartModel

from ...utils.loader import start_loader
from ...utils.loader import stop_loader
from .utils.credentials import load_credentials


# List of supported supported models
MODEL_CHOICES: List[Tuple[str, Dict[str, str]]] = [
    (
        "Llama-2-7b - v2.0.0",
        {
            "id": "meta-textgeneration-llama-2-7b",
            "version": "2.0.0",
        },
    ),
    (
        "Llama-2-7b-chat - v1.1.0",
        {
            "id": "meta-textgeneration-llama-2-7b-f",
            "version": "1.1.0",
        },
    ),
    (
        "Llama-2-13b - v2.0.0",
        {
            "id": "meta-textgeneration-llama-2-13b",
            "version": "2.0.0",
        },
    ),
    (
        "Llama-2-13b-chat - v1.1.0",
        {
            "id": "meta-textgeneration-llama-2-13b-f",
            "version": "1.1.0",
        },
    ),
    (
        "Llama-2-70b - v1.1.0",
        {
            "id": "meta-textgeneration-llama-2-70b",
            "version": "1.1.0",
        },
    ),
    (
        "Llama-2-70b-chat v1.1.0",
        {
            "id": "meta-textgeneration-llama-2-70b-f",
            "version": "1.1.0",
        },
    ),
]

questions: List[inquirer.List] = [
    inquirer.List(
        "model",
        message="Select a model id to deploy:",
        choices=MODEL_CHOICES,
    ),
]


def create_api_gateway(endpoint_name: str, iam_role_arn: str) -> str:
    """Creates a REST API using AWS API Gateway for a specified SageMaker endpoint.

    This function performs tasks like creating the REST API, defining
    resources, methods, integration with the SageMaker endpoint, and
    deploying the API to the "prod" stage. It also handles specific
    headers and response codes mapping.

    :param endpoint_name: Name of the SageMaker endpoint.
    :param iam_role_arn: ARN of the IAM role with required permissions.
    :return: The URL of the deployed API, accessible via HTTPS POST.

    Note: The URL is in the format
    `https://<API-ID>.execute-api.<REGION>.amazonaws.com/prod/predict`.
    """
    region = os.environ["AWS_DEFAULT_REGION"]
    client = boto3.client("apigateway")

    from typing import Any
    from typing import Callable
    from typing import Optional

    def execute_task(
        start_message: str,
        color: str,
        action: Callable[[], Any],
        stop_message: Optional[str] = None,
    ) -> Any:
        """Executes a given task with a loading animation.

        Args:
            start_message (str): Message to display alongside
                the start of the loading animation.
            color (str): Text color for the loading animation.
            action (Callable[[], Any]): Function to execute.
                Takes no arguments, returns result.
            stop_message (Optional[str], optional): Message to
                display after stopping the loader. Defaults to None.

        Returns:
            Any: Result of executing the action.
        """
        try:
            loader_thread = start_loader(message=start_message, color=color)
            result = action()
            stop_loader(
                loader_thread,
                message=stop_message,
            )
            return result
        except Exception as e:
            stop_loader(
                loader_thread,
                message=stop_message,
            )
            click.secho(
                f"An error occurred: {e}",
                fg="red",
            )
            exit(1)

    api_id = execute_task(
        "Creating a REST API...",
        "green",
        lambda: client.create_rest_api(
            name=f"sych-llm-pg-api-{endpoint_name}",
            description="API for SageMaker endpoint " + endpoint_name,
        )["id"],
        "Created REST API",
    )

    root_resource_id = execute_task(
        "Fetching REST API...",
        "green",
        lambda: client.get_resources(restApiId=api_id,)["items"][
            0
        ]["id"],
        "Fetched REST API",
    )

    resource_id = execute_task(
        "Creating API resources...",
        "green",
        lambda: client.create_resource(
            restApiId=api_id,
            parentId=root_resource_id,
            pathPart="predict",
        )["id"],
        "Created API resources",
    )

    execute_task(
        "Creating a POST method...",
        "green",
        lambda: client.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="POST",
            authorizationType="NONE",
            requestParameters={
                # Header used to pass custom attributes to models.
                # Also required by Llama 2 to accept EULA.
                "method.request.header.custom_attributes": True
            },
        ),
        "Created a POST method",
    )

    execute_task(
        "Creating API integration with the Sagemaker endpoint...",
        "green",
        lambda: client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="POST",
            type="AWS",
            integrationHttpMethod="POST",
            uri=f"arn:aws:apigateway:{region}:runtime.sagemaker:path//endpoints/{endpoint_name}/invocations",
            credentials=iam_role_arn,
            passthroughBehavior="WHEN_NO_MATCH",
            # fmt: off
            requestParameters={
                # Sagemaker endpoints expect the X-Amzn-SageMaker-Custom-Attributes
                # header for custom_attributes. See:
                # https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_runtime_InvokeEndpoint.html
                "integration.request.header.X-Amzn-SageMaker-Custom-Attributes":
                    "method.request.header.custom_attributes"
            },
            # fmt: on
        ),
        "Created API Integration with SageMaker endpoint",
    )

    """Regex to map all possible response type to generic codes.
    e.g. any 2xx from the Sagemaker endpoint would be returned as 200
    by API Gateway. Ideally all response codes should be pass-through but
    API Gateway does not support it. We'd need to setup a lambda to
    do that which is additional infrastructure and cost.
    """
    status_code_patterns = {
        r".*2\d\d.*": "200",
        r".*3\d\d.*": "300",
        r".*4\d\d.*": "400",
        r".*5\d\d.*": "500",
    }

    # Define the method responses
    for _, status_code in status_code_patterns.items():

        def action_method_response(status_code: str = status_code) -> Any:
            return client.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod="POST",
                statusCode=status_code,
            )

        execute_task(
            f"Creating method response for {status_code}...",
            "green",
            action_method_response,
            "",
        )

    # Define the integration responses
    for pattern, status_code in status_code_patterns.items():

        def action_integration_response(
            status_code: str = status_code, pattern: str = pattern
        ) -> Any:
            return client.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod="POST",
                statusCode=status_code,
                selectionPattern=pattern,
                responseTemplates={"application/json": ""},
            )

        execute_task(
            f"Creating API integration response for {status_code}...",
            "green",
            action_integration_response,
            "",
        )

    execute_task(
        "Deploying the API...",
        "green",
        lambda: client.create_deployment(
            restApiId=api_id,
            stageName="prod",
        ),
        "API Deployed \n",
    )

    url = f"https://{api_id}.execute-api.{region}.amazonaws.com/prod/predict"
    click.secho(
        f"Public API HTTP (POST) URL: {url} \n",
        fg="yellow",
    )

    return url


def deploy() -> None:
    """Deploy the selected model to the cloud.

    This function prompts the user to select a model from the predefined
    list. After selecting the model, it handles the deployment process,
    It also manages error handling and success messaging. If an error
    occurs during deployment, it prints an error message and exits with
    a status code of 1.
    """
    credentials = load_credentials()

    # Prompt the user to select a model
    answers = inquirer.prompt(questions)
    model_id = answers["model"]["id"]
    model_version = answers["model"]["version"]

    timestamp = str(int(time.time()))
    model_name = f"sych-llm-pg-{model_id}-m-{timestamp}"
    endpoint_name = f"sych-llm-pg-{model_id}-e-{timestamp}"

    try:
        loader_thread = start_loader(
            message="Deploying... Why not grab a cup of coffee?",
            color="green",
        )

        # Deploy the model
        model = JumpStartModel(
            model_id=model_id,
            role=credentials["role_arn"],
            name=model_name,
            model_version=model_version,
        )
        predictor = model.deploy(endpoint_name=endpoint_name)
        stop_loader(
            loader_thread,
            "Model and Endpoint Deployed \n",
        )

        click.secho(
            f"Endpoint Name: {predictor.endpoint_name} \n",
            fg="yellow",
        )

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(
            f"An error occurred during deployment: {e}",
            fg="red",
        )
        exit(1)

    create_api_gateway(
        predictor.endpoint_name,
        credentials["role_arn"],
    )

    click.secho("Deployment successful! \n", fg="green")
