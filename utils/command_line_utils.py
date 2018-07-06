""" Utilities for running scripts from the command line """
import argparse
from sys import version_info


def get_input(prompt):
    """
    Standard input function to use which will adapt based on Python version

    Args:
        prompt: Text to display to the user

    Returns: Input from prompt
    """
    return input(prompt) if version_info[0] >= 3 else raw_input(prompt)


def ask_do_step(name):
    """
    Ask the user whether to do a step

    Args:
        name: Name of the step

    Returns: True or False on whether to perform the step
    """
    return get_input("Should I do step: {} (Y/N) ".format(name)).upper() == "Y"
