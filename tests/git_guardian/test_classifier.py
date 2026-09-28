"""
Automated test suite for Git guardian's classification layer.
"""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from cassian.git_guardian.classifier import (
    ParsedCommand,
    Verdict,
    classify,
    find_subcommand,
)


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["status"], ParsedCommand(subcommand="status", args=(), chdir=())),
        (
            ["reset", "--hard"],
            ParsedCommand(subcommand="reset", args=("--hard",), chdir=()),
        ),
        (
            ["-c", "user.name=x", "status"],
            ParsedCommand(subcommand="status", args=(), chdir=()),
        ),
        (
            ["-C", "../x", "status"],
            ParsedCommand(subcommand="status", args=(), chdir=("../x",)),
        ),
        (
            ["-C", "a", "-C", "b", "status"],
            ParsedCommand(subcommand="status", args=(), chdir=("a", "b")),
        ),
        (
            ["--git-dir=/x", "status"],
            ParsedCommand(subcommand="status", args=(), chdir=()),
        ),
        (["--no-pager", "log"], ParsedCommand(subcommand="log", args=(), chdir=())),
        (
            ["--git-dir", "/x", "status"],
            ParsedCommand(subcommand="status", args=(), chdir=()),
        ),
        (
            ["-C", "../x", "--no-pager", "reset", "--hard"],
            ParsedCommand(subcommand="reset", args=("--hard",), chdir=("../x",)),
        ),
        (["-C"], None),
        (["--weird", "status"], None),
        ([], None),
    ],
)
def test_find_subcommand(argv: Sequence[str], expected: ParsedCommand) -> None:
    result = find_subcommand(argv)
    assert result == expected


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["status"], Verdict.SAFE),
        (["-C", "../x", "status"], Verdict.SAFE),
        (["commit", "-m", "x"], Verdict.SAFE),
        (["commit", "--amend"], Verdict.SNAPSHOT),
        (["stash", "list"], Verdict.SAFE),
        (["stash"], Verdict.SNAPSHOT),
        (["stash", "pop"], Verdict.SNAPSHOT),
        (["reset", "--hard"], Verdict.SNAPSHOT),
        (["co"], Verdict.SNAPSHOT),
        (["--weird", "status"], Verdict.SNAPSHOT),
        ([], Verdict.SNAPSHOT),
        (["clean", "-fd"], Verdict.SNAPSHOT),
        (["clean", "-fdx"], Verdict.REFUSE),
        (["clean", "-fdX"], Verdict.REFUSE),
        (["clean", "-f", "-x"], Verdict.REFUSE),
        (["clean", "--exclude=foo"], Verdict.SNAPSHOT),
        (["ls-files"], Verdict.SAFE),
    ],
)
def test_classify(argv: Sequence[str], expected: Verdict) -> None:
    verdict = classify(argv)
    assert verdict == expected
