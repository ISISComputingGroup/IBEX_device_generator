"""
Utilities for interacting with Git. This is largely done via the command line because it's simpler and easier
to maintain than the PythonGit API.
"""
from git import Repo, GitCommandError, InvalidGitRepositoryError

# Do everything locally without pushing to remote repo
LOCAL = True

class RepoWrapper(object):
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

    def prepare_new_branch(self, branch):
        """
        :param branch: Name of the new branch
        """
        try:
            self._repo.git.stash('save')
            self._repo.git.reset("HEAD", hard=True)
            self._repo.git.clean(f=True, d=True)  # No -x. Some repos have file names too long in ignored dirs
            self._repo.git.checkout("master", force=True)
            self._repo.git.pull()
            branch_is_new = branch not in self._repo.branches
            self._repo.git.checkout(branch, b=branch_is_new)
            self._repo.git.checkout(branch)
            if not LOCAL:
                self._repo.git.push("origin", branch, set_upstream=True)
        except GitCommandError as e:
            raise RuntimeError("Error whilst executing preparing git branch, {}".format(e))

    def push_all_changes(self, message, allow_master=False):
        """
        Adds all modified and untracked files to git, commits with the message provided and pushes to git

        :param message: The commit message to include with the push
        :param allow_master: Can commit changes to the master branch
        """
        if not allow_master and self._repo.active_branch is "master":
            raise RuntimeError("Attempting to commit to master branch")

        if len(self._repo.index.diff(None))>0:
            try:
                self._repo.git.add(A=True)
                self._repo.git.commit(m=message)
                if not LOCAL:
                    self._repo.git.push()
            except GitCommandError as e:
                raise RuntimeError("Error whilst pushing changes to git, {}".format(e))