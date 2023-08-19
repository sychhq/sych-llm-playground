"""Utility module for selecting cloud providers.

This module provides functions to prompt the user for their preferred cloud provider
and call the corresponding function based on the parent caller.

Functions:
    select_provider_and_call_function: Prompts the user to select
        a provider and then call the corresponding function.
"""

from importlib import import_module
from typing import Any

import inquirer


def select_provider_and_call_function(caller_function_name: str) -> None:
    """Prompt the user to select a cloud provider and call the corresponding function.

    Args:
        caller_function_name (str): The name of the calling
            function (e.g., "deploy", "configure").
    """
    questions = [
        inquirer.List(
            "provider",
            message="Please choose a provider:",
            choices=["AWS"],
            carousel=True,
        ),
    ]

    answers = inquirer.prompt(questions)
    provider_choice = answers["provider"]

    # Mapping function names to their respective modules
    functions_mapping = {
        "AWS": {
            "configure": "providers.aws.configure.configure",
            "deploy": "providers.aws.deploy.deploy",
            "list": "providers.aws.list.list",
            "interact": "providers.aws.interact.interact",
            "cleanup": "providers.aws.cleanup.cleanup",
        },
    }

    module_path = functions_mapping[provider_choice][caller_function_name]
    function_to_call = _dynamic_import(module_path)
    function_to_call()


def _dynamic_import(module_path: str) -> Any:
    """Dynamically import a module from a given module path.

    Args:
        module_path (str): The module path
            (e.g., "providers.aws.configure.aws_configure").

    Returns:
        (Any): The imported function.
    """
    full_module_path = "sych_llm_playground." + module_path
    module_name, function_name = full_module_path.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, function_name)
