"""
Launches local applications: text editor, calculator, VS Code, plus
protocol-based apps (Steam, Spotify, Discord, WhatsApp). 

Adding or changing an app should mean editing config/applications.json, not
this file. Each OS in that config lists one or more *candidate* commands to
try in order (e.g. Linux text editors: gedit, then kate, then mousepad, then
nano) so Cassian still finds something usable even if the first choice isn't
installed.
"""

import json
import shutil
import subprocess
from pathlib import Path

from execution import system_open
from utils import platform_utils

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "applications.json"


def _load_app_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"processes": {}, "protocols": {}}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_APP_CONFIG = _load_app_config()


def _binary_available(command: list) -> bool:
    """
    Best-effort check that a candidate command is actually launchable on this
    machine, so fallback chains (gedit -> kate -> mousepad -> nano) don't
    just fire-and-fail on the first entry.
    """
    if not command:
        return False
    executable = command[0]
    # 'open' (mac) and absolute/relative paths are assumed available;
    # anything else is checked against PATH.
    if executable == "open":
        return True
    return shutil.which(executable) is not None


def _launch_first_available(candidates: list) -> bool:
    for command in candidates:
        if _binary_available(command):
            try:
                subprocess.Popen(command)
                return True
            except OSError:
                continue
    return False


def launch_application(action: str) -> bool:
    """
    Returns True if `action` matched a known application (process-based or
    protocol-based) and a launch was attempted, False otherwise.
    """
    current_os = platform_utils.get_os()

    for keyword, platform_map in _APP_CONFIG.get("processes", {}).items():
        if keyword in action:
            candidates = platform_map.get(current_os, [])
            if _launch_first_available(candidates):
                return True

    for keyword, protocol in _APP_CONFIG.get("protocols", {}).items():
        if keyword in action:
            return system_open.open_with_os_default(protocol)

    return False
