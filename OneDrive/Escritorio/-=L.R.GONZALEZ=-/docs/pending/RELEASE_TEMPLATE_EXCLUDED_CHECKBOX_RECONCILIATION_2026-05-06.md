# Release Template Excluded Checkbox Reconciliation - 2026-05-06

## Decision

Some open checkboxes remained in release-template or excluded paths after the
active pending tracker was reduced to the 19 true blockers. These files are
excluded from `pending_review.py` by design, but their unchecked syntax still
looked like live work in broad markdown scans.

They were converted to explicit gate markers. This does not mean the release
requirements are complete.

## Reconciled Sources

| source | action |
|---|---|
| `docs\release\RELEASE_READINESS_SCORE.md` | open release gates converted to `release-template-gate` |
| `docs\release\RELEASE_CHECKLIST.md` | template checklist items converted to `release-template-gate` |
| `docs\release\MANUAL_QA_CHECKLIST.md` | manual QA template items converted to `release-template-gate` |
| `docs\release\APP_STORE_READINESS.md` | app-store template items converted to `release-template-gate` |
| `apps\commercial\flujocrm\installer\BUILD.md` | verified audit/scans marked done; remaining sale/publication items converted to `flujocrm-release-gate` |
| `apps\commercial\argus-desktop\STATUS.md` | stale placeholder next actions converted to `argus-status-gate` |

## Verified FlujoCRM Checks

- `npm audit --omit=dev --audit-level=high`: `found 0 vulnerabilities`.
- `python tools\release\scan_secrets.py --path apps\commercial\flujocrm --json --fail-on-findings`: `count_reported=0`.
- `python tools\release\scan_secrets.py --artifact apps\commercial\flujocrm\dist\win-unpacked\FlujoCRM.exe --json --fail-on-findings`: `count_reported=0`.

## Boundary

No installer rebuild, clean-VM test, Gumroad edit, website CTA change, deploy or
public sale was executed. The active source of truth for current blockers remains
`docs\pending\ACTIVE_BLOCKERS_GATE_STATUS_2026-05-06.md`.

