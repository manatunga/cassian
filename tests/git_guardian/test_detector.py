"""
Automated test suite for Git guardian's detection layer.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from cassian.git_guardian.detector import get_repo_root, has_git


def test_has_git_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda cmd: "/usr/bin/git")
    assert has_git() is True


def test_has_git_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda cmd: None)
    assert has_git() is False


def test_get_repo_root_success(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, text=True)
    (tmp_path / "src").mkdir()
    root = get_repo_root(start_path=(tmp_path / "src"))

    assert root == tmp_path.resolve()


def test_get_repo_root_not_git_repo(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    root = get_repo_root(start_path=(tmp_path / "src"))

    assert root is None
