"""This module provides functions to interact with deployed models on AWS.

It includes functionality to list available endpoints, make predictions,
and facilitate a chat interaction with a model.
"""

import json
import re

import boto3
import click
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer

from ...utils.loader import start_loader
from ...utils.loader import stop_loader
from .utils.credentials import load_credentials
from .utils.resources import choose_resource


def predict(selected_endpoint: str) -> None:
    """Make a prediction using the selected endpoint and display the results.

    Args:
        selected_endpoint (str): The name of the selected endpoint.
    """
    click.echo("\n")

    max_new_tokens = (
        input(click.style("Your desired Max new tokens? (default 256): ", fg="blue"))
        or 256
    )
    top_p = input(click.style("Your desired top_p? (default 0.9): ", fg="blue")) or 0.9
    temperature = (
        input(click.style("Your desired Temperature? (default 0.6): ", fg="blue"))
        or 0.6
    )

    user_input = ""
    while not user_input.strip():
        user_input = input(
            click.style(
                "Your Input (e.g., 'I believe the meaning of life is'): ",
                fg="blue",
            )
        )

    try:
        loader_thread = start_loader(
            message="Waiting for Model response...", color="green"
        )

        predictor = Predictor(endpoint_name=selected_endpoint)
        predictor.serializer = JSONSerializer(content_type="application/json")

        payload = {
            "inputs": user_input,
            "parameters": {
                "max_new_tokens": int(max_new_tokens),
                "top_p": float(top_p),
                "temperature": float(temperature),
            },
        }

        response_bytes = predictor.predict(
            payload, custom_attributes="accept_eula=true"
        )
        stop_loader(loader_thread)

        response_string = response_bytes.decode("utf-8")
        response_json = json.loads(response_string)
        content = response_json[0]["generation"]

        click.secho("Model Output: ", fg="green", nl=False)
        click.secho(content, fg="white")
        click.secho("\n", nl=False)

    except Exception as e:
        stop_loader(loader_thread)
        click.secho(f"An error occurred during prediction: {e}", fg="red")
        exit(1)


def chat(selected_endpoint: str) -> None:
    """Initiate a chat interaction with the selected endpoint.

    Args:
        selected_endpoint (str): The name of the selected endpoint.
    """
    click.echo("\n")

    system_instruction = input(
        click.style(
            "Provide a system instruction to guide the model's "
            + "behavior (optional, e.g., 'Please talk in riddles.'): ",
            fg="blue",
        )
    )

    max_new_tokens = (
        input(click.style("Your desired Max new tokens? (default 256): ", fg="blue"))
        or 256
    )
    top_p = input(click.style("Your desired top_p? (default 0.9): ", fg="blue")) or 0.9
    temperature = (
        input(click.style("Your desired Temperature? (default 0.6) : ", fg="blue"))
        or 0.6
    )

    conversation_history = []
    if system_instruction.strip():
        conversation_history.append({"role": "system", "content": system_instruction})

    click.secho("\nType 'exit' to end the chat.\n", fg="yellow")

    exit_chat = False
    while True:
        user_input = ""
        while not user_input.strip():
            user_input = input(click.style("You: ", fg="blue"))
            if user_input.lower() == "exit":
                click.secho("Exiting chat...", fg="yellow")
                exit_chat = True
                break

        if exit_chat:
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            loader_thread = start_loader(
                message="Waiting for Model response...", color="green"
            )

            predictor = Predictor(endpoint_name=selected_endpoint)
            predictor.serializer = JSONSerializer(content_type="application/json")

            payload = {
                "inputs": [conversation_history],
                "parameters": {
                    "max_new_tokens": int(max_new_tokens),
                    "top_p": float(top_p),
                    "temperature": float(temperature),
                },
            }

            response_bytes = predictor.predict(
                payload, custom_attributes="accept_eula=true"
            )
            stop_loader(loader_thread)

            response_string = response_bytes.decode("utf-8")
            response_json = json.loads(response_string)
            content = response_json[0]["generation"]["content"]

            # Add the assistant's response to the conversation history
            conversation_history.append({"role": "assistant", "content": content})

            click.secho("Model: ", fg="green", nl=False)
            click.secho(content, fg="white")
            click.secho("\n", nl=False)

        except Exception as e:
            stop_loader(loader_thread)
            click.secho(f"An error occurred during prediction: {e}", fg="red")
            exit(1)

    click.secho("Chat ended. \n", fg="yellow")


INTERACTION_FUNCTIONS = {
    "meta-textgeneration-llama-2-7b": predict,
    "meta-textgeneration-llama-2-7b-f": chat,
    "meta-textgeneration-llama-2-13b": predict,
    "meta-textgeneration-llama-2-13b-f": chat,
    "meta-textgeneration-llama-2-70b": predict,
    "meta-textgeneration-llama-2-70b-f": chat,
}


def interact() -> None:
    """Main function to interact with deployed models on AWS.

    Loads credentials, allows the user to choose an endpoint, and then facilitates
    either prediction or chat interaction based on the selected endpoint.
    """
    load_credentials()

    sagemaker_client = boto3.client("sagemaker")
    selected_endpoint = choose_resource("Endpoint", sagemaker_client, "interact")
    selected_endpoint_name = selected_endpoint["name"]

    # Extract the model ID from the endpoint name using a regular expression
    match = re.match(r"^sych-llm-pg-(.*?)-e-", selected_endpoint_name)
    if match:
        model_id = match.group(1)
        interaction_function = INTERACTION_FUNCTIONS.get(model_id)
        if interaction_function:
            interaction_function(selected_endpoint_name)
        else:
            click.secho(
                f"The model {model_id!r} is not currently supported. \n",
                fg="red",
            )
            exit(1)
    else:
        click.secho(
            f"""The endpoint {selected_endpoint_name!r} does not match
            any supported models. \n""",
            fg="red",
        )
        exit(1)
