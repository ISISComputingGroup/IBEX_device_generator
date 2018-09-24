from hamcrest import assert_that, is_, has_length, equal_to
from mock import patch
import unittest

from utils.git_utils import RepoWrapper
from utils.stubs import RepoStub


class TestPushingChangesToGit(unittest.TestCase):

    @patch("utils.git_utils.Repo", new=RepoStub)
    def setUp(self):
        # Given:
        self.repo = RepoWrapper("path")

    def test_that_GIVEN_a_clean_Git_repo_with_ini_commit_WHEN_pushing_changes_with_no_files_THEN_nothing_is_pushed(self):
        # When:
        self.repo.push_changes("a message", files_to_commit=())

        # Then:
        assert_that(self.repo._repo.git.push_called, is_(equal_to(0)))

    def test_that_GIVEN_a_clean_Git_repo_with_ini_commit_WHEN_pushing_changes_with_one_file_THEN_only_that_one_file_is_pushed(self):
        # When:
        self.repo.push_changes("a message", files_to_commit="test_file")

        # Then:
        assert_that(self.repo ._repo.git.push_called, is_(equal_to(1)))
        assert_that(self.repo ._repo.git.pushed[0], "test_file")
        assert_that(self.repo ._repo.git.pushed, has_length(1))

    def test_that_GIVEN_a_clean_Git_repo_with_ini_commit_WHEN_pushing_changes_with_no_files_specified_THEN_git_adds_all_files(self):
        # When:
        self.repo.push_changes("a message")

        # Then:
        assert_that(self.repo ._repo.git.add_all_called, is_(equal_to(1)))

    def test_that_GIVEN_a_clean_Git_repo_with_ini_commit_WHEN_pushing_changes_with_two_files_specified_THEN_git_adds_only_these_two_files(
            self):
        # When:
        files_to_add = ["one\\path", "two\\path"]
        self.repo.push_changes("a message", files_to_commit=files_to_add)

        # Then:
        assert_that(self.repo ._repo.git.add_called, is_(equal_to(1)))
        assert_that(self.repo ._repo.git.pushed, has_length(2))
