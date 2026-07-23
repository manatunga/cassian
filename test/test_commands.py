"""
Tests for commands/parser.py and commands/registry.py.
"""

from src.commands.parser import parse_command
from src.commands.registry import build_registry


def test_parse_simple_command():
    assert parse_command("status") == ("status", None)


def test_parse_prefixed_run_command():
    assert parse_command("run spotify") == ("run", "spotify")


def test_parse_prefixed_delete_task_command():
    assert parse_command("delete task 3") == ("delete_task", "3")


def test_parse_is_case_insensitive_for_the_command_key():
    cmd_key, arg = parse_command("SEARCH cats")
    assert cmd_key == "search"
    assert arg == "cats"


def test_registry_contains_all_static_commands():
    registry = build_registry()
    for expected in ("status", "help", "exit", "clear", "telemetry", "view tasks"):
        assert expected in registry
