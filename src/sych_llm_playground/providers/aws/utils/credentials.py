"""This module provides utility functions for managing AWS cloud credentials.

It includes functionality for:

    - Validating the presence and completeness of required credential keys.
    - Loading credentials into environment variables.
    - Saving credentials to a file.
    - Retrieving existing credentials from a file.

It uses a specific file format and location defined by the `CREDENTIALS_FILE` constant.

Example:
    # Load the credentials into the environment
    credentials = load_credentials()

    # Save new credentials
    save_credentials(new_credentials)

    # Validate if credentials are present and correct
    is_valid = validate_credentials()
"""

import os
from typing import Dict

import click


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "providers", "aws", ".credentials")


def validate_credentials() -> bool:
    """Validates that the required keys are present in the credentials file.

    Returns:
        bool: True if all required keys are present and not empty, False otherwise.
    """
    required_keys = ["access_key", "secret_key", "role_arn", "region"]

    if not os.path.exists(CREDENTIALS_FILE):
        click.secho(
            "CLI credentials have not been configured. "
            + "Please run the configure command to do so. \n",
            fg="red",
        )
        return False

    credentials = {}
    with open(CREDENTIALS_FILE) as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            credentials[key] = value

    for key in required_keys:
        if key not in credentials or not credentials[key].strip():
            click.secho(f"{key} is missing or empty in the credentials file.", fg="red")
            return False

    click.secho("\n✓ Cloud Credentials validated.", fg="green")
    return True


def load_credentials() -> Dict[str, str]:
    """Loads the credentials from the file.

    Returns:
        Dict[str, str]: A dictionary containing the loaded credentials.
    """
    if not validate_credentials():
        exit(1)

    credentials = {}
    with open(CREDENTIALS_FILE) as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            credentials[key] = value

    os.environ["AWS_ACCESS_KEY_ID"] = credentials["access_key"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials["secret_key"]
    os.environ["AWS_DEFAULT_REGION"] = credentials["region"]

    click.secho(" \n✓ Cloud Credentials loaded. \n", fg="green")

    return credentials


def save_credentials(credentials: Dict[str, str]) -> None:
    """Saves the given credentials to the file.

    Args:
        credentials (Dict[str, str]): A dictionary
            containing the credentials to be saved.
    """
    with open(CREDENTIALS_FILE, "w") as f:
        for key, value in credentials.items():
            f.write(f"{key}={value}\n")


def existing_credentials() -> Dict[str, str]:
    """Retrieves the existing credentials from the file.

    Returns:
        Dict[str, str]: A dictionary containing the
        existing credentials, or an empty dictionary if no
        credentials are found.
    """
    credentials = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE) as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                credentials[key] = value
    return credentials
