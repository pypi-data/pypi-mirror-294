from halig.commands.git.base import GitBaseCommand


class GitCommitCommand(GitBaseCommand):
    def run(self):
        """Add all .age files to git and commit them using gitpython"""
        self.repo.index.add(
            [str(path) for path in self.settings.notebooks_root_path.glob("**/*.age")]
        )
        self.repo.index.commit(self.message)
