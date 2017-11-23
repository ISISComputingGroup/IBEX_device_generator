""" Utilities for interacting with the file system """
import logging
from os import access, chmod, W_OK, remove
from os.path import exists, join
from os import mkdir as mkdir_external
from stat import S_IWUSR
from shutil import rmtree as rmtree_external
from shutil import copyfile as copyfile_external
from shutil import copytree as copytree_external
from command_line_utils import get_input


def replace_in_file(target, substitutions):
    """
    Replaces matching content in a file

    :param target: Path to file where we are going to make substitutions
    :param substitutions: A collection of substitutions to make. Each substitution should be in the form
    (original, final)
    """
    logging.info("Making substitutions into file {}: {}".format(target, substitutions))
    with open(target) as f:
        lines = f.readlines()

    def substitute(input_str):
        """
        :param input_str: The original string
        :return: The original string after substitutions have beeen made
        """
        output_str = input_str
        for s in substitutions:
            output_str = output_str.replace(s[0], s[1])
        return output_str

    with open(target, "w") as f:
        f.writelines(substitute(line) for line in lines)


def rmtree(delete_path):
    """
    Enhanced version of shutil rmtree that can cope with windows permission issues

    :param delete_path: The directory to the path to delete
    """
    logging.info("Deleting folder {}".format(delete_path))

    def onerror(func, path, exc_info):
        """
        Error handler for ``shutil.rmtree``.

        If the error is due to an access error (read only file)
        it attempts to add write permission and then retries.

        If the error is for another reason it re-raises the error.

        :param func: Action taken on the path
        :param path: Path that is being manipulated
        :param exc_info: Whether to log execution info
        """
        if not access(path, W_OK):  # Is the error an access error ?
            chmod(path, S_IWUSR)
            func(path)
        elif exc_info:
            raise OSError("Unable to delete file at {}".format(path))
    rmtree_external(delete_path, onerror=onerror)


def mkdir(path):
    """
    :param path: The path to the dir to create
    :return:
    """
    if exists(path):
        if get_input("{} already exists. Shall I try and delete it? (Y/N) ".format(path)).upper() == "Y":
            rmtree(path)
        else:
            raise OSError("Directory {} already exists. Aborting".format(path))
    try:
        mkdir_external(path)
    except OSError as e:
        raise OSError("Unable to create directory {}: {}".format(path, e))


def copy_file(src, dst):
    """
    Copy a file from one place to another
    :param src: Place to copy from
    :param dst: Place to copy to
    """
    _copy(src, dst, remove, copyfile_external)


def copy_tree(src, dst):
    """
    Copy a folder from one place to another
    :param src: Place to copy from
    :param dst: Place to copy to
    """
    _copy(src, dst, rmtree, copytree_external)


def _copy(src, dst, remove_func, copy_func):
    """
    :param src: Place to copy from
    :param dst: Place to copy to
    :param copy_func: External function to perform copy
    :param remove_func: External function to perform remove
    """
    if exists(dst):
        if get_input("{} already exists. Shall I try and delete it? (Y/N) ".format(dst)).upper() == "Y":
            remove_func(dst)
        else:
            raise OSError("File {} already exists. Aborting".format(dst))
    try:
        copy_func(src, dst)
    except OSError as e:
        raise OSError("Unable to copy from {} to {}: {}".format(src, dst, e))


def add_to_makefile_list(directory, list_name, entry):
    """
    Adds an entry to a list in a makefile. Finds the last line of the form "list_name += ..." and puts a new line
    containing the entry after it

    :param directory: Directory containing the makefile
    :param list_name: The name of the list in the makefile to append to
    :param entry: The entry to add to the list
    """
    logging.info("Adding {} to list {} in Makefile for directory {}".format(entry, list_name, directory))
    makefile = join(directory, "Makefile")
    with open(makefile) as f:
        old_lines = f.readlines()
    new_lines = []
    last_line = ""
    marker = "{} += ".format(list_name)
    for line in old_lines:
        if marker in last_line and marker not in line:
            new_lines.append(marker + entry)
        new_lines.append(line)

    with open(makefile, "w") as f:
        f.writelines(new_lines)
