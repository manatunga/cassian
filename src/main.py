"""
Main Execution Bootloader for Cassian
"""

from pathlib import Path

from core.engine import CassianCore

if __name__ == '__main__':
    script_dir = Path(__file__).resolve().parent.parent
    target_memory = script_dir / 'data' / 'memory.json'

    assistant = CassianCore(target_memory)
    assistant.run()
