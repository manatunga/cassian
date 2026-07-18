"""
Primary execution file for Cassian
"""

# Import dependencies
import os
import json


# Function to load Cassian's memory
def load_memory():
    if os.path.exists('memory.json'):
        print('Loading memory...')
        with open('memory.json', 'r') as file:
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
def add_task ():
    task = input('Enter the task on the queue: >').lower()
    memory['task_queue'].append(task)
    if task in memory['task_queue']:
        print(f'Task, "{task}", has been added to queue.')
    else:
        print(f'Oops! Error occured when adding your task, "{task}"')


# Function to view the task queue
def view_tasks():
    if len(memory['task_queue']) == 0:
        print('No tasks on queue.')
    else:
        print('\nHere are all the tasks currently in my system queue:\n')
        for index, task in enumerate(memory['task_queue']):
            if index == 0:
                print(f'Current Task:  {task}')
            elif index == 1:
                print(f'Next Task:  {task}\n')
            else:
                print(f"Task {memory['task_queue'].index(task) + 1}:  {task}")
        print('')


# Function to view the system's status
def view_status():
    print('\nHere is my current system metrics:\n')
    print(f"\tSystem Name:  {memory['system_name']}")
    print(f"\tCreator:  {memory['creator']}")
    print(f"\tBoot Count:  {memory['boot_count']}")
    print('')


# Function to exit Cassian
def system_exit():
    print('Updating memory...')
    with open('memory.json', 'w') as file:
        json.dump(memory, file, indent=4)
        print('Memory has been successfully updated.')
    print(f"Have a nice day, {memory['creator']}!")


# Function to view commands
def view_commands():
    print('\nHere is a list of all the commands that I recognize:\n')
    print(f"\tadd task  - {memory['commands']['add task']}")
    print(f"\tview tasks  - {memory['commands']['view tasks']}")
    print(f"\tstatus  - {memory['commands']['status']}")
    print(f"\thelp  - {memory['commands']['help']}")
    print(f"\texit  - {memory['commands']['exit']}")
    print('')



# Pre-initialization message
print('Initializing Cassian...')

# Boot up Cassian and load his memory
memory = load_memory()
while True:
    command = input('Waiting for your next command: >').lower()
    if command == 'add task':
        add_task()
    elif command == 'view tasks':
        view_tasks()
    elif command == 'status':
        view_status()
    elif command == 'help':
        view_commands()
    elif command == 'exit':
        system_exit()
        break
    else:
        print(f"Sorry {memory['creator']}, but I don't recognize that command :(\nPlease try again.")


