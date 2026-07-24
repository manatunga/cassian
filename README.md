# Cassian

Cassian is a personal, terminal-based AI operating layer — a JARVIS/Cortana/Samantha-inspired
assistant that starts as a command-driven Python engine and grows, phase by phase, into a
full "companion" system with voice, memory, and an embedded presence.

## Status

`v1.0.1` — Cassian Terminal Assistant (v1): Debugged "run" command bug.

## Architecture at a Glance

```
User → UI → Command Parser → Registry → Handlers → Dispatcher → Execution / Services → Memory
```

Every layer only talks to the layer directly beneath it. For full breakdown of the modular design, check `docs/Architecure.md`.

## Key Features (`v.1.0`)

- **Interactive Onboarding:** First-time boot automatically initiates profile setup (Name, City location, and hashed password security).
- **Location & Geocoding:** Automatically resolves city names into coordinates via geopy for weather and telemetry context.
- **Separated Execution Dispatcher:** Strict distinction between launching local desktop applications (run <app>) and browser URLs (open <url>).
- **Prioritized Task Queue:** Add, inspect, run, and delete prioritized queue items.
- **Telemetry & Environment:** Live local temperature polling via Open-Meteo API.
- **Persistent Notes:** Quick note recording saved directly to Cassian's JSON memory.
- **Self-Healing Schema:** Automated migrations keep legacy memory files compatible with updated schema structures.

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/manatunga/cassian.git
cd cassian
```

2. Set up virtual environment and dependencies:
```bash
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Launch Cassian:
```bash
python src/main.py
```

## Command Reference

| Command | Syntax | Description |
| :--- | :--- | :--- |
| **Run App** | `run <app_name>` | Spawns local binaries/apps (e.g., `run calc`, `run spotify`) |
| **Open URL** | `open <url>` | Navigates directly to web domains in Chrome/default browser |
| **Search** | `search <query>` | Performs a Google search query in browser |
| **Set Profile** | `set name <name>` / `set city <city>` | Password-authenticated user metadata updates |
| **Task Queue** | `add task`, `view tasks`, `del task <id>` | Manage prioritized tasks |
| **Notes** | `note <text>`, `view notes` | Record and list quick notes |
| **System** | `status`, `temp`, `clear`, `help` | View system metrics, weather telemetry, or command index |

## Repository Structure

```
cassian/
├── config/       # Process mappings & defaults
├── data/         # User memory and logs
├── docs/         # Architectural notes & development guides
└── src/
    ├── commands/ # Language parser, registry, and handlers
    ├── core/     # Bootstrap sequence and engine loop
    ├── execution/# Application processes & browser dispatchers
    ├── memory/   # Profile storage & task queue managers
    ├── services/ # Location geocoding & telemetry services
    ├── ui/       # Terminal formatting and banners
    └── utils/    # OS detectors & validators
```

## Roadmap

1. **The Workshop** (v0.x → v1.0) — solidify the core engine, command system, memory.
2. **The Household Mind** (v1.x → v2.0) — richer services, smarter task handling.
3. **The Operator** (v2.x → v3.0) — proactive automation.
4. **The Embedded Layer** (v3.x → v4.0) — voice, always-on presence.
5. **The Companion** (v4.x → v5.0) — full conversational companion.

## Contributing

This is currently a solo project. Design notes and rationale live in
`docs/Engineering Handbook.md` — please read that before modifying `src/core/`.
