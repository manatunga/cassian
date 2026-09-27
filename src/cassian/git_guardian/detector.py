"""
Detection layer for Cassian's Git guardian. Holds functions to detect
whether Git is installed in the current local machine, and whether the
codebase or directory is a git repository.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def has_git() -> bool:
    return bool(shutil.which("git"))


def get_repo_root(start_path: Path | None = None) -> Path | None:
    cwd = start_path or Path.cwd()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None

        return Path(result.stdout.strip())

    except OSError:
        return None
