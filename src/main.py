"""
Main Execution Bootloader for Cassian
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

ROOT_DIR = SRC_DIR.parent

from core.engine import CassianCore

def main() -> None:

    target_memory = ROOT_DIR / 'data' / 'memory.json'

    assistant = CassianCore(target_memory)
    assistant.run()


if __name__ == '__main__':
    main()
