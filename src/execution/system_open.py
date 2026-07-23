"""
Hands a protocol link (steam://, spotify://, discord://, whatsapp://) or a
file path to the OS's own "open with registered handler" mechanism.

This is the cross-platform replacement for the old Windows-only
`cmd /c start <protocol>` trick:
  - Windows: `start`  (via cmd)
  - macOS:   `open`
  - Linux:   `xdg-open`
"""

import subprocess

from utils import platform_utils


def open_with_os_default(target: str) -> bool:
    """
    Returns True if the OS accepted the request to open `target` (this does
    NOT guarantee the target app is actually installed -- just that the OS
    launcher itself ran without error). Returns False if the platform has no
    known opener or the opener command itself couldn't run.
    """
    system = platform_utils.get_os()

    try:
        if system == "windows":
            # The empty "" is a required placeholder for the window title
            # argument that `start` expects before the target.
            subprocess.Popen(["cmd", "/c", "start", "", target], shell=False)
        elif system == "mac":
            subprocess.Popen(["open", target])
        else:
            subprocess.Popen(["xdg-open", target])
        return True
    except (OSError, FileNotFoundError):
        return False
