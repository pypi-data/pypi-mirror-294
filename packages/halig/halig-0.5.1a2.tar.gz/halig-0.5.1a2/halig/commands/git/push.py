from halig.commands.git.base import GitBaseCommand


class GitPushCommand(GitBaseCommand):
    def run(self, remotes: list[str] | None = None):
        """Push all changes to the remote git repo"""
        if not remotes:
            self.repo.remotes.origin.push()
            return

        for remote in remotes:
            self.repo.remotes[remote].push()
