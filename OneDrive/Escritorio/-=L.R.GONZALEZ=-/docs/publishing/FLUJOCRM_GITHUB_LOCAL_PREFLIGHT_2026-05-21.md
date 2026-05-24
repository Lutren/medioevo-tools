# FlujoCRM GitHub Local Preflight - 2026-05-21

Scope: local-only review of `publish_staging\github\flujocrm-free-review`.
No GitHub remote, push, deploy, publication or website change was executed.

## Result

- License readiness: `publication_ready=true`, `blockers=[]`.
- Secret scan: `count_reported=0`.
- Local check: `npm run check` passed.
- Git state: local staging HEAD `a16c019`, no remote output observed.
- Manifest comparison:
  - manifest files: `16`.
  - actual non-git/non-node_modules files: `21`.
  - missing from disk: `0`.
  - extra review/control files not listed in manifest: `5`.

## Commands

```powershell
python tools\release\audit_flujocrm_free_license_readiness.py --write --json
python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json
npm run check
git -C publish_staging\github\flujocrm-free-review status --short
git -C publish_staging\github\flujocrm-free-review rev-parse --short HEAD
git -C publish_staging\github\flujocrm-free-review remote -v
```

## Evidence

- License report:
  `qa_artifacts\release_validation\flujocrm-free-license-readiness-2026-05-06.json`.
- `npm run check` output:
  - `flujocrm main smoke passed`.
  - `flujocrm preload smoke passed`.
  - `flujocrm renderer smoke passed`.
- Staging install notes exist:
  `publish_staging\github\flujocrm-free-review\CUSTOMER_INSTALL_NOTES.md`.
- Staging publication gate exists:
  `publish_staging\github\flujocrm-free-review\PUBLICATION_GATE.md`.
- Staging source allowlist exists:
  `publish_staging\github\flujocrm-free-review\SOURCE_ALLOWLIST_MANIFEST.json`.

## Manifest Review

The source allowlist manifest covers the release source files and scripts, but
the staging folder also includes five review/control documents:

- `LICENSE`
- `LICENSE_DECISION_REQUIRED.md`
- `PUBLICATION_GATE.md`
- `README_PUBLIC_DRAFT.md`
- `SOURCE_ALLOWLIST_MANIFEST.json`

This is not a publication blocker by itself, but the final GitHub publication
packet should either include these control files intentionally or regenerate the
manifest before push.

## REVIEW_REQUIRED

- Do not run `gh repo create`, `git push`, `gh repo edit`, website updates or
  publication until ActionGate/host gate allow the exact target.
- Re-run secret scan after the public repository exists.
- Verify live GitHub files against the final local manifest after publication.
- Add public-safe screenshots only after visual QA and public-safe media review.
- Confirm website points to the final GitHub URL only after the URL exists.
