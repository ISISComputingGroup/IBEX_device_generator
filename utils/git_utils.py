"""
Utilities for interacting with Git. This is largely done via the command line because it's simpler and easier
to maintain than the PythonGit API.
"""
from git import Repo, GitCommandError, InvalidGitRepositoryError


class Repo(object):
    """
    A wrapper around a git repository
    """
    def __init__(self, path):
        """
        :param path: The path to the git repository
        """
        try:
            self._repo = Repo(path)
        except InvalidGitRepositoryError:
            self._repo = Repo.init(path)
        except Exception:
            raise RuntimeError("Unable to attach to git repository at path {}".format(path))

    def prepare_new_branch(self, name):
        """
        :param name: Name of the new branch
        """
        try:
            self._repo.git.stash('save')
            self._repo.git.reset("HEAD", hard=True)
            self._repo.git.clean(f=True, d=True, x=True)
            self._repo.git.checkout("master", force=True)
            self._repo.git.pull()
            self._repo.git.checkout(name, force=True)
            self._repo.git.push("origin", name, set_upstream=True)
        except GitCommandError as e:
            raise RuntimeError("Error whilst executing git command, {}".format(e.message))