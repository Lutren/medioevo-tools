# Curador Orden Assistant Report

Schema: `wabi.curator_assistant_report.v1`
Workspace: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`
Mode: `dry_run_only`
Gate: `APPROVE`

## Estado seco

- Worktree dirty: `True`
- Status count: `219`
- Candidate count: `120`
- Safe cleanup performed: `False`

## Categorias

- `BOUNDARY_BLOCKED`: 3
- `CONCURRENT_TRACKED_CHANGE`: 36
- `HANDOFF_EVIDENCE`: 6
- `RUNTIME_EVIDENCE`: 2
- `UNTRACKED_REVIEW`: 73

## Reglas para quien trabaje en esta computadora

- Start with status: Run worktree-status or curator-assistant before changing broad folders.
- No broad staging: Never use git add . in this workspace; stage only files owned by the current task.
- No physical cleanup during concurrency: When other agents are active, do not delete, move, revert or rename their files.
- Use evidence folders: Generated outputs go to runtime/outputs, logs to runtime/logs and handoffs to NEXT_SESSION_BRIEF/SESSION_FINGERPRINT.
- Ficha before archive: Unknown material needs a ficha, hash or manifest before archive/delete candidates are trusted.
- Keep private lanes blocked: Game, TCG, secrets, paid content and publication actions stay BLOCK unless a specific gate authorizes them.
- Close with verification: Use claim-contract, project-scan, test-plan and run-safe-tests before claiming a feature is done.

## Primeros candidatos

- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/COMMS/agents_state/publicacion-perfiles-observatorio.json` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/COMMS/outbox/publicacion-perfiles-observatorio.jsonl` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/COMMS/topics/agent-city-coordination.jsonl` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/DELETED_OR_ARCHIVED.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/DUPLICATES_AND_DEAD_CODE.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/metrics.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/SOURCE_INTAKE_REGISTER.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/README.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/REPORT_WABI_SABI_LOCAL_AGENTS.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/docs/ARCHITECTURE.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/docs/USAGE.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/pyproject.toml` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/tests/test_cli.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/tests/test_codex_bridge.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/tests/test_memory.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/wabi_sabi/agents/programmer_agent.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/wabi_sabi/cli/main.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/wabi_sabi/cli/parser.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/wabi_sabi/core/codex_bridge.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/wabi_sabi/core/memory.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/apps/local/wabi-sabi/wabi_sabi/core/programming.py` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/docs/canon/atlas/claudio-wabisabi.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/docs/canon/atlas/curaduria.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/docs/canon/atlas/psi-observacionismo.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`
- `OneDrive/Escritorio/-=L.R.GONZALEZ=-/docs/intake/ATLAS_MAIN.md` -> `CONCURRENT_TRACKED_CHANGE` / `KEEP` / `REVIEW`

## Acciones bloqueadas

- delete files
- move files
- git add .
- git reset, checkout or broad revert
- publish, push, deploy or upload
- inspect or print secret values
- touch private game, TCG or game bridge lanes

## Proxima accion segura

- Crear fichas para los `UNKNOWN_REVIEW_REQUIRED` de mayor valor antes de archivar o borrar.
