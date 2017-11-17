""" Tests for Git utilities """
import unittest
from git import Repo
from mock import MagicMock, patch
from git_utils import GitUtilsException, GitRepoWrapper, LOGGER


class GitUtilsExceptionTests(unittest.TestCase):
    """
    Tests for the GitUtilsException class
    """

    def test_WHEN_an_exception_is_created_THEN_its_message_contains_the_input_message(self):
        message = "A git exception has occurred"
        self.assertTrue(message in GitUtilsException(message).message)

    def test_WHEN_an_exception_is_created_THEN_an_error_is_sent_to_the_log_containing_the_message(self):
        LOGGER.error = MagicMock()
        message = "A git exception has occurred"
        GitUtilsException(message)
        LOGGER.error.assert_called_once()
        LOGGER.error.assert_called_with(message)


class GitRepoTests(unittest.TestCase):
    """
    Tests for the GitRepo class
    """

    def test_GIVEN_a_branch_name_which_is_not_an_existing_branch_WHEN_a_new_branch_is_requested_THEN_a_new_branch_is_requested_from_the_git_module(self):
        # Arrange
        with patch("git.Repo.create_head") as create_head:
            with patch("git.Repo.branches") as branches:
                create_head.__get__ = MagicMock()
                branches.__get__ = MagicMock(return_value=["not_new_branch"])
                repo = GitRepoWrapper("")

                # Act
                repo.create_branch("new_branch")

                # Assert
                repo._repo.create_head.assert_called_once()

    def test_GIVEN_a_branch_name_which_matches_an_existing_branch_WHEN_a_new_branch_is_requested_THEN_not_new_branch_is_requested_and_an_exception_is_thrown(self):
        # Arrange
        with patch("git.Repo.create_head") as create_head:
            with patch("git.Repo.branches") as branches:
                branch = "new_branch"
                create_head.__get__ = MagicMock()
                branches.__get__ = MagicMock(return_value=[branch])
                repo = GitRepoWrapper("")

                # Act
                try:
                    repo.create_branch(branch)
                except GitUtilsException:
                    pass
                # Assert
                except Exception as e:
                    raise AssertionError("Unknown exception when creating a Mock repo branch: {}".format(e))
                else:
                    raise AssertionError("No exception raised by trying to create a branch with name matching an existing branch")

                repo._repo.create_head.assert_not_called()
