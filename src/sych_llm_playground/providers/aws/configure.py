"""Module for AWS cloud credential configuration.

This module provides functions and a CLI command to set up for the Playground with AWS.
The user is prompted to provide AWS-specific cloud credentials.

Functions:
    aws_configure: Main function to orchestrate the AWS configuration process.
"""

from typing import Dict

import click

from .utils.credentials import existing_credentials
from .utils.credentials import save_credentials


def prompt_for_aws_credentials(existing_credentials: Dict[str, str]) -> Dict[str, str]:
    """Prompt the user for AWS cloud credentials.

    Args:
        existing_credentials (Dict[str, str]): Existing credentials that may
            be used as defaults.

    Returns:
        Dict[str, str]: A dictionary containing the user's credentials.
    """
    credentials = {}
    prompts = [
        (
            "access_key",
            "Please Provide your AWS Access Key",
            True,
            "bright_yellow",
        ),
        (
            "secret_key",
            "Please provide your AWS Secret Key",
            True,
            "bright_yellow",
        ),
        (
            "role_arn",
            "Please provide your ARN of the IAM role for SageMaker",
            True,
            "bright_yellow",
        ),
        (
            "region",
            "Please provide the AWS Region you want to deploy in",
            False,
            "bright_cyan",
        ),
    ]
    default_values = {"region": "us-west-2"}  # You can set default values here
    for (
        key,
        prompt,
        required,
        color,
    ) in prompts:
        while True:  # Keep asking until a valid input is given
            default_value = existing_credentials.get(key, default_values.get(key, ""))
            value = click.prompt(
                click.style(prompt, fg=color),
                default=default_value if not required else None,
                show_default=not required,
                hide_input=(key == "secret_key"),
            )
            if value or not required:
                credentials[key] = value
                break
    return credentials


def configure() -> None:
    """Configure AWS cloud credentials for the Playground.

    This function prompts the user for AWS cloud credentials.
    If existing credentials are found, the user is asked if they want to use them.
    Once the credentials are set, they are saved using the `save_credentials` function.
    """
    existing_creds = existing_credentials()
    if existing_creds:
        use_existing = click.confirm(
            click.style(
                "We found saved AWS credentials. Do you want to use them?",
                fg="bright_magenta",
            ),
            default=True,
        )

        if use_existing:
            credentials = existing_creds
        else:
            credentials = prompt_for_aws_credentials(existing_creds)
    else:
        credentials = prompt_for_aws_credentials({})

    save_credentials(credentials)

    click.secho("AWS Configuration successful! \n", fg="green")
