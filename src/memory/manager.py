"""
All related to accessing and manipulating Cassian's memory:
loading, saving, creating, migrating
"""

import json
import getpass
from memory import profile
from ui import terminal
from services.location import city_to_coordinates
from core.constants import GREEN, MAGENTA, YELLOW, CYAN, RESET, DEFAULT_LOCATION

class MemoryManager():

    def __init__(self, filepath, version: str):
        self.filepath = filepath
        self.version = version

    #-----------------------------------
    # ---------- Perseistence ----------
    #-----------------------------------

    def save(self, memory: dict):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w') as file:
            json.dump(memory, file, indent=4)

    def load(self) -> dict:
        if self.filepath.exists():
            return self._load_existing()
        return self._create_new()
    

    #-------------------------------
    # ---------- Internal ----------
    #-------------------------------
    
    def _load_existing(self) -> dict:
        terminal.print_info("Loading Cassian's memory...")
        with open(self.filepath, 'r', encoding='utf-8') as file:
            memory = json.load(file)

        memory['boot_count'] += 1
        memory['version'] = self.version
        self._migrate_schema(memory)
        self.save(memory)

        terminal.print_success("\nMemory loaded to system.")
        terminal.print_info(f"{memory['system_name']} System Online.")
        print(f"Boot Count: {GREEN}{memory['boot_count']}{RESET} | Build: {MAGENTA}{self.version}{RESET}")
        print(f"\nWelcome back, {MAGENTA}{memory['user']}!\n")

        return memory


    def _create_new(self) -> dict:
        terminal.print_warning("Initializing Cassian's memory for the first time...")

        name = input(f"{MAGENTA}What may I call you?{RESET} (your name){MAGENTA} >{RESET} ")
        while not name:
            name = input(f"{YELLOW}I'm afraid name cannot be empty. Please tell me your name > ")

        city = input(f"{MAGENTA}Enter your city of residence {YELLOW}(ONLY used for fetching temperature data){RESET} {MAGENTA}>{RESET} ")
        if not city:
            terminal.print_warning(f"City not entered. Defaulting to Colombo...")
            coords = None
        else:
            coords = city_to_coordinates(city)

        if not coords:
            terminal.print_warning(f"Could not resolve coordinates for '{city}'. Defaulting to Colombo...")
            location_dict = dict(DEFAULT_LOCATION)
        else:
            location_dict = {'lat': coords[0], 'lon': coords[1]}

        while True:
            password = getpass.getpass(f"{MAGENTA}Set a password for protected commands: {RESET}")
            if not password:
                terminal.print_warning("Password cannot be empty. Please enter a valid password.\n")
                continue
            confirm_pwd = getpass.getpass(f"{CYAN}Confirm your password: {RESET}")
            if password == confirm_pwd:
                break
            terminal.print_warning("Passwords do not match. Please try again.")

        memory = profile.create_memory(
            version=self.version,
            user=name,
            city=city,
            location=location_dict,
            password=password
        )
        self.save(memory)

        terminal.print_success("\nProfile setup is complete!")
        terminal.print_success("\nMemory loaded to system.")
        terminal.print_info(f"{memory['system_name']} System Online.")
        print(f"Boot Count: {GREEN}{memory['boot_count']}{RESET} | Build: {MAGENTA}{self.version}{RESET}")
        print(f"\nWelcome, {MAGENTA}{memory['user']}!\n")

        return memory


    def _migrate_schema(self, memory:dict):
        """
        Keeps older memory.json files compatible with the current schema.
        Add a new migration step here whenever the shape of memory changes.
        """
        migrated_queue = []
        for item in memory.get('task_queue', []):
            if isinstance(item, str):
                migrated_queue.append({'task': item, 'priority': 2})
            else:
                migrated_queue.append(item)
        memory['task_queue'] = migrated_queue
        memory['task_queue'].sort(key=lambda x: x['priority'])

        if 'notes' not in memory:
            memory['notes'] = []
        if 'location' not in memory:
            memory['location'] = dict(DEFAULT_LOCATION)
        if 'city' not in memory['location']:
            memory['location']['city'] = 'Unknown'
        if 'auth' not in memory:
            memory['auth'] = {'password_hash': None}