# GAME_OS_ARCHITECTURE_v1_3

Fingerprint: DUAT-v1.3-GAME-OS-DISK-FORENSICS-LANGUAGE-CORTEX

DUAT v1.3 adds a game operating system layer on top of the existing playable Pixel Realism Engine.

## Architecture

- Simulation state remains outside the renderer.
- DOM panels handle mode/UI/language/brain surfaces.
- Canvas remains the playfield.
- Game mode state is serializable and local.
- Language Cortex is deterministic template/rule logic; no external LLM/API.
- Brain Runtime coordinates subsystems but never enables Wabi execution.
- Disk/zip forensics are metadata-only and staging-safe.

## Boundaries

- No push, deploy, commit, cloud or MCP execution.
- No unknown zip code executed.
- No assets copied to runtime/public use.
- publication_allowed=false.
- Wabi execution remains false.
- Cosmology is in-world lore/formal-lab only, not real science.
