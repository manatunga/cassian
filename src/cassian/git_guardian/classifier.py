"""
Classification layer for Cassian's Git guardian. Holds functions to
inspect git commands run by Cassian against a list of approved commands,
and classifies accordingly.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum

_VALUE_OPTS = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"})
_FLAG_OPTS = frozenset(
    {
        "-p",
        "--paginate",
        "-P",
        "--no-pager",
        "--bare",
        "--no-replace-objects",
        "--literal-pathspecs",
        "--glob-pathspecs",
        "--noglob-pathspecs",
        "--icase-pathspecs",
        "--no-optional-locks",
    }
)
_LONG_WITH_VALUE = frozenset({"--git-dir", "--work-tree", "--namespace", "--config-env"})


@dataclass(frozen=True)
class ParsedCommand:
    subcommand: str
    args: tuple[str, ...]
    chdir: tuple[str, ...]


def find_subcommand(argv: Sequence[str]) -> ParsedCommand | None:
    chdir: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] in _VALUE_OPTS:
            if i + 1 >= len(argv):
                return None

            if argv[i] == "-C":
                chdir.append(argv[i + 1])
            i += 2
            continue

        if "=" in argv[i] and argv[i].split("=", 1)[0] in _LONG_WITH_VALUE:
            i += 1
            continue

        if argv[i] in _FLAG_OPTS:
            i += 1
            continue

        if argv[i].startswith("-"):
            return None

        return ParsedCommand(argv[i], tuple(argv[i + 1 :]), tuple(chdir))

    return None


class Verdict(Enum):
    SAFE = "safe"
    SNAPSHOT = "snapshot"
    REFUSE = "refuse"


_ALWAYS_SAFE = frozenset(
    {"status", "log", "diff", "show", "fetch", "blame", "ls-files", "rev-parse", "add"}
)
_CONDITIONAL: dict[str, Callable[[tuple[str, ...]], bool]] = {
    "commit": lambda args: "--amend" not in args,
    "stash": lambda args: bool(args) and args[0] in {"list", "show"},
}


def _has_short_flag(args: tuple[str, ...], letters: list[str]) -> bool:
    return any(
        arg.startswith("-")
        and not arg.startswith("--")
        and any(letter in arg for letter in letters)
        for arg in args
    )


def classify(argv: Sequence[str]) -> Verdict:
    result = find_subcommand(argv)

    if result is None:
        return Verdict.SNAPSHOT

    if result.subcommand == "clean" and _has_short_flag(result.args, ["x", "X"]):
        return Verdict.REFUSE

    if result.subcommand in _ALWAYS_SAFE:
        return Verdict.SAFE

    if result.subcommand in _CONDITIONAL and _CONDITIONAL[result.subcommand](result.args):
        return Verdict.SAFE

    return Verdict.SNAPSHOT
