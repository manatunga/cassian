"""
Prints Cassian's banner: The ASCII logo, the theme and the version string.
"""

from ui import terminal
from pathlib import Path
from core.constants import CYAN, MAGENTA, RESET

ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / 'assets'
BANNER_FILE = ASSETS_DIR / 'banner.txt'

def __load_ascii_logo() -> str:
    if BANNER_FILE.exists():
        return BANNER_FILE.read_text(encoding='utf-8')

    return 'CASSIAN'


def print_banner(version: str):
    logo = __load_ascii_logo()
    print(f"{CYAN}{logo}{RESET}")
    print(f"{MAGENTA}           -- CYBERPUNK HUD EDITION | v{version} --           {RESET}")
    print(f"========================================================\n")