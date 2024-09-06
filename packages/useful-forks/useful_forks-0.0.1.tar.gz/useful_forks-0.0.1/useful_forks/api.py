from __future__ import annotations

from typing import TYPE_CHECKING

from githubkit import GitHub

if TYPE_CHECKING:
    from githubkit.versions.latest.models import (
        CommitComparison,
        FullRepository,
        MinimalRepository,
        PullRequestSimple,
    )

    from .models import ComparisonFork


class UsefulForks:

    github: GitHub
    base_repo: FullRepository | None = None
    base_repo_full_name: str

    def __init__(self, access_token: str, repo_full_name: str):
        self.github = GitHub(access_token)
        self.base_repo_full_name = repo_full_name

    async def get_repo(self, repo_full_name: str) -> FullRepository:
        """Get a repository object by its full name (e.g., 'owner/repo')."""
        repo_owner, repo_name = repo_full_name.split("/")
        # return self.github.get_repo(repo_full_name)
        resp = await self.github.rest.repos.async_get(owner=repo_owner, repo=repo_name)
        return resp.parsed_data

    async def get_forks(self) -> list[MinimalRepository]:
        """Get all forks of the given repository."""
        if self.base_repo is None:
            self.base_repo = await self.get_repo(self.base_repo_full_name)

        forks = await self.github.rest.repos.async_list_forks(
            owner=self.base_repo.owner.login,
            repo=self.base_repo.name,
            sort="stargazers",
            per_page=100,
            page=1,
        )
        return forks.parsed_data

    async def compare_fork(
        self,
        base_repo: FullRepository | str,
        fork: FullRepository | str,
    ) -> CommitComparison:
        """Compare a fork to the base repository."""
        if isinstance(base_repo, str):
            base_repo = await self.get_repo(base_repo)
        if isinstance(fork, str):
            fork = await self.get_repo(fork)

        response = await self.github.rest.repos.async_compare_commits(
            owner=base_repo.owner.login,
            repo=base_repo.name,
            basehead=f"{base_repo.default_branch}...{fork.owner.login}:{fork.default_branch}",
        )
        return response.parsed_data

    async def get_commit_pulls(self, commit_sha: str) -> list[PullRequestSimple]:
        response = await self.github.rest.repos.async_list_pull_requests_associated_with_commit(
            owner=self.base_repo.owner.login,
            repo=self.base_repo.name,
            commit_sha=commit_sha,
        )
        return response.parsed_data

    async def analyze_forks(self) -> list[ComparisonFork]:
        """Analyze all forks of the given repository and return a summary of the comparisons."""
        forks = await self.get_forks()

        results = []
        for fork in forks:
            comparison = await self.compare_fork(self.base_repo, fork.full_name)
            if comparison.ahead_by > 0:
                fork_pulls = []
                for commit in comparison.commits:
                    pulls = await self.get_commit_pulls(commit.sha)
                    fork_pulls += pulls

                res: ComparisonFork = {
                    "full_name": fork.full_name,
                    "ahead_by": comparison.ahead_by,
                    "behind_by": comparison.behind_by,
                    "status": comparison.status,
                    "total_commits": comparison.total_commits,
                    "files_changed": len(comparison.files),
                    "additions": sum(file.additions for file in comparison.files),
                    "deletions": sum(file.deletions for file in comparison.files),
                    "latest_push": fork.pushed_at,
                }
                results.append(res)

        return results

    async def print_fork_analysis(self) -> str:
        """Print a formatted analysis of all forks for the given repository."""
        results = await self.analyze_forks()
        buf = []
        buf += [f"Fork analysis for {self.base_repo.full_name}:"]
        buf += ["-" * 80]

        for data in results:
            buf += [f"Fork: {data['full_name']}"]
            buf += [f"  Ahead by: {data['ahead_by']} commits"]
            buf += [f"  Behind by: {data['behind_by']} commits"]
            buf += [f"  Status: {data['status']}"]
            buf += [f"  Total commits: {data['total_commits']}"]
            buf += [f"  Files changed: {data['files_changed']}"]
            buf += [f"  Additions: {data['additions']}"]
            buf += [f"  Deletions: {data['deletions']}"]
            buf += [f"  Latest push: {data['latest_push'].isoformat()}"]
            buf += ["-" * 80]

        return "\n".join(buf)
