""" Utilities for running scripts from the command line """
import argparse


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
