"""
Primary execution file for Cassian
"""

import json
import logging
import os
import subprocess
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError 

# ANSI Constants for styling Cassian's terminal UI
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


class CassianCore():

    def __init__(self, filepath):
        self.filepath = filepath
        self.version = '0.9.0'
        self.memory = {}
        self.is_running = True
        self.chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.weather_url = 'https://api.open-meteo.com/v1/forecast?latitude=6.84&longitude=79.92&current=temperature_2m'
        
        # Setup error log file location
        log_file = self.filepath.parent / "system_errors.log"
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def clear_screen(self):
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    def display_banner(self):
        self.clear_screen()
        banner = f"""{CYAN}
  ██████╗ █████╗ ███████╗███████╗██╗ █████╗ ███╗   ██╗
 ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔══██╗████╗  ██║
 ██║     ███████║███████╗███████╗██║███████║██╔██╗ ██║
 ██║     ██╔══██║╚════██║╚════██║██║██╔══██║██║╚██╗██║
 ╚██████╗██║  ██║███████║███████║██║██║  ██║██║ ╚████║
  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝{RESET}
{MAGENTA}           -- CYBERPUNK HUD EDITION v{self.version} --           {RESET}
========================================================\n"""
        print(banner)

    def save_memory(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w') as file:
            json.dump(self.memory, file, indent=4)

    def load_memory(self):
        if self.filepath.exists():
            print(f'{CYAN}Loading memory...{RESET}')
            with open(self.filepath, 'r', encoding='utf-8') as file:
                self.memory = json.load(file)
                self.memory['boot_count'] += 1
                self.memory['version'] = self.version

            migrated_queue = []
            for item in self.memory.get('task_queue', []):
                if isinstance(item, str):
                    migrated_queue.append({'task': item, 'priority': 2})
                else:
                    migrated_queue.append(item)
            self.memory['task_queue'] = migrated_queue
            self.memory['task_queue'].sort(key=lambda x: x['priority'])

            print(f'{GREEN}Memory initialised and loaded.{RESET}')
            print(f'{CYAN}{self.memory["system_name"]} System Online.{RESET}')
            print(f'Boot Count: {GREEN}{self.memory["boot_count"]}{RESET} | Build: {MAGENTA}v{self.version}{RESET}')
            print(f'Welcome back, {MAGENTA}{self.memory["creator"]}{RESET}\n')
        else:
            print(f'{YELLOW}Initialising memory for the first time...{RESET}')
            self.memory = {
                'system_name': 'Cassian',
                'version': self.version,
                'creator': 'Jan',
                'boot_count': 1,
                'commands': {
                    'add task': 'to add a prioritized task to my queue', 
                    'view tasks': 'to view all tasks sorted by priority', 
                    'run task': 'to execute the top priority task',
                    'run <app/url>': 'to directly execute an app or URL immediately',
                    'status': 'to view my current system metrics',
                    'telemetry': 'to fetch live environmental weather data', 
                    'help': 'to view all commands I recognize', 
                    'clear': 'to clear my terminal',
                    'exit': 'to exit the system' 
                },
                'task_queue': []
            }
            self.save_memory()
            print(f'{GREEN}Memory initialised and loaded.{RESET}')
            print(f'{CYAN}{self.memory["system_name"]} System Online.{RESET}')
            print(f'Boot Count: {GREEN}{self.memory["boot_count"]}{RESET} | Build: {MAGENTA}v{self.version}{RESET}')
            print(f'Welcome, {MAGENTA}{self.memory["creator"]}{RESET}\n')

    def add_task(self):
        adding_tasks = True
        while adding_tasks:
            task = input(f'{MAGENTA}Enter the task description:{RESET} ').lower().strip()
            if task == '':
                print(f"{YELLOW}{self.memory['creator']}, no task was entered...{RESET}")
            else: 
                p_input = input(f"{CYAN}Set priority - (1) High, (2) Medium, (3) Low [Default=2]:{RESET} ").strip().lower()
                if p_input in ['1', 'h', 'high']:
                    priority = 1
                elif p_input in ['3', 'l', 'low']:
                    priority = 3
                else:
                    priority = 2

                self.memory['task_queue'].append({'task': task, 'priority': priority})
                self.memory['task_queue'].sort(key=lambda x: x['priority'])
                self.save_memory()
                print(f"{GREEN}Task \"{RESET}{task}{GREEN}\" [Priority {priority}] queued successfully.{RESET}")

            while True:
                response = input(f"{CYAN}Add another task?{RESET} (y/n) {CYAN}> {RESET}").lower().strip()
                if response in ['y', 'yes']:
                    break  
                elif response in ['n', 'no']:
                    adding_tasks = False  
                    break 
                else:
                    print(f"{YELLOW}Please respond with 'y' or 'n'.{RESET}")
        
        print(f"{GREEN}Task queue updated and sorted by priority.{RESET}\n")

    def view_tasks(self):
        if len(self.memory['task_queue']) == 0:
            print(f'{YELLOW}There are currently no tasks in queue.{RESET}')
        else:
            print(f"\n{CYAN}---------- ACTIVE TASK QUEUE (BY PRIORITY) ----------{RESET}\n")
            p_labels = {1: f"{RED}[HIGH]{RESET}", 2: f"{CYAN}[MED]{RESET}", 3: f"{GREEN}[LOW]{RESET}"}
            
            for index, item in enumerate(self.memory['task_queue']):
                p_tag = p_labels.get(item['priority'], "[MED]")
                task_desc = item['task']
                if index == 0:
                    print(f"{GREEN}TOP TASK:{RESET} {p_tag} {task_desc}")
                else:
                    print(f"Task {index + 1}: {p_tag} {task_desc}")
            print('')

    def execute_action(self, target_action):
        action = target_action.lower().strip()

        if 'notepad' in action:
            subprocess.Popen(['notepad.exe'])
            return True
        elif 'calc' in action or 'calculator' in action:
            subprocess.Popen(['calc.exe'])
            return True
        elif 'code' in action or 'vs code' in action or 'vscode' in action:
            subprocess.Popen(['code'], shell=True)
            return True
        elif 'chrome' in action or 'google chrome' in action or 'google' in action:
            subprocess.Popen([self.chrome_path, 'https://google.com'])
            return True
        elif 'steam' in action:
            subprocess.Popen(["cmd", "/c", "start", "steam://"])
            return True
        elif 'spotify' in action:
            subprocess.Popen(["cmd", "/c", "start", "spotify://"])
            return True
        elif 'discord' in action:
            subprocess.Popen(["cmd", "/c", "start", "discord://"])
            return True
        elif 'whatsapp' in action:
            subprocess.Popen(["cmd", "/c", "start", "whatsapp://"])
            return True
        elif action.startswith('http://') or action.startswith('https://'):
            subprocess.Popen([self.chrome_path, action], shell=True)
            return True
        else:
            return False

    def run_task(self):
        if len(self.memory['task_queue']) == 0:
            print(f"{YELLOW}There are currently no tasks in queue.{RESET}\n")
            return
        
        current = self.memory['task_queue'][0]
        current_task = current['task']
        print(f"\n{CYAN}Attempting execution for top priority task:{RESET} {MAGENTA}\"{current_task}\"{RESET}")

        if self.execute_action(current_task):
            completed = self.memory['task_queue'].pop(0)
            self.save_memory()
            print(f"{GREEN}Successfully executed task: \"{completed['task']}\".{RESET}")
            print(f"{CYAN}Removed from queue.{RESET}\n")
        else:
            print(f"{YELLOW}No automated executable mapped for: \"{current_task}\".{RESET}")
            print(f"{CYAN}Leaving task in queue as a manual reminder.{RESET}\n")

    def execute_direct_action(self, action_string):
        print(f"\n{CYAN}Executing direct action:{RESET} {MAGENTA}\"{action_string}\"{RESET}")
        if self.execute_action(action_string):
            print(f"{GREEN}Action spawned successfully.{RESET}\n")
        else:
            print(f"{YELLOW}Unrecognized action: \"{action_string}\". Couldn't map to local app or URL.{RESET}\n")

    def view_status(self):
        print(f"\n{CYAN}---------- SYSTEM METRICS ----------{RESET}\n")
        print(f"\tSystem Name:\t{CYAN}{self.memory['system_name']}{RESET}")
        print(f"\tVersion:\t{MAGENTA}{self.memory['version']}{RESET}")
        print(f"\tCreator:\t{MAGENTA}{self.memory['creator']}{RESET}")
        print(f"\tBoot Count:\t{GREEN}{self.memory['boot_count']}{RESET}")
        print('')

    def view_commands(self):
        print(f"\n{CYAN}---------- COMMAND INDEX ----------{RESET}\n")
        for cmd, desc in self.memory['commands'].items():
            print(f"\t{MAGENTA}'{cmd}'{RESET} - {desc}")
        print('')

    def fetch_telemetry(self):
        try:
            req = urllib.request.Request(
                self.weather_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )

            with urllib.request.urlopen(req) as res:
                raw_telemetry = res.read().decode('utf-8')
                telemetry = json.loads(raw_telemetry)
            
            print(f'{GREEN}Network transmission complete. Reading processed.{RESET}\n')
            return telemetry
        except HTTPError as err:
            print(f"{RED}Server responded with HTTP status code {err.code}{RESET}")
            return None
        except URLError as err:
            print(f"{RED}Failed to reach server. Reason: {err.reason}{RESET}")
            return None

    def exit(self):
        print(f"{CYAN}Updating memory...{RESET}")
        self.save_memory()
        print(f"{GREEN}Memory successfully updated. Terminating session...{RESET}")
        print(f"Have a nice day, {MAGENTA}{self.memory['creator']}!{RESET}\n")

    def run(self):
        self.display_banner()
        print(f'{CYAN}Initializing system...{RESET}')
        self.load_memory()
        
        while self.is_running:
            try:
                command = input(f"{MAGENTA}CASSIAN v{self.memory['version']}  {CYAN}>> {RESET}").lower().strip()
                if command == 'add task':
                    self.add_task()
                elif command == 'view tasks':
                    self.view_tasks()
                elif command == 'status':
                    self.view_status()
                elif command == 'help':
                    self.view_commands()
                elif command == 'exit':
                    self.exit()
                    self.is_running = False
                elif command == '':
                    print(f"{YELLOW}Whoa there! No command entered.{RESET}")
                elif command == 'clear':
                    self.display_banner()
                elif command == 'telemetry':
                    print(f"{CYAN}Polling remote telemetry grid...{RESET}")
                    reading = self.fetch_telemetry()
                    if reading:
                        temp = reading["current"]["temperature_2m"]
                        unit = reading["current_units"]["temperature_2m"]
                        print(f"{CYAN}Current Environment Temperature:{RESET} {GREEN}{temp}{unit}{RESET}\n")
                elif command == 'run task' or command == 'execute':
                    self.run_task()
                elif command.startswith('run '):
                    action = command[4:].strip()
                    if action == '':
                        print(f"{YELLOW}You didn't specify an action for direct execution.{RESET}")
                    else:
                        self.execute_direct_action(action)
                else:
                    print(f"{YELLOW}Sorry {self.memory['creator']}, but I don't recognize that command :({RESET}\nPlease try again.")
            except Exception as err:
                logging.error(f"System Exception Caught: {err}", exc_info=True)
                print(f"\n{RED}[SYSTEM ERROR ANOMALY]{RESET} An unexpected error occurred.")
                print(f"{CYAN}Fault details logged securely to memory/system_errors.log. Engine remaining online.{RESET}\n")