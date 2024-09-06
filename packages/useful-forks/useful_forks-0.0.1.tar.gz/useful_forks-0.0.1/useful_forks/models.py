from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from datetime import datetime


class ComparisonFork(TypedDict):
    full_name: str
    ahead_by: int
    behind_by: int
    status: Literal["diverged", "ahead", "behind", "identical"]
    total_commits: int
    files_changed: int
    additions: int
    deletions: int
    latest_push: datetime | None
