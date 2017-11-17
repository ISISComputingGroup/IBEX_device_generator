""" Utilities for modifying the gui for a new IOC """
from git_utils import Repo
from system_paths import CLIENT

def create_opi(name, branch):
    """

    :param name:
    :param branch:
    :return:
    """
    repo = Repo(CLIENT)
    repo.prepare_branch(branch)


