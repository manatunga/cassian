"""
Primary execution file for Cassian
"""

# Import dependencies
import json
from pathlib import Path

# Function to load Cassian's memory
def load_memory(target):
    if target.exists():
        print('Loading memory...')
        with open(target, 'r', encoding='utf-8') as file:
            memory = json.load(file)
            memory['boot_count'] += 1
            print(f'Cassian System Online. Boot Count: {memory["boot_count"]}. Welcome back, {memory["creator"]}')
    else:
        print('Initialising memory for the first time...')
        memory = {
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
        print(f'Cassian System Online. Boot Count: {memory["boot_count"]}. Welcome, {memory["creator"]}')
    
    return memory


# Function to add tasks to queue
def add_task (state_dict):
    condition_met = False
    while not condition_met:
        task = input('Enter the task on the queue: >').lower().strip()
        if task == '':
            print(f"{state_dict['creator']}, there was no task entered...")
        else: 
            state_dict['task_queue'].append(task)
            if task in state_dict['task_queue']:
                print(f'Task, "{task}", has been added to queue.')
                condition_met = True
            else:
                print(f'Oops! Error occured when adding your task, "{task}"')
    


# Function to view the task queue
def view_tasks(state_dict):
    if len(state_dict['task_queue']) == 0:
        print('No tasks on queue.')
    else:
        print('\nHere are all the tasks currently in my system queue:\n')
        for index, task in enumerate(state_dict['task_queue']):
            if index == 0:
                print(f'Current Task:  {task}')
            elif index == 1:
                print(f'Next Task:  {task}\n')
            else:
                print(f"Task {index + 1}:  {task}")
        print('')


# Function to view the system's status
def view_status(state_dict):
    print('\nHere is my current system metrics:\n')
    print(f"\tSystem Name:  {state_dict['system_name']}")
    print(f"\tCreator:  {state_dict['creator']}")
    print(f"\tBoot Count:  {state_dict['boot_count']}")
    print('')


# Function to exit Cassian
def system_exit(state_dict, target):
    print('Updating memory...')
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, 'w') as file:
        json.dump(state_dict, file, indent=4)
        print('Memory has been successfully updated.')
    print(f"Have a nice day, {state_dict['creator']}!")


# Function to view commands
def view_commands(state_dict):
    print('\nHere is a list of all the commands that I recognize:\n')
    print(f"\t'add task'  - {state_dict['commands']['add task']}")
    print(f"\t'view tasks'  - {state_dict['commands']['view tasks']}")
    print(f"\t'status'  - {state_dict['commands']['status']}")
    print(f"\t'help'  - {state_dict['commands']['help']}")
    print(f"\t'exit'  - {state_dict['commands']['exit']}")
    print('')



# Pre-initialization message
print('Initializing Cassian...')

# Boot up Cassian and load his memory
script_dir = Path(__file__).resolve().parent
target_file = script_dir / 'memory' / 'memory.json'

memory = load_memory(target_file)

while True:
    command = input('Waiting for your next command: >').lower().strip()
    if command == 'add task':
        add_task(memory)
    elif command == 'view tasks':
        view_tasks(memory)
    elif command == 'status':
        view_status(memory)
    elif command == 'help':
        view_commands(memory)
    elif command == 'exit':
        system_exit(memory, target_file)
        break
    elif command == '':
        print('Whoa there! There was no command entered.')
    else:
        print(f"Sorry {memory['creator']}, but I don't recognize that command :(\nPlease try again.")


