"""
Detects which OS Cassian is running on, in exactly one place. Every other
module that needs to branch on platform should import get_os() from here
instead of calling platform.system() / os.name directly -- keeps the
OS-detection logic (and any future edge cases) centralised.
"""

import platform


def get_os() -> str:
    """
    Returns one of: 'windows', 'mac', 'linux'.

    Anything Python's platform.system() doesn't recognise as Windows or
    Darwin is treated as linux, since that's the closest behavioural match
    (POSIX shell, xdg-open, etc.) for the *nix family Cassian is likely to
    encounter (Linux, BSD, WSL).
    """
    system = platform.system()
    if system == "Windows":
        return "windows"
    if system == "Darwin":
        return "mac"
    return "linux"


def is_windows() -> bool:
    return get_os() == "windows"


def is_mac() -> bool:
    return get_os() == "mac"


def is_linux() -> bool:
    return get_os() == "linux"
