"""
Umderstands language. Parsers commands for execution.
"""

_PREFIXED_COMMANDS = {
    'del task': 'delete_task',
    'run task': 'run_task',
    'run ': 'run',
    'open': 'open_url',
    'search ': 'search',
    'note ': 'note',
    'set name': 'set_name',
    'set city': 'set_city'
}

def parse_commands(raw_command: str):
    text = raw_command.strip()
    lower = text.lower()

    for prefix, cmd_key in _PREFIXED_COMMANDS.items():
        if lower.startswith(prefix):
            argument = text[len(prefix):].strip()
            return cmd_key, argument

    return lower, None