"""
Implements each command. Each command is its own function: status(), help(),
clear(), telemetry(), etc. Handlers receive the running CassianCore instance
(for memory + shared services) and an optional argument parsed by parser.py.
"""

import getpass
from memory import tasks, profile
from core.constants import CYAN, MAGENTA, RESET
from services.location import city_to_coordinates
from execution.dispatcher import execute_action
from services.telemetry import fetch_environment_reading
from utils.validators import is_valid_task_index, parse_priority
from ui import prompts, terminal


#-----------------------------------------
# ---------- Settings / Profile ----------
#-----------------------------------------

def set_name(core, new_name: str):
    if not new_name:
        terminal.print_warning("I'm afraid name cannot be empty.\n")
        return

    pwd_input = getpass.getpass(f"{MAGENTA}Enter your password to authorize this change: {RESET}")
    if not profile.verify_password(core.memory, pwd_input):
        terminal.print_error("Acess denied: Incorrect password.\n")
        return

    profile.update_user_name(core.memory, new_name.capitalize())
    core.memory_manager.save(core.memeory)
    terminal.print_success(f"User name updated successfully to '{new_name}'.\n")


def set_city(core, new_city: str):
    if not new_city:
        terminal.print_warning("I'm afraid city cannot be empty.\n")
        return

    pwd_input = getpass.getpass(f"{MAGENTA}Enter your password to authorize this change: {RESET}")
    if not profile.verify_password(core.memory, pwd_input):
        terminal.print_error("Acess denied: Incorrect password.\n")
        return

    terminal.print_info(f"Resolving coordinates for '{new_city}'...")
    coords = city_to_coordinates(new_city)

    if not coords:
        terminal.print_error(f"Could not resolve coordinates for '{new_city}'. City location was not updated.")
        return

    profile.update_user_city(core.memory, new_city.capitalize(), coords[0], coords[1])
    core.memory_manager.save(core.memory)
    terminal.print_success(f"City updated to '{new_city}' (Lat: {coords[0]}, Lon: {coords[1]}).\n")


# ------------------------------------------
# ---------- Task Queue Functions ----------
#-------------------------------------------

def add_task(core, _argument=None):
    adding_tasks = True
    while adding_tasks:
        task = prompts.ask('Enter the task description: ')

        if task == '':
            terminal.print_warning(f"{core.memory['user']}, no task was entered.")
        elif task == 'back':
            break
        else:
            p_input = prompts.ask(
                'Set priority - (1) High, (2) Medium, (3) - Low  [Default = 2]: '
            )
            priority = parse_priority(p_input)

            tasks.add_task_entry(core.memory, task, priority)
            core.memory_manager.save(core.memory)
            terminal.print_success(f'Task "{task}" [Priority: {priority}] queued successfully.')

        adding_tasks = prompts.confirm('Add another task?')

    terminal.print_success('Task queue updated and soreted by priority.')


def view_tasks(core, _argument=None):
    queue = core.memory['task_queue']
    if not queue:
        terminal.print_warning('There are currently no tasks in queue.')
        return

    terminal.print_header('ACTIVE TASK QUEUE (BY PRIORITY)')
    from core.constants import RED, CYAN, GREEN, RESET
    p_labels = {1: f"{RED}[HIGH]{RESET}", 2: f"{CYAN}[MED]{RESET}", 3: f"{GREEN}[LOW]{RESET}"}

    for index, item in enumerate(queue):
        p_tag = p_labels.get(item['priority'], '[MED]')
        task_desc = item['task']
        if index == 0:
            print(f"{GREEN}TOP TASK (1):{RESET}\t{p_tag} {task_desc}\n")
        else:
            print(f"Task {index + 1}:\t{p_tag} {task_desc}")
    print('')


def delete_task(core, index_str):
    queue = core.memory['task_queue']
    if not queue:
        terminal.print_warning('No tasks available to delete.\n')
        return

    if not is_valid_task_index(index_str, len(queue)):
        if index_str.strip().lstrip('-').isdigit():
            terminal.print_warning(
                f"Invalid task number. There are only {len(queue)} task/s in queue."
            )
            if prompts.confirm('Do you want to view tasks currently in queue?'):
                view_tasks(core)
        else:
            terminal.print_warning("Please provide a valid task number (e.g., 'delete task 1').\n")
        return

    removed = tasks.remove_task_at(core.memory, int(index_str) - 1)
    core.memory_manager.save(core.memory)
    terminal.print_success(f'Successfully deleted task: "{removed["task"]}"\n')


def clear_tasks(core, _argument=None):
    if not core.memory['task_queue']:
        terminal.print_warning('Task queue is already empty.\n')
        return

    if prompts.confirm('Are you sure you want to clear all tasks?'):
        tasks.clear_all_tasks(core.memory)
        core.memory_manager.save(core.memory)
        terminal.print_success('Task queue cleared successfully.\n')
    else:
        terminal.print_info('Operation cancelled.\n')


def run_task(core, _argument=None):
    current = tasks.top_task(core.memory)
    if current is None:
        terminal.print_warning('There are currently no tasks in queue.\n')
        return

    from core.constants import CYAN, MAGENTA, RESET
    print(f"\n{CYAN}Attempting execution for top priority task:{RESET} {MAGENTA}\"{current['task']}\"{RESET}")

    if execute_action(current['task']):
        completed = tasks.remove_task_at(core.memory, 0)
        core.memory_manager.save(core.memory)
        terminal.print_success(f'Successfully executed task: "{completed["task"]}".')
        terminal.print_info('Removed from queue.\n')
    else:
        terminal.print_warning(f'No automated executable mapped for: "{current["task"]}".')
        terminal.print_info('Leaving task in queue as a manual reminder.\n')


#-------------------------------------------------
# ---------- Direct Execution / Browser ----------
#-------------------------------------------------

def run_direct(core, action_string):
    if not action_string:
        terminal.print_warning("You didn't specify an application to run.")
        return

    from execution.dispatcher import execute_app
    from core.constants import CYAN, MAGENTA, RESET
    print(f"\n{CYAN}Executing application:{RESET} {MAGENTA}\"{action_string}\"{RESET}")

    if execute_app(action_string):
        terminal.print_success('Application spawned successfully.\n')
    else:
        terminal.print_warning(f'Unrecognized application: "{action_string}". Couldn\'t find local executable.\n')


def open_url_cmd(core, url_string):
    if not url_string:
        terminal.print_warning("You didn't specify a URL to open.")
        return

    from execution.dispatcher import execute_url
    print(f"\n{CYAN}Opening URL:{RESET} {MAGENTA}\"{url_string}\"{RESET}")

    if execute_url(url_string):
        terminal.print_success("Browser launched successfully.\n")
    else:
        terminal.print_error(f"Could not open the URL: \"{url_string}\".\n")


def search_cmd(core, query):
    if not query:
        terminal.print_warning('Search query cannot be empty.')
        return

    from execution import browser
    print(f"\n{CYAN}Searching Google for:{RESET} {MAGENTA}\"{query}\"{RESET}")
    browser.search_google(query)
    terminal.print_success('Browser tab launched successfully.\n')


#----------------------------
# ---------- Notes ----------
#----------------------------

def note_cmd(core, note_text):
    if not note_text:
        terminal.print_warning('Cannot add an empty note.\n')
        return
    core.memory['notes'].append(note_text)
    core.memory_manager.save(core.memory)
    terminal.print_success('Note saved successfully.\n')


def view_notes(core, _argument=None):
    notes = core.memory.get('notes')
    if not notes:
        terminal.print_warning('No saved notes found.\n')
        return

    terminal.print_header('SAVED NOTES')
    from core.constants import MAGENTA, RESET
    for i, note in enumerate(notes, 1):
        print(f"{MAGENTA}[{i}]{RESET} {note}")
    print('')


#----------------------------------
# ---------- System/Meta ----------
#----------------------------------

def view_status(core, _argument=None):
    terminal.print_header('SYSTEM METRICS')
    from core.constants import CYAN, MAGENTA, GREEN, RESET
    memory = core.memory
    print(f"\tSystem Name:\t{CYAN}{memory['system_name']}{RESET}")
    print(f"\tVersion:\t{MAGENTA}{memory['version']}{RESET}")
    print(f"\tUser Name:\t{MAGENTA}{memory['user']}{RESET}")
    print(f"\tBoot Count:\t{GREEN}{memory['boot_count']}{RESET}")
    print('')


def view_commands(core, _argument=None):
    terminal.print_header('COMMAND INDEX')
    from core.constants import MAGENTA, RESET
    for cmd, desc in core.memory['commands'].items():
        print(f"\t{MAGENTA}'{cmd}'{RESET} - {desc}")
    print('')


def clear_screen_cmd(core, _argument=None):
    from ui import banner
    terminal.clear_screen()
    banner.print_banner(core.memory.get('version', core.version))


def temp_cmd(core, _argument=None):
    terminal.print_info('Polling remote telemetry grid...')
    reading, error = fetch_environment_reading(core.memory)

    if error:
        terminal.print_error(error)
        return

    from core.constants import CYAN, GREEN, RESET
    temp = reading["current"]["temperature_2m"]
    unit = reading["current_units"]["temperature_2m"]
    terminal.print_success('Network transmission complete. Reading processed.\n')
    print(f"{CYAN}Current Environment Temperature:{RESET} {GREEN}{temp}{unit}{RESET}\n")


def exit_system(core, _argument=None):
    core.exit()