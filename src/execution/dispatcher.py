"""
Receives a target action string (e.g. "spotify", "https://x.com") and decides
whether the Applications module or the Browser module should handle it.
Nothing about *how* to launch things lives here -- only the routing.

Eventually: Email module, Music module, AI module all plug in here.
"""

from execution import applications, browser


def execute_app(target_action: str) -> bool:
    action = target_action.lower().strip()
    return applications.launch_application(action)


def execute_url(target_action: str) -> bool:
    action = target_action.lower().strip()
    return browser.open_target_url(action)


def execute_action(target_action: str) -> bool:
    action = target_action.lower().strip()

    if action.startswith('open '):
        return execute_url(action[5:].strip())

    if action.startswith('run '):
        return execute_app(action[4:].strip())

    if applications.launch_application(action):
        return True
    if browser.try_handle(action):
        return True
    return False
