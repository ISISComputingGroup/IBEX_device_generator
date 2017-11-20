""" Utilities common to all steps """
from git_utils import RepoWrapper
import logging


def create_component(device, branch, path, action, commit_message):
    """
    Creates part of the IBEX device support
    :param device: Name of the device used in the action
    :param branch: Branch name to put the changes on
    :param path: Path to the repository
    :param action: Function that takes the device as an argument that creates the component
    :param commit_message: Message to attach to the changes
    """
    try:
        repo = RepoWrapper(path)
        repo.prepare_new_branch(branch)
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
