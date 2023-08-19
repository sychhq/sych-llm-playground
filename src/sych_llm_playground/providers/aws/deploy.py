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

import time
from typing import Dict
from typing import List
from typing import Tuple

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
        {"id": "meta-textgeneration-llama-2-7b", "version": "2.0.0"},
    ),
    (
        "Llama-2-7b-chat - v1.1.0",
        {"id": "meta-textgeneration-llama-2-7b-f", "version": "1.1.0"},
    ),
    (
        "Llama-2-13b - v2.0.0",
        {"id": "meta-textgeneration-llama-2-13b", "version": "2.0.0"},
    ),
    (
        "Llama-2-13b-chat - v1.1.0",
        {"id": "meta-textgeneration-llama-2-13b-f", "version": "1.1.0"},
    ),
    (
        "Llama-2-70b - v1.1.0",
        {"id": "meta-textgeneration-llama-2-70b", "version": "1.1.0"},
    ),
    (
        "Llama-2-70b-chat v1.1.0",
        {"id": "meta-textgeneration-llama-2-70b-f", "version": "1.1.0"},
    ),
]

questions: List[inquirer.List] = [
    inquirer.List(
        "model", message="Select a model id to deploy:", choices=MODEL_CHOICES
    ),
]


def deploy() -> None:
    """Deploy the selected model to the cloud.

    This function prompts the user to select a model from the predefined
    list. After selecting the model, it handles the deployment process,
    It also manages error handling and success messaging. If an error
    occurs during deployment, it prints an error message and exits with
    a status code of 1.
    """
    credentials = load_credentials()

    # Prompt the user to select a model from the list
    answers = inquirer.prompt(questions)
    model_id = answers["model"]["id"]
    model_version = answers["model"]["version"]

    timestamp = str(int(time.time()))
    model_name = f"sych-llm-pg-{model_id}-m-{timestamp}"
    endpoint_name = f"sych-llm-pg-{model_id}-e-{timestamp}"

    try:
        loader_thread = start_loader(
            message="Deploying... Why not grab a cup of coffee?", color="green"
        )

        # Deploy the model
        model = JumpStartModel(
            model_id=model_id,
            role=credentials["role_arn"],
            name=model_name,
            model_version=model_version,
        )
        predictor = model.deploy(endpoint_name=endpoint_name)
        print(f"Endpoint name: {predictor.endpoint_name}")

        stop_loader(loader_thread)

        click.secho("Deployment successful! \n", fg="green")

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(f"An error occurred during deployment: {e}", fg="red")
        exit(1)
