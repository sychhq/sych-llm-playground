"""Main entry point for sych_llm_playground.

This module provides the main entry point for sych_llm_playground,
a command-line tool to manage and interact with language models in the cloud.
"""

import click

from .cleanup import cleanup
from .configure import configure
from .deploy import deploy
from .interact import interact
from .list import list


@click.group(
    help=(
        "sych-llm-playground is a command-line tool to manage and "
        "interact with language models on the cloud.\n\n"
        "Brought to you by Sych. Visit us at https://sych.io.\n\n"
        "Detailed documenation at "
        "https://sych-llm-playground.readthedocs.io"
    )  # Replace with your actual shortened URL
)
@click.version_option()
def main() -> None:
    """Main command-line interface function for sych_llm_playground."""
    pass


main.add_command(configure)
main.add_command(deploy)
main.add_command(list)
main.add_command(cleanup)
main.add_command(interact)

if __name__ == "__main__":
    main(prog_name="sych_llm_playground")  # pragma: no cover
