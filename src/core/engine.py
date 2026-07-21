"""
Primary execution file for Cassian
"""

# Import dependencies
import json
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


# Master class for Cassian's core object
class CassianCore():

    def __init__(self, filepath):
        self.filepath = filepath
        self.version = '0.7.0'
        self.memory = {}
        self.is_running = True
        self.chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.weather_url = 'https://api.open-meteo.com/v1/forecast?latitude=6.84&longitude=79.92&current=temperature_2m'
    

    # Method to clear terminal screen securely
    def clear_screen(self):
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    

    # Renders Cassian's ASCII header
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
========================================================"""
        print(banner)


    # Helper method to save/update Cassian's memory
    def save_memory(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w') as file:
            json.dump(self.memory, file, indent=4)


    # Method to load Cassian's memory
    def load_memory(self):
        if self.filepath.exists():
            print(f'{CYAN}Loading memory...{RESET}')
            with open(self.filepath, 'r', encoding='utf-8') as file:
                self.memory = json.load(file)
                self.memory['boot_count'] += 1
                self.memory['version'] = self.version
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
                    'add task': 'to add a task to my queue', 
                    'view tasks': 'to view all my tasks in queue', 
                    'run task': 'to execute the top task in queue',
                    'run <app/url>': 'to directly execute an app or URL immediately',
                    'status': 'to view my current system metrics',
                    'telemetry': 'to fetch live environmental weather data', 
                    'help': 'to view all commands I recognize', 
                    'clear': 'to clear my terminal',
                    'exit': 'to exit the system' },
                'task_queue': []
            }
            self.save_memory()
            print(f'{GREEN}Memory initialised and loaded.{RESET}')
            print(f'{CYAN}{self.memory["system_name"]} System Online.{RESET}')
            print(f'Boot Count: {GREEN}{self.memory["boot_count"]}{RESET} | Build: {MAGENTA}v{self.version}{RESET}')
            print(f'Welcome, {MAGENTA}{self.memory["creator"]}{RESET}\n')
    

    # Method to add tasks to queue
    def add_task(self):
        adding_tasks = True
        while adding_tasks:
            task = input(f'{MAGENTA}Enter the task you want me to do:{RESET} ').lower().strip()
            if task == '':
                print(f"{YELLOW}{self.memory['creator']}, there was no task entered...{RESET}")
            else: 
                self.memory['task_queue'].append(task)
                self.save_memory()
                print(f"{GREEN}Task \"{RESET}{task}{GREEN}\" added to queue successfully.{RESET}")
    
            while True:
                response = input(f"{CYAN}Do you have any more tasks to add?{RESET} (y/n) {CYAN}> {RESET}").lower().strip()
                if response in ['y', 'yes']:
                    break  
                elif response in ['n', 'no']:
                    adding_tasks = False  
                    break 
                else:
                    print(f"{YELLOW}Please respond with '{RESET}y{YELLOW}' or '{RESET}n{YELLOW}'.{RESET}")
        
        print(f"{GREEN}Task queue updated.{RESET}\n")


    # Method to view all tasks currently in queue
    def view_tasks(self):
        if len(self.memory['task_queue']) == 0:
            print(f'{YELLOW}There are currently no tasks on queue.{RESET}')
        else:
            print(f"\n{CYAN}---------- ACTIVE TASK QUEUE ----------{RESET}\n")
            for index, task in enumerate(self.memory['task_queue']):
                if index == 0:
                    print(f"{GREEN}Current Task:{RESET}\t{task}")
                elif index == 1:
                    print(f"{MAGENTA}Next Task:{RESET}\t{task}\n")
                else:
                    print(f"Task {index + 1}:\t{task}")
            print('')
    

    # Helper method to parse and spawn local executables/URLs
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


    # Method to run the top queued task (current task)
    def run_task(self):
        if len(self.memory['task_queue']) == 0:
            print(f"{YELLOW}There are currently no tasks on queue.{RESET}\n")
            return
        
        current_task = self.memory['task_queue'][0]
        print(f"\n{CYAN}Attempting execution for queued task:{RESET} {MAGENTA}\"{current_task}\"{RESET}")

        if self.execute_action(current_task):
            completed = self.memory['task_queue'].pop(0)
            self.save_memory()
            print(f"{GREEN}Successfully executed the task: \"{completed}\".{RESET}\n")
            print(f"{CYAN}Task has been removed from queue.{RESET}")
        else:
            print(f"{YELLOW}No automated executable mapped for: \"{current_task}\".{RESET}")
            print(f"{CYAN}Leaving task in queue as a manial reminder.{RESET}\n")
    

    # Method for immediate execution bypassing the queue
    def execute_direct_action(self, action_string):
        print(f"\n{CYAN}Executing direct action:{RESET} {MAGENTA}\"{action_string}\"{RESET}")
        if self.execute_action(action_string):
            print(f"{GREEN}Action spawned successfully.{RESET}\n")
        else:
            print(f"{YELLOW}Unrecognized action: \"{action_string}\". Couldn't map it to a local app or valid URL.{RESET}\n")


    # Method to view core performance details
    def view_status(self):
        print(f"\n{CYAN}---------- SYSTEM METRICS ----------{RESET}\n")
        print(f"\tSystem Name:\t{CYAN}{self.memory['system_name']}{RESET}")
        print(f"\tVersion:\t{MAGENTA}{self.memory['version']}{RESET}")
        print(f"\tCreator:\t{MAGENTA}{self.memory['creator']}{RESET}")
        print(f"\tBoot Count:\t{GREEN}{self.memory['boot_count']}{RESET}")
        print('')


    # Method to view all functional commands for Cassian
    def view_commands(self):
        print(f"\n{CYAN}---------- COMMAND INDEX ----------{RESET}\n")
        for cmd, desc in self.memory['commands'].items():
            print(f"\t{MAGENTA}'{cmd}'{RESET} - {desc}")
        print('')
    

    # Method to fetch environmental weather data
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
            print(f"{RED}I'm afraid the server responded with HTTP status code {err.code}{RESET}")
            return None
        except URLError as err:
            print(f"{RED}Apologies {self.memory['creator']}, but I failed to reach the server.\nThe reason was: {err.reason}{RESET}")
            return None
    

    # Method to terminate Cassian session
    def exit(self):
        print(f"{CYAN}Updating memory...{RESET}")
        self.save_memory()
        print(f"{GREEN}Memory successfully updated. Terminating session...{RESET}")
        print(f"Have a nice day, {MAGENTA}{self.memory['creator']}!{RESET}")
    

    # Method to execute master loop and run Cassian
    def run(self):
        self.display_banner()
        print(f'{CYAN}Initializing system...{RESET}')
        self.load_memory()
        while self.is_running:
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
                    # Target specific target values inside the payload matrix
                    temp = reading["current"]["temperature_2m"]
                    unit = reading["current_units"]["temperature_2m"]
                    print(f"{CYAN}Current Environment Temperature:{RESET} {GREEN}{temp}{unit}{RESET}\n")
            elif command == 'run task' or command == 'execute':
                self.run_task()
            elif command.startswith('run '):
                action = command[4:].strip()
                if action == '':
                    print(f"{YELLOW}You didn't specify an action for direct execution{RESET}")
                else:
                    self.execute_direct_action(action)
            else:
                print(f"{YELLOW}Sorry {self.memory['creator']}, but I don't recognize that command :({RESET}\nPlease try again.")
