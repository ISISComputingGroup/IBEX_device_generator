from hamcrest import assert_that, is_, has_length, equal_to
from mock import patch
import unittest

from utils.git_utils import RepoWrapper
from utils.stubs import RepoStub


class TestInitChangesToGit(unittest.TestCase):

    @patch("utils.git_utils.Repo", new=RepoStub)
    def setUp(self):
        # Given:
        self.repo = RepoWrapper("path")

    @patch("utils.git_utils.Repo", new=RepoStub)
    def test_that_GIVEN_a_clean_Git_repo_WHEN_initial_commit_is_called_THEN_only_the_readme_is_pushed(self):
        with patch("utils.git_utils.copy_file") as _:
            self.repo.add_initial_commit()

        # Then:
        assert_that(self.repo._repo.git.push_called, is_(equal_to(1)))
        assert_that(self.repo._repo.git.pushed, has_length(1))
        assert_that(self.repo._repo.git.pushed[0], is_("README.md"))
