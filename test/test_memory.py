"""
Tests for memory/manager.py and memory/tasks.py: saving, loading, migration,
boot count.
"""

import json

from memory import tasks
from memory.manager import MemoryManager
from memory.profile import create_default_memory


def test_create_default_memory_shape():
    memory = create_default_memory("0.9.5")
    assert memory['system_name'] == 'Cassian'
    assert memory['boot_count'] == 1
    assert memory['task_queue'] == []
    assert 'notes' in memory


def test_save_and_load_round_trip(tmp_path):
    filepath = tmp_path / "data" / "memory.json"
    manager = MemoryManager(filepath, "0.9.5")

    memory = manager.load()  # first boot -> creates default
    assert memory['boot_count'] == 1

    reloaded = manager.load()  # second boot -> increments
    assert reloaded['boot_count'] == 2


def test_migration_converts_string_tasks_to_dicts(tmp_path):
    filepath = tmp_path / "data" / "memory.json"
    filepath.parent.mkdir(parents=True)

    legacy_memory = create_default_memory("0.9.0")
    legacy_memory['task_queue'] = ["old string task"]
    with open(filepath, 'w') as f:
        json.dump(legacy_memory, f)

    manager = MemoryManager(filepath, "0.9.5")
    migrated = manager.load()

    assert migrated['task_queue'][0] == {'task': 'old string task', 'priority': 2}


def test_add_and_sort_tasks():
    memory = create_default_memory("0.9.5")
    tasks.add_task_entry(memory, "low priority thing", 3)
    tasks.add_task_entry(memory, "urgent thing", 1)

    assert memory['task_queue'][0]['task'] == "urgent thing"
    assert memory['task_queue'][1]['task'] == "low priority thing"


def test_remove_and_clear_tasks():
    memory = create_default_memory("0.9.5")
    tasks.add_task_entry(memory, "task a", 2)
    tasks.add_task_entry(memory, "task b", 1)

    removed = tasks.remove_task_at(memory, 0)
    assert removed['task'] == "task b"

    tasks.clear_all_tasks(memory)
    assert memory['task_queue'] == []
