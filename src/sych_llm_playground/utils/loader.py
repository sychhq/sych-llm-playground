"""This module contains utility functions to create a loader animation in the terminal.

Functions:
    - loader: A function that displays a loading animation.
    - start_loader: Starts the loading animation in a new thread.
    - stop_loader: Stops the loading animation and clears the terminal line.

The loading animation can be customized with different messages and colors.

Example:
    loader_thread = start_loader(message="Fetching data...", color="green")
    # Perform some operation...
    stop_loader(loader_thread)

Note:
    The `loading` variable is used to control the state of the loader (start/stop).
"""

import shutil
import threading
import time

import click


loading = False


def loader(message: str, color: str) -> None:
    """Display a loading animation using a sequence of characters.

    Args:
        message (str): The message to display alongside the animation.
        color (str): The text color for the message.
    """
    chars = "|/-\\"
    colored_message = click.style(message, fg=color)
    while loading:
        for char in chars:
            click.echo("\r" + colored_message + " " + char, nl=False)
            time.sleep(0.1)


def start_loader(message: str = "Loading...", color: str = "cyan") -> threading.Thread:
    """Start the loading animation in a new thread.

    Args:
        message (str): The message to display
            alongside the animation. Defaults to "Loading...".
        color (str): The text color for the message.
            Defaults to "cyan".

    Returns:
        threading.Thread: The thread running the loading animation.
    """
    global loading
    loading = True
    t = threading.Thread(target=loader, args=(message, color))
    t.start()
    return t


def stop_loader(thread: threading.Thread) -> None:
    """Stop the loading animation and clear the terminal line.

    Args:
        thread (threading.Thread): The thread running the loading animation.
    """
    global loading
    loading = False
    thread.join()
    columns, _ = shutil.get_terminal_size()
    click.echo(
        "\r" + " " * columns, nl=False
    )  # Clear the loader with the exact number of spaces
    click.echo("\n", nl=False)
