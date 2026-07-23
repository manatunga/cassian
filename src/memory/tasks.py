"""
All related executions related to Cassian's task queue: add, remove, sort, search.
"""

def sort_by_priority(memory: dict):
    memory['task_queue'].sort(key=lambda item: item['priority'])

def add_task_entry(memory: dict, task: str, priority: int):
    memory['task_queue'].append({'task': task, 'priority': priority})
    sort_by_priority(memory)

def remove_task_at(memory: dict, index: int):
    return memory['task_queue'].pop(index)

def clear_all_tasks(memory: dict):
    memory['task_queue'] = []

def top_task(memory: dict):
    if not memory['task_queue']:
        return None
    return memory['task_queue'][0]