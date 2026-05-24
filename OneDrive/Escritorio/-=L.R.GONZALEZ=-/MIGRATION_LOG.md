# MIGRATION_LOG

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
