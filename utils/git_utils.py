"""
Utilities for interacting with Git. This is largely done via the command line because it's simpler and easier
to maintain than the PythonGit API.
"""
from git import Repo, GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from .command_line_utils import ask_do_step, get_input
from templates.paths import SUPPORT_README
from .file_system_utils import copy_file, mkdir, rmtree
from os.path import join, exists
from time import sleep
import logging


class RepoWrapper(object):
    """
    A wrapper around a git repository
    """
    def __init__(self, path):
        """
        Args:
            path: The path to the git repository
        """
        try:
            self._repo = Repo(path)
        except (InvalidGitRepositoryError, NoSuchPathError):
            mkdir(path)
            self._repo = Repo.init(path)
            self.add_initial_commit()
        except Exception as e:
            raise RuntimeError("Unable to attach to git repository at path {}: {}".format(path, e))

    def prepare_new_branch(self, branch):
        """
        Args:
            branch: Name of the new branch
        """
        logging.info("Preparing new branch, {}, for repo {}".format(branch, self._repo.working_tree_dir))
        if self._repo.is_dirty():
            try:
                option = int(get_input(
                    "Repository {} is dirty, clean it? \n"
                    "    0: No clean\n"
                    "    1: Stash uncommited changes\n"
                    "    2: Clean (-fd). All uncommited changes will be lost\n"
                    "    3: Reset hard to HEAD. All unpushed changes will be lost\n"
                    "    [Default: 0] ".format(self._repo.working_tree_dir)))
            except (ValueError, TypeError):
                option = 0
            logging.info("Option {} selected".format(option))
            try:
                if option == 1:
                    logging.info("Local changes will be stashed")
                    self._repo.git.stash(include_untracked=True)
                elif option == 2 and ask_do_step(
                        "Git clean -fd requested. All uncommited changes will be lost. Are you sure?"):
                    self._repo.git.clean(f=True, d=True)
                elif option == 3 and ask_do_step(
                        "Git reset HEAD --hard requested. All unpushed changes will be lost. Are you sure?"):
                    self._repo.git.reset("HEAD", hard=True)
                else:
                    logging.info("No clean requested")
            except GitCommandError as e:
                logging.warning("Error whilst scrubbing repository. I'll try to continue anyway: {}").format(e)

        try:
            logging.info("Switching repo {} to master and fetching latest changes".format(self._repo.working_tree_dir))
            self._repo.git.checkout("master")
            self._repo.git.fetch(recurse_submodules=True)
        except GitCommandError as e:
            raise RuntimeError("Could not switch repo back to master: {}".format(e))

        try:
            logging.info("Creating/switching to branch {}".format(branch))
            branch_is_new = branch.upper() not in [b.name.upper() for b in self._repo.branches]  # Case insensitive
            self._repo.git.checkout(branch, b=branch_is_new)
            self._repo.git.push("origin", branch, set_upstream=True)
        except GitCommandError as e:
            raise RuntimeError("Error whilst creating git branch, {}".format(e))

        logging.info("Branch {} ready".format(branch))

    def push_all_changes(self, message, allow_master=False):
        """
        Adds all modified and un-tracked files to git, commits with the message provided and pushes to git

        Args:
            message: The commit message to include with the push
            allow_master: Can commit changes to the master branch
        """
        logging.info("Pushing all changes to current branch, {}, for repo {}".format(
            self._repo.active_branch, self._repo.working_tree_dir))
        if not allow_master and self._repo.active_branch is "master":
            raise RuntimeError("Attempting to commit to master branch")

        try:
            self._repo.git.add(A=True)
            n_files = len(self._repo.index.diff("HEAD"))
            if n_files > 0:
                self._repo.git.commit(m=message)
                self._repo.git.push(recurse_submodule="check")
                logging.info("{} files pushed to {}: {}".format(n_files, self._repo.active_branch, message))
            else:
                logging.warn("Commit aborted. No files changed")
        except GitCommandError as e:
            raise RuntimeError("Error whilst pushing changes to git, {}".format(e))

    def add_initial_commit(self):
        """
        Returns:
             Adds a starting commit to a repo
        """
        try:
            copy_file(SUPPORT_README, join(self._repo.working_dir, "README.md"))
            self._repo.git.add(A=True)
            self._repo.git.commit(m="Initial commit")
            self._repo.git.push("origin", "master", set_upstream=True)
        except (OSError, GitCommandError) as e:
            raise RuntimeError("Error whilst creating initial commit in {}: {}"
                               .format(self._repo.working_dir, e))

    def create_submodule(self, name, url, path):
        """
        Args:
            name: Name of the submodule
            url: Url to the submodule repo
            path: Local system path to the submodule
        """
        try:
            git_modules_path = join(self._repo.working_tree_dir, ".git", "modules", name)
            if self.contains_submodule(url):
                get_input("Submodule {} already exists. Confirm this is as expected and press return to continue"
                          .format(name))
            else:
                if exists(git_modules_path) and ask_do_step(
                        "The submodule {} is not part of this repo, yet {} exists. Shall I delete it?"
                        "".format(name, git_modules_path)):
                    rmtree(git_modules_path)
                self._repo.create_submodule(name, path, url=url, branch="master")
        except InvalidGitRepositoryError as e:
            logging.error("Cannot add {} as a submodule, it does not exist: {}".format(path, e))
        except GitCommandError as e:
            logging.error("Git command failed to create submodule from {}: {}".format(path, e))
        except Exception as e:
            raise RuntimeError("Unknown error {} of type {} whilst creating submodule in {}".format(e, type(e), path))

    def contains_submodule(self, url):
        """
        Check if the repository already contains the submodule. Can be a little slow to update after a reset so on
        a simple retry loop

        Args:
            url: The url of the remote repository

        Returns:
             True if already a submodule else False
        """
        for i in range(10):
            if url.lower() in [s.url.lower() for s in self._repo.submodules]:
                return True
            sleep(0.1)
        return False
