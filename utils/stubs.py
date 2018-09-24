
class RepoStub(object):

    def __init__(self, path):
        self._git = GitStub(self)
        self._working_tree_dir = path
        self.working_dir = ""
        self._index = IndexStub(self)

    @property
    def active_branch(self):
        return self.git.active_branch

    def create_submodule(self):
        pass

    @property
    def git(self):
        return self._git

    @property
    def index(self):
        return self._index

    @property
    def working_tree_dir(self):
        """:return: The working tree directory of our git repository. If this is a bare repository, None is returned.
        """
        return self._working_tree_dir


class IndexStub(object):

    def __init__(self, repo):
        self.repo = repo

    def diff(self, *args):
        return self.repo.git.staged


class GitStub(object):

    def __init__(self, repo):
        self.repo = repo
        self.staged = []
        self.committed = []
        self.pushed = []
        self._branches = ["master"]
        self.active_branch = None
        self.add_called = 0
        self.push_called = 0
        self.commit_called = 0
        self.add_all_called = 0

    def add(self, files_to_add=None, A=False, *args, **kwargs):
        self.add_called += 1
        if A:
            self.add_all_called += 1
        elif files_to_add is not None:
            for path in files_to_add.split(" "):
                self.staged.append(path)
        else:
            pass

    def push(self, *args, **kwargs):
        self.push_called += 1
        self.pushed.extend(self.committed)
        self.committed = []

    def checkout(self, branch,  b=None, *args, **kwargs):
        if branch in self._branches:
            self.active_branch = branch
        elif b is not None:
            self._branches.append(b)
            self.active_branch = branch
        else:
            print("{} does not exist.".format(branch))

    def commit(self, *args, **kwargs):
        self.commit_called += 1
        self.committed = self.staged
        self.staged = []
