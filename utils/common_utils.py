""" Utilities common to all steps """
from git_utils import RepoWrapper
from command_line_utils import ask_do_step
import logging
import subprocess
from os import devnull


def create_component(device, branch, path, action, commit_message, use_git, **kwargs):
    """
    Creates part of the IBEX device support
    
    Args:
        device: Name of the device used in the action
        branch: Branch name to put the changes on
        path: Path to the repository
        action: Function that takes the device as an argument that creates the component
        commit_message: Message to attach to the changes
        use_git: user git; False do not issue git commands
    """
    if not ask_do_step(commit_message):
        return

    repo = None
    try:
        if use_git:
            repo = RepoWrapper(path)
            repo.prepare_new_branch(branch)
            logging.warning("No git so branch not created or cleaned.")

        files_to_commit = action(device, **kwargs)

        if repo is not None:
            repo.push_changes(commit_message, files_to_commit=files_to_commit)
    except (RuntimeError, IOError) as e:
        logging.error(str(e))
    except RuntimeWarning as e:
        logging.warning(str(e))
    except Exception as e:
        logging.error("Encountered unknown error: {}".format(e))


def run_command(command, working_dir):
    """
    Runs a command using subprocess. Waits for completion

    Args:
        command: A list defining the command to run
        working_dir: The directory to run the command in
    """
    logging.info("Running command {} from {}".format(" ".join(command), working_dir))
    with open(devnull, 'w') as null_out:
        cmd = subprocess.Popen(command, cwd=working_dir, stdout=null_out, stderr=subprocess.STDOUT,
                               stdin=subprocess.PIPE)
    cmd.wait()
