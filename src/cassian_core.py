"""
Primary execution file for Cassian
"""

# Import dependencies
import json
from pathlib import Path


# Master class for Cassian's core object
class CassianCore():

    def __init__(self, filepath):
        self.filepath = filepath
        self.memory = {}
        self.is_running = True
    
    # Method to save/update Cassian's memory
    def save_memory(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w') as file:
            json.dump(self.memory, file, indent=4)

    # Method to load Cassian's memory
    def load_memory(self):
        if self.filepath.exists():
            print('Loading memory...')
            with open(self.filepath, 'r', encoding='utf-8') as file:
                self.memory = json.load(file)
                self.memory['boot_count'] += 1
            print('Memory initialised and loaded.')
            print(f'{self.memory["system_name"]} System Online. Boot Count: {self.memory["boot_count"]}. Welcome back, {self.memory["creator"]}')
        else:
            print('Initialising memory for the first time...')
            self.memory = {
                'system_name': 'Cassian',
                'creator': 'Jan',
                'boot_count': 1,
                'commands': {
                    'add task': 'to add a task to my queue', 
                    'view tasks': 'to view all my tasks in queue', 
                    'status': 'to view my current system metrics', 
                    'help': 'to view all commands I recognize', 
                    'exit': 'to exit the system' },
                'task_queue': []
            }
            self.save_memory()
            print('Memory initialised and loaded.')
            print(f'{self.memory["system_name"]} System Online. Boot Count: {self.memory["boot_count"]}. Welcome, {self.memory["creator"]}')
    
    # Method to add tasks to queue
    def add_task(self):
        condition_met = False
        while not condition_met:
            task = input('Enter the task you want me to do: >').lower().strip()
            if task == '':
                print(f"{self.memory['creator']}, there was no task entered...")
            else: 
                self.memory['task_queue'].append(task)
                if task in self.memory['task_queue']:
                    print(f'Task, "{task}", has been added to queue.')
                    condition_met = True
                else:
                    print(f'Oops! Error occured when adding your task, "{task}"')
    
    # Method to view all tasks currently in queue
    def view_tasks(self):
        if len(self.memory['task_queue']) == 0:
            print('There are currently no tasks on queue.')
        else:
            print('\nHere are all the tasks you have asked me to do:\n')
            for index, task in enumerate(self.memory['task_queue']):
                if index == 0:
                    print(f'Current Task:  {task}')
                elif index == 1:
                    print(f'Next Task:  {task}\n')
                else:
                    print(f"Task {index + 1}:  {task}")
            print('')
    
    # Method to view core performance details
    def view_status(self):
        print('\nHere are my current system metrics:\n')
        print(f"\tSystem Name:  {self.memory['system_name']}")
        print(f"\tCreator:  {self.memory['creator']}")
        print(f"\tBoot Count:  {self.memory['boot_count']}")
        print('')

    # Method to view all functional commands for Cassian
    def view_commands(self):
        print('\nHere is a list of all the commands that I recognize:\n')
        print(f"\t'add task'  - {self.memory['commands']['add task']}")
        print(f"\t'view tasks'  - {self.memory['commands']['view tasks']}")
        print(f"\t'status'  - {self.memory['commands']['status']}")
        print(f"\t'help'  - {self.memory['commands']['help']}")
        print(f"\t'exit'  - {self.memory['commands']['exit']}")
        print('')
    
    # Method to terminate Cassian session
    def exit(self):
        print('Updating memory...')
        self.save_memory()
        print('Memory has been successfully updated. Terminating session...')
        print(f"Have a nice day, {self.memory['creator']}!")
    
    # Method to execute master loop and run Cassian
    def run(self):
        print('Initializing system...')
        self.load_memory()
        while self.is_running:
            command = input('Waiting for your next command: >').lower().strip()
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
                print('Whoa there! There was no command entered.')
            else:
                print(f"Sorry {self.memory['creator']}, but I don't recognize that command :(\nPlease try again.")



# Execution block to initiate Cassian
if __name__ == '__main__':

    # Calculate directory and look for Cassian's memory
    script_dir = Path(__file__).resolve().parent
    target_memory = script_dir / 'memory' / 'memory.json'

    # Instantiate and fire up system engine
    assistant = CassianCore(target_memory)
    assistant.run()