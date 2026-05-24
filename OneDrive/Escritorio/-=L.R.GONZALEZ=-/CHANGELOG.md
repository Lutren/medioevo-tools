# CHANGELOG

## 2026-05-06

- Added root prompt-execution wrappers for MEDIOEVO / CLAUDIO:
  `AUDIT_CLAUDIO.md`, `SECRET_SCAN_REPORT.md`, `IMPLEMENTATION_PLAN.md`,
  `TREE_PLAN.md`, `PRIVATE_BOUNDARY.md`, `RELEASE_CHECKLIST.md`, closure docs
  and folder indices.
- Refreshed local pending-review evidence: `active_dedup=0`,
  `claudio_open=0`.
- Refreshed global secret-scan summary: `count_reported=200`, global workspace
  remains not publishable by broad release.
- Added `TaskManager` to `packages/open-dev/obsai-core` with evidence-gated
  closure and JSON persistence.
- `obsai-core` tests pass: `29 passed in 1.13s`.
- `obsai-core` focused secret scan remains clean: `count_reported=0`.
- No private paths, publish/deploy targets, moves or deletes were changed in
  this cycle.
