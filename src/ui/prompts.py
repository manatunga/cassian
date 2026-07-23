"""
Responsible for user input collection, including:
'asking' (free text) questions & 'confirm' (boolean) questions
"""

from ui import terminal
from core.constants import CYAN, MAGENTA, YELLOW, RESET

def ask(prompt: str) -> str:
    return input(f"{MAGENTA}{prompt}{MAGENTA} ").lower().strip()

def confirm(prompt: str) -> bool:
    while True:
        response = input(f"{CYAN}{prompt}{RESET} (y/n) {CYAN}> {RESET}").lower().strip()
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        terminal.print_warning(f"Please respond with {RESET}'y'{YELLOW} or {RESET}'n'{YELLOW}.")