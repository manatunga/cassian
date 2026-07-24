# Cassian System Architecture 

This document details the high-level architecture, module boundaries, data flow, and design patterns used across Cassian.

---

## 1. System Overview

Cassian is designed as a **strictly layered, decoupled operating layer**. No layer is allowed to skip over adjacent layers to call underlying logic.

### High-Level Component Flow

```text
User Input
    │
    ▼
[ UI Layer ] (ui/terminal.py, ui/banner.py, ui/prompts.py)
    │
    ▼
[ Command Parser ] (commands/parser.py)
    │
    ▼
[ Command Registry ] (commands/registry.py)
    │
    ▼
[ Command Handlers ] (commands/handlers.py)
    │
    ├──► [ Memory Manager ] (memory/manager.py, memory/profile.py, memory/tasks.py)
    │
    └──► [ Execution Dispatcher ] (execution/dispatcher.py)
            │
            ├──► [ Applications Module ] (execution/applications.py)
            │       └──► System Process / Protocol Handlers
            │
            └──► [ Browser Module ] (execution/browser.py)
                    └──► Chrome / Default Web Browser
```

## 2. Directory & Module Responsibilities

| Path | Module | Primary Responsibility |
| :--- | :--- | :--- |
| `src/core/` | **Engine & Boot** | Main initialization, loop lifecycle, and global system constants. |
| `src/ui/` | **User Interface** | Output formatting, ANSI colors, banners, and interactive prompts. |
| `src/commands/` | **Command Router** | Parses raw strings, maps keys to functions, and delegates work to handlers. |
| `src/execution/` | **Dispatcher & Actions** | Spawns local desktop OS binaries (`run`) or handles browser navigation (`open`). |
| `src/services/` | **External Integrations** | Geocoding (`geopy`), weather telemetry, and future API integrations. |
| `src/memory/` | **State & Persistence** | Schema management, JSON persistence, profile password verification, and task queues. |
| `src/utils/` | **Cross-Cutting Utilities** | Platform detection (Windows/Mac/Linux) and string/index validation. |

## 3. Key Execution Flows

### A. First-Time Boot Sequence

1. `src/main.py` launches `run_boot_sequence()`.
2. `MemoryManager` checks for `data/memory.json`.
3. If absent:
   - Triggers interactive profile setup (asks for Name, City, and Password).
   - `services.location.city_to_coordinates()` queries `geopy` for lat/lon.
   - Hashes password using `SHA-256` and writes `memory.json`.

### B. Command Execution (`run` vs. `open`)

- `run <app>`: `parser.py` extracts key `'run'` → `handlers.run_direct()` → `dispatcher.execute_app()` → matches binary in `config/applications.json` and spawns process via `subprocess.Popen`.
- `open <url>`: `parser.py` extracts key `'open_url'` → `handlers.open_url_cmd()` → `dispatcher.execute_url()` → `browser.open_target_url()` launches default system browser.

## 4. State & Memory Management

All states persists in `data/memory.json`.

### Schema Structure (`v.1.0.0`)
```json
{
    "system_name": "Cassian",
    "version": "1.0.0",
    "user": "User Name",
    "boot_count": 1,
    "location": {
        "city": "London",
        "lat": 51.5074,
        "lon": -0.1278
    },
    "auth": {
        "password_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    },
    "notes": [],
    "commands": {},
    "task_queue": []
}
```
- Self-Healing Migrations: On load, `MemoryManager._migrate_schema()` injects any missing keys or defaults into legacy memory files without wiping user data.
