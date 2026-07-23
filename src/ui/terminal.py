"""
Funnel for all raw print() calls to run through before displaying on the terminal.
Color-coded based on the type of message/output being sent to user.
"""

import os
import subprocess
from core.constants import CYAN, GREEN, RED, YELLOW, RESET

def clear_screen():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


def print_header(title: str):
    print(f"\n{CYAN}--------------------{title}--------------------{RESET}\n")

def print_success(message: str):
    print(f"{GREEN}{message}{RESET}")

def print_error(message: str):
    print(f"{RED}{message}{RESET}")

def print_warning(message: str):
    print(f"{YELLOW}{message}{RESET}")

def print_info(message: str):
    print(f"{CYAN}{message}{RESET}")
