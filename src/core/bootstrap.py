"""
Start-up/Boostrap sequence for Cassian. 
Initiates before loading memory.
"""

from ui import banner, terminal

def run_boot_sequence(version: str) -> None:
    terminal.clear_screen()
    banner.print_banner(version)
    terminal.print_info("Initializing Cassian's system...")