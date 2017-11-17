""" Tests for Git utilities """
import unittest
import git
from mock import MagicMock
from git_utils import GitUtilsException, GitRepo, LOGGER


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
        repo = GitRepo("")
        repo.create_head = MagicMock()
        repo.active_branch = MagicMock(return_value=["not_new_branch"])

        # Act
        repo.create_branch("new_branch")

        # Assert
        repo.create_head.assert_called_once()

    def test_GIVEN_a_branch_name_which_matches_an_existing_branch_WHEN_a_new_branch_is_requested_THEN_not_new_branch_is_requested_and_an_exception_is_thrown(self):
        # Arrange
        branch = "new_branch"
        repo = GitRepo("")
        repo.create_head = MagicMock()
        repo.branches = [branch]

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

        repo.create_head.assert_not_called()
