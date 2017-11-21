""" Utilities common to all steps """
from git_utils import RepoWrapper
import logging
import subprocess
from os import devnull


def create_component(device, branch, path, action, commit_message, epics=False):
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
        action(device)
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
    logging.info("Running command {} from {}".format(" ".join(command), working_dir))
    with open(devnull, 'w') as null_out:
        cmd = subprocess.Popen(command, cwd=working_dir, stdout=null_out, stderr=subprocess.STDOUT,
                               stdin=subprocess.PIPE)
    cmd.wait()
