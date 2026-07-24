"""
Constants used throughout Cassian's system.
Meant to be immutable, unchangeable.
"""

# ---------- System Identity ----------
APP_NAME = 'Cassian'
VERSION = '1.0.1'

# ---------- ANSI Color Codes for Terminal UI Styling ----------
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# ---------- Fallback Defaults (if config/defaults.json is missing) ----------
DEFAULT_LOCATION = {"lat": 6.84, "lon": 79.92}
DEFAULT_CREATOR = 'Jan'

# ---------- Command Index shown to user ----------
COMMAND_INDEX = {
    'add task': 'to add a prioritized task to queue', 
    'view tasks': 'to view all tasks sorted by priority', 
    'del task <num>': 'to remove a task by index',
    'clear tasks': 'to wipe all queued tasks',
    'set name <new name>': 'to change your name',
    'set city <new city>': 'to change your city',
    'run task': 'to execute top priority task',
    'run <app>': 'to execute an app directly',
    'open <url>': 'to open a URL immediately via Google',
    'search <query>': 'to search Google directly in Chrome',
    'note <text>': 'to record a quick persistent note',
    'view notes': 'to view all saved notes',
    'status': 'to view system metrics',
    'temp': 'to fetch live environmental weather data', 
    'help': 'to view command index', 
    'clear': 'to clear terminal',
    'exit': 'to exit the system' 
}