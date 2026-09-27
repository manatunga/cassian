"""
Automated test suite for Git guardian's detection layer.
"""

import shutil
import subprocess

import pytest

from cassian.git_guardian.detector import has_git, get_repo_root


def test_has_git_found(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda cmd: "/usr/bin/git")
    assert has_git() is True


def test_has_git_missing(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda cmd: None)
    assert has_git() is False


def test_get_repo_root_success(tmp_path):
    subprocess.run(
        ["git", "init"],
        cwd=tmp_path,
        capture_output=True,
        text=True
    )
    (tmp_path / "src").mkdir()
    root = get_repo_root(start_path=(tmp_path / "src"))

    assert root == tmp_path.resolve()


def test_get_repo_root_not_git_repo(tmp_path):
    (tmp_path / "src").mkdir()
    root = get_repo_root(start_path=(tmp_path / "src"))

    assert root is None
