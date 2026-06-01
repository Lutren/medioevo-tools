# MIGRATION_LOG

## 2026-05-31 - Wabi-Sabi consolidation: BRAIN_OS como tronco canónico

ActionGate: `APPROVE` para consolidación documental y archivo de legacy.

Canon confirmado: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\wabi_sabi` y `core/wabi*.py` son el runtime activo.

| source | destination | reason |
|---|---|---|
| `apps/local/wabi-sabi/` | `_archive/legacy/wabi-sabi-legacy-2026-05-31/` | generación anterior (52 entries, 744 files); activo canónico en BRAIN_OS |
| `scripts/wabi_sabi_startup.ps1` | `_archive/legacy/wabi-sabi-legacy-2026-05-31/scripts/` | refería al legacy |
| `scripts/wabi_sabi_startup.cmd` | `_archive/legacy/wabi-sabi-legacy-2026-05-31/scripts/` | refería al legacy |

Rollback: mover `_archive/legacy/wabi-sabi-legacy-2026-05-31/` de vuelta a `apps/local/wabi-sabi/`.

## 2026-05-16 - Wabi-Sabi canonical route absorption

ActionGate: `APPROVE` for local archive move after canonical copies and wrapper
updates.

Canonical route:

`apps/local/wabi-sabi`

Moved to archive, not deleted:

| source | destination | reason |
|---|---|---|
| `adapters/` | `_archive/legacy/wabi-sabi-external-2026-05-16/adapters/` | adapter implementation absorbed into `apps/local/wabi-sabi/adapters/` |
| `config/models.wabisabi.yaml` | `_archive/legacy/wabi-sabi-external-2026-05-16/config/models.wabisabi.yaml` | non-secret model profile absorbed into `apps/local/wabi-sabi/config/` |
| `config/models.wabisabi_extra.yaml` | `_archive/legacy/wabi-sabi-external-2026-05-16/config/models.wabisabi_extra.yaml` | non-secret model profile absorbed into `apps/local/wabi-sabi/config/` |

Wrappers retained:

- `scripts/select_model.ps1` now reads `apps/local/wabi-sabi/config/models.wabisabi.yaml`.
- `scripts/wabi_sabi_startup.ps1` now uses `apps/local/wabi-sabi/adapters` and
  `apps/local/wabi-sabi/runtime/logs`.
- `README_WABISABI.md` is a redirect to the canonical route.

Boundaries:

- No source was deleted.
- No secrets or secret loaders were copied.
- No publication, deploy, push or external action was performed.