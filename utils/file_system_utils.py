""" Utilities for interacting with the file system """
import logging
from os import access, chmod, W_OK, remove
from os.path import exists, join
from os import makedirs
from stat import S_IWUSR
from shutil import rmtree as rmtree_external
from shutil import copyfile as copyfile_external
from shutil import copytree as copytree_external
from utils.command_line_utils import ask_do_step


def replace_in_file(target, substitutions):
    """
    Replaces matching content in a file

    Args:
        target: Path to file where we are going to make substitutions
        substitutions: A collection of substitutions to make. Each substitution should be in the form
        (original, final)
    """
    logging.info("Making substitutions into file {}: {}".format(target, substitutions))
    with open(target) as f:
        lines = f.readlines()

    def substitute(input_str):
        """
        Args:
            input_str: The original string

        Returns:
            The original string after substitutions have beeen made
        """
        output_str = input_str
        for s in substitutions:
            output_str = output_str.replace(s[0], s[1])
        return output_str

    with open(target, "w") as f:
        f.writelines(substitute(line) for line in lines)

def append_to_file(target, newlines):
    with open(target, "a") as f:
        f.writelines(newlines)


def rmtree(delete_path):
    """
    Enhanced version of shutil rmtree that can cope with windows permission issues

    Args:
        delete_path: The directory to the path to delete
    """
    logging.info("Deleting folder {}".format(delete_path))

    def onerror(func, path, exc_info):
        """
        Error handler for ``shutil.rmtree``.

        If the error is due to an access error (read only file)
        it attempts to add write permission and then retries.

        If the error is for another reason it re-raises the error.

        Args:
            func: Action taken on the path
            path: Path that is being manipulated
            exc_info: Whether to log execution info
        """
        if not access(path, W_OK):  # Is the error an access error ?
            chmod(path, S_IWUSR)
            func(path)
        elif exc_info:
            raise OSError("Unable to delete file at {}".format(path))
    rmtree_external(delete_path, onerror=onerror)


def mkdir(path):
    """
    Args:
        path: The path to the dir to create
    """
    try:
        makedirs(path)

    except OSError:
        if ask_do_step("{} already exists. Delete its contents and make it an empty directory?".format(path)):
            rmtree(path)
            mkdir(path)
        # Else do nothing if the dir exists and the user requests no deletion

def touch(path, filename):
    """
    Create an empty file in a given path with the given name.
    Args:
        path: Path to create file in.
        filename: The filename to create.
    """
    open(join(path, filename), 'a').close()


def copy_file(src, dst):
    """
    Copy a file from one place to another
    
    Args:
        src: Place to copy from
        dst: Place to copy to
    """
    _copy(src, dst, remove, copyfile_external)


def copy_tree(src, dst):
    """
    Copy a folder from one place to another
    
    Args:
        src: Place to copy from
        dst: Place to copy to
    """
    _copy(src, dst, rmtree, copytree_external)


def _copy(src, dst, remove_func, copy_func):
    """
    Args:
        src: Place to copy from
        dst: Place to copy to
        copy_func: External function to perform copy
        remove_func: External function to perform remove
    """
    if exists(dst):
        if ask_do_step("{} already exists. Delete it?".format(dst)):
            remove_func(dst)
        else:
            raise OSError("File {} already exists. Aborting".format(dst))
    try:
        copy_func(src, dst)
    except OSError as e:
        raise OSError("Unable to copy from {} to {}: {}".format(src, dst, e))


def _add_entry_to_list(text, list_name, entry):
    """
    Check if IOC name has already been added to support/Makefile or ioc/master/Makefile, 
    and add it at the end of IOC | SUPP DIRS list if it isn't there already.

    Args:
        text: The original text
        list_name: The name of the list to add to
        entry: The entry to add to the list

    Returns: The original text with the requested entry added to the named list

    """
    new_text = []
    last_line = ""
    marker = "{} += ".format(list_name)
    
    new_line = marker + entry + "\n"
    # Go to the end of the list of IOCDIRS/SUPPDIRS += iocname, and add our new IOC
    for line in text:
        if entry in line:
            # Entry already in the list
            logging.warn("IOC name already added to {}".format(list_name))
            return text
        elif marker in last_line and marker not in line:
            # We found the end of the list
            new_text.append(new_line)
        # Copy rest of the lines into new text as usual
        new_text.append(line)
        last_line = line
    return new_text # return Makefile with new entry


def add_to_makefile_list(directory, list_name, entry):
    """
    Adds an entry to a list in a makefile. Finds the last line of the form "list_name += ..." and puts a new line
    containing the entry after it
    
    Args:
        directory: Directory containing the makefile
        list_name: The name of the list in the makefile to append to
        entry: The entry to add to the list
    """
    logging.info("Adding {} to list {} in Makefile for directory {}".format(entry, list_name, directory))
    makefile = join(directory, "Makefile")
    with open(makefile) as f:
        old_lines = f.readlines()

    with open(makefile, "w") as f:
        f.writelines(_add_entry_to_list(old_lines, list_name, entry))
