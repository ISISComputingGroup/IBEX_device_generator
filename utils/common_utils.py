""" Utilities common to all steps """
from git_utils import RepoWrapper


def create_component(device, branch, path, logger, action, commit_message):
    """
    Creates part of the IBEX device support
    :param device: Name of the device used in the action
    :param branch: Branch name to put the changes on
    :param path: Path to the repository
    :param logger: Logger to use for messages
    :param action: Function that takes the device as an argument that creates the component
    :param commit_message: Message to attach to the changes
    """
    try:
        repo = RepoWrapper(path)
        repo.prepare_new_branch(branch)
        action(device)
        repo.push_all_changes(commit_message)
    except (RuntimeError, IOError) as e:
        logger.error(str(e))
        return
    except Exception as e:
        logger.error("Encountered unknown error: {}".format(e))
        return
    except RuntimeWarning as e:
        logger.warning(str(e))