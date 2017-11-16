""" Contains utilities for Git/GitHub operations during creation of an IOC """
import git
import logging

LOGGER = logging.getLogger("git_utils")


class GitUtilsException(Exception):
    """
    Type of exception for Git operations
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)
        LOGGER.error(message)


class GitRepo(object):
    """
    A git repository we wish to manipulate as part of the creation of a boilerplate IOC
    """

    LOG_FORMAT = "Git: %s"

    def __init__(self, system_path):
        """
        :param system_path: The local path to the git repo
        """
        self.repo = git.Repo(path=system_path)

    def create_branch(self, branch_name):
        """
        :param branch_name: The name of the branch to create
        """
        if branch_name in self.repo.branches:
            raise GitUtilsException("Unable to create branch {} in repo {}. Branch already exists".format(
                branch_name, self.repo.git_dir))

        LOGGER.info(self.LOG_FORMAT, "Creating branch {} in repo {}".format(branch_name, self.repo.git_dir))
        self.repo.create_head(branch_name)

    def add_modified(self):
        """
        Add all modified files to git
        """
        self.repo.index.add(A=True)

    def commit(self, commit_message):
        """
        Commits all staged changes to git
        :param commit_message: The message to associate with the commit
        """
        self.repo.commit(commit_message)