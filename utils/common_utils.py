""" Utilities common to all steps """
from git_utils import RepoWrapper
import logging
import subprocess
from os import access, chmod, W_OK, devnull, remove
from os.path import exists
from stat import S_IWUSR
from shutil import rmtree as shutil_rmtree
from sys import version_info


def create_component(device, branch, path, action, commit_message, epics=False, **kwargs):
    """
    Creates part of the IBEX device support
    :param device: Name of the device used in the action
    :param branch: Branch name to put the changes on
    :param path: Path to the repository
    :param action: Function that takes the device as an argument that creates the component
    :param commit_message: Message to attach to the changes
    :param epics: Is this change to the main EPICS repo?
    """
    try:
        repo = RepoWrapper(path)
        repo.prepare_new_branch(branch, epics)
        action(device, **kwargs)
        repo.push_all_changes(commit_message)
    except (RuntimeError, IOError) as e:
        logging.error(str(e))
        return
    except RuntimeWarning as e:
        logging.warning(str(e))
    except Exception as e:
        logging.error("Encountered unknown error: {}".format(e))
        return


def run_command(command, working_dir):
    """
    Runs a command using subprocess. Waits for completion
    :param command: A list defining the command to run
    :param working_dir: The directory to run the command in
    """
    logging.info("Running command: {}".format(" ".join(command)))
    with open(devnull, 'w') as null_out:
        cmd = subprocess.Popen(command, cwd=working_dir, stdout=null_out, stderr=subprocess.STDOUT,
                               stdin=subprocess.PIPE)
    cmd.wait()


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
    shutil_rmtree(delete_path, onerror=onerror)


def get_input(prompt):
    """
    Standard input function to use which will adapt based on Python version

    :param prompt: Text to display to the user
    :return: Input from prompt
    """
    return input(prompt) if version_info[0] >= 3 else raw_input(prompt)


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
        mkdir(path)
    except OSError as e:
        raise OSError("Unable to create directory {}: {}".format(path, e))


def copy_file(src, dst):
    """
    Copy a file from one place to another
    :param src: Place to copy from
    :param dst: Place to copy to
    """
    if exists(dst):
        if get_input("{} already exists. Shall I try and delete it? (Y/N) ".format(dst)).upper() == "Y":
            remove(dst)
        else:
            raise OSError("File {} already exists. Aborting".format(dst))
    try:
        copy_file(src, dst)
    except OSError as e:
        raise OSError("Unable to copy file from {} to {}: {}".format(src, dst, e))