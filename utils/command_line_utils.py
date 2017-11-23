""" Utilities for running scripts from the command line """
import argparse
from sys import version_info, exit


def parse_args(description, arguments):
    """
    Parse the arguments for a script passed in at the command line
    :param description: Description of the script
    :param arguments: Collection of argument descriptors
    :return: A collection of argument
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=description)
    for a in arguments:
        if "default" not in a.keys():
            a["default"] = None
        parser.add_argument("--{}".format(a["name"]), type=a["type"], help=a["description"], default=a["default"])

    return parser.parse_args()


def get_input(prompt):
    """
    Standard input function to use which will adapt based on Python version

    :param prompt: Text to display to the user
    :return: Input from prompt
    """
    return input(prompt) if version_info[0] >= 3 else raw_input(prompt)


def ask_to_continue():
    """
    Ask the user whether the program should continue
    """
    if get_input("Should I continue (Y/N) ").upper() != "Y":
        exit(0)
