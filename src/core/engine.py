"""
The brain of Cassian.

CassianCore is the master controller: it starts the program, stops the program,
initialises the other modules, and coordinates the main loop. It delegates specific 
jobs to the modules built for them.
"""

import logging

from core import bootstrap, constants
from commands.parser import parse_commands
from commands.registry import build_registry
from memory.manager import MemoryManager
from ui import terminal
from utils.logger import setup_logging


class CassianCore:

    def __init__(self, filepath):
        self.filepath = filepath
        self.version = constants.VERSION
        self.is_running = True

        self.memory_manager = MemoryManager(self.filepath, self.version)
        self.memory = {}

        setup_logging(self.filepath)
        self.registry = build_registry()

    #-------------------------------------------------------------------
    # -------------------------- Lifecycle -----------------------------
    #-------------------------------------------------------------------

    def run(self):
        bootstrap.run_boot_sequence(self.version)
        self.memory = self.memory_manager.load()

        while self.is_running:
            try:
                self._tick()
            except Exception as err:
                logging.error(f"System Exception Caught: {err}", exc_info=True)
                terminal.print_error("[SYSTEM ERROR ANOMALY] An unexpected error occurred.")
                terminal.print_info(
                    "Fault details logged securely to data/system_errors.log. Engine remaining online."
                )

    def _tick(self):
        version = self.memory.get('version', self.version) if self.memory is not None else self.version
        raw_command = input(
            f"{constants.MAGENTA}CASSIAN v{self.memory.get('version', self.version)}"
            f"  {constants.CYAN}>> {constants.RESET}"
        ).strip()

        if raw_command == '':
            terminal.print_warning("Whoa there! No command was entered.")
            return

        cmd_key, argument = parse_commands(raw_command)
        handler = self.registry.get(cmd_key)

        if handler is None:
            user = self.memory.get('user', constants.DEFAULT_CREATOR)
            terminal.print_warning(
                f"Sorry {user}, but I don't recognize that command :(\nPlease try again."
            )
            return

        handler(self, argument)

    def exit(self):
        terminal.print_info("\nUpdating memory...")
        self.memory_manager.save(self.memory)
        terminal.print_success("Memory successfully updated. Terminating session...")
        user = self.memory.get('user', constants.DEFAULT_CREATOR)
        print(f"\nHave a nice day, {constants.MAGENTA}{user}!{constants.RESET}\n")
        self.is_running = False
