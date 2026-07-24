"""
Stores every available command as a lookup table FOR CASSIAN.
For command index that is shown to users, see COMMAND_INDEX in core.constants

Adding a new command means adding one line here plus one
function in handlers.py -- not touching the main loop in core/engine.py.
"""

from commands import handlers

def build_registry() -> dict:
   return {
           'add task': handlers.add_task,
           'view tasks': handlers.view_tasks,
           'delete_task': handlers.delete_task,
           'clear tasks': handlers.clear_tasks,
           'set_name': handlers.set_name,
           'set_city': handlers.set_city,
           'status': handlers.view_status,
           'help': handlers.view_commands,
           'exit': handlers.exit_system,
           'clear': handlers.clear_screen_cmd,
           'temp': handlers.temp_cmd,
           'run_task': handlers.run_task,
           'execute': handlers.run_task,
           'run': handlers.run_direct,
           'open_url': handlers.open_url_cmd,
           'search': handlers.search_cmd,
           'note': handlers.note_cmd,
           'view notes': handlers.view_notes,
       } 