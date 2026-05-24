# WABI LOCAL APPLY READINESS 2026-05-19

Fingerprint: `WABI_LOCAL_APPLY_READY_20260519`

## Estado

Wabi ya tiene una ruta local de programacion controlada:

`ConversationEngine -> TaskSpec -> Review -> Gate Preview -> Apply Local Preview -> Apply Local -> SafeExecutor -> RollbackStore -> Tests -> WitnessLog`

El `Apply` legado de TaskSpec sigue bloqueado por diseno. La ruta nueva es explicita:

- CLI: `wabi apply-local-preview --latest --json`
- CLI: `wabi apply-local --latest --json`
- UI: `Apply Local Preview`
- UI: `Apply Local`
- API: `POST /api/taskspec/apply-local-preview`
- API: `POST /api/taskspec/apply-local`

## Gates

- ActionGate: local allowlisted apply only.
- PathAllowlist: `wabi_sabi/**`, `tests/**`, `docs/**` dentro de `apps/local/wabi-sabi`.
- Brain OS UI/API allowlist: `02_CLAUDIO/server/wabi_local_server.py`, `02_CLAUDIO/tests/**`, `apps/local/wabi_ui/**` when the workspace root is BRAIN_OS.
- GhostGate: rollback snapshot required before mutation.
- RollbackStore: snapshot captured by `SafeExecutor` immediately before write.
- TestRunner: allowlisted `python -m pytest` and `python -m py_compile`, including optional `-B`.
- SecretScan: patch content and written files scanned for secret-like values.
- BoundaryScan: patch content and written files scanned for private path markers.
- CloudGate: `cloud_provider_called=false`; NVIDIA remains proposal-only.
- GraphicsGate: `graphics_live=false`.
- PublicationGate: `BLOCK`.

## Real Apply Evidence

The CLI executed a real local apply against the Wabi workspace for a safe JSON helper.

Written files:

- `apps/local/wabi-sabi/wabi_sabi/core/json_safety.py`
- `apps/local/wabi-sabi/tests/test_json_safety.py`

Runtime evidence:

- Patch candidate: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\local_apply\patch_candidate_20260519-224609.json`
- Patch plan: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\local_apply\patch_plans\patch-20260519-224609-6fdd476832d1.json`
- Diff: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\local_apply\patch-20260519-224609-6fdd476832d1.diff`
- Rollback snapshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\rollback\patch-20260519-224609-6fdd476832d1.json`
- Execution report: `C:\Users\L-Tyr\.medioevo\wabi\runtime\executions\patch-20260519-224609-6fdd476832d1.json`
- Witness DB: `C:\Users\L-Tyr\.medioevo\wabi\runtime\witness\wabi_patch_witness.sqlite`
- Witness event: `47`
- Witness chain: `verified=true`

## QA

- Wabi focal: `51 passed`
- BRAIN_OS focal server/UI: `254 passed`
- Wabi post-apply focal: `18 passed`
- Wabi regression: `374 passed`
- BRAIN_OS regression: `764 passed`
- py_compile touched modules: PASS

## Limits

- No arbitrary command execution from UI.
- No cloud output is applied.
- No BrowserBridge live.
- No graphics live.
- No push/deploy was performed.
- Asset publication remains REVIEW because source assets still require provenance and metadata stripping/review.
