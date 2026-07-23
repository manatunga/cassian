# Cassian Engineering Handbook

This handbook documents the design philosophy, coding standards, and contribution rules for developing Cassian.

---

## 1. Core Philosophy & Design Principles

1. **Strict Separation of Concerns:**
   - Handlers do not execute process calls directly.
   - Execution dispatchers do not format terminal output directly.
   - UI utilities do not manipulate memory state.

2. **Zero Pain Additions:**
   - Adding a new command should only require:
     1. Adding a parser rule in `src/commands/parser.py`.
     2. Writing the handler function in `src/commands/handlers.py`.
     3. Mapping the key in `src/commands/registry.py`.

3. **Graceful Failures over Crashes:**
   - External services (e.g., geocoding or weather telemetry) must always catch network errors/timeouts and fall back to sane defaults instead of throwing unhandled exceptions to the user.

4. **Privacy & Security First:**
   - Raw passwords must **never** be saved to disk in plain text. Always pass user inputs through `profile.hash_password()` before persisting to `memory.json`.

---

## 2. Code Conventions

### Python Style & Standards
* Follow **PEP 8** style guidelines where applicable.
* Use **explicit type hints** for function signatures:
  `def city_to_coordinates(city_name: str) -> tuple[float, float] | None:`
* Prefer **relative imports** within internal packages (e.g., `from core.constants import GREEN`) or clean package imports.

### Terminal Output Standards
* Do **not** use raw `print()` statements for system messages or warnings. Use the standard `ui.terminal` helpers:
  - `terminal.print_info(...)` for status updates.
  - `terminal.print_success(...)` for completed actions.
  - `terminal.print_warning(...)` for missing inputs or soft failures.
  - `terminal.print_error(...)` for hard errors.

---

## 3. Extending Cassian

### Adding a New Application Mapping
To support a new desktop app for `run <app>`:
1. Open `config/applications.json`.
2. Add the process keyword or system protocol to the respective OS map. Do **not** hardcode executable paths in `execution/applications.py`.

Example entry in `config/applications.json`:
"processes": {
    "editor": {
        "windows": ["notepad.exe"],
        "mac": ["open", "-a", "TextEdit"],
        "linux": ["gedit", "kate", "nano"]
    }
}

---

## 4. Testing & Pull Request Checklist

Before submitting code or tagging a release:
- [ ] Ensure fresh boot sequence works when `data/memory.json` is deleted.
- [ ] Confirm passwords are required for sensitive modifications (`set name`, `set city`).
- [ ] Verify `run <app>` only launches local processes and rejects HTTP URLs.
- [ ] Verify `open <url>` launches browser targets cleanly.
- [ ] Run test scripts under `test/` to check for regression bugs.