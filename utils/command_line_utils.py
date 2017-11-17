""" Utilities for running scripts from the command line """
import argparse


class ArgumentDescriptor(object):
    """
    The description of an argument consumed by the argument parser
    """

    def __init__(self, name, input_type, help, default=None):
        """
        Bundles an argument for use by the argument parser
        :param name: Name of the argument
        :param input_type: Type of the argument
        :param help: Help text to display
        :param default: Default value
        :return: (name, type, help)
        """
        self.name = name
        self.type = input_type
        self.help = help
        self.default = default


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
        parser.add_argument("--{}".format(a.name), type=a.type, help=a.help, default=a.default)

    return parser.parse_args()
