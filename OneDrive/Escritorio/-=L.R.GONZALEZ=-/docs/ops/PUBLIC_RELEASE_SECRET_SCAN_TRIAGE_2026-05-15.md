# Public Release Secret Scan Triage - 2026-05-15

StateFingerprint: AUTONOMIA-8H-PUBLIC-SAFE-20260515-8F2A  
TriageFingerprint: PUBLIC-SECRET-TRIAGE-20260515-4FINDINGS  
PublicationGate: BLOCK  
CommitGate: REVIEW

## Scope

This triage covers only the four findings reported by:

`python tools\release\scan_secrets.py --path publish_staging\medioevo-duat-public-release --json`

No publish, deploy, push, LinkedIn, Gumroad or KDP action was executed.

## Scanner Behavior

The root scanner reported `secret-like filename` when a file path or filename contained markers such as `secret` or `token`. The four reported files had filename/path markers only. Content evidence was checked separately with the same content-marker family used by the scanner plus local-path and strong-claim checks.

Remediation added a path-exact allowlist in `tools/release/scan_secrets.py`. It suppresses only the filename reason for the four exact public-release paths and the required triage artifacts whose filenames include `SECRET_SCAN`. Content scanning remains active.

## Findings

| finding_id | path | detector | classification | secret value | private path | strong claim | action |
|---|---|---|---|---|---|---|---|
| F1 | `publish_staging/medioevo-duat-public-release/08_QA_WITNESSLOG/SECRET_SCAN_RESULTS.json` | `secret-like filename` | `FALSE_POSITIVE_FILENAME_ONLY` | no | no | no | path-exact filename allowlist |
| F2 | `publish_staging/medioevo-duat-public-release/08_QA_WITNESSLOG/SECRET_SCAN_RESULTS.md` | `secret-like filename` | `FALSE_POSITIVE_FILENAME_ONLY` | no | no | no | path-exact filename allowlist |
| F3 | `publish_staging/medioevo-duat-public-release/public/prompts/02_ahorro_tokens_extremo.md` | `secret-like filename` | `FALSE_POSITIVE_FILENAME_ONLY` | no | no | no | path-exact filename allowlist |
| F4 | `publish_staging/medioevo-duat-public-release/public_release_package/public/prompts/02_ahorro_tokens_extremo.md` | `secret-like filename` | `FALSE_POSITIVE_FILENAME_ONLY` | no | no | no | path-exact filename allowlist |

## Evidence Summary

Each file was checked for:

- scanner content patterns: 0 hits
- local private path patterns: 0 hits
- unbounded strong public claim literals: 0 hits

Final scan:

`python tools\release\scan_secrets.py --path publish_staging\medioevo-duat-public-release --json`

Result: `count_reported=0`.

Final release audit:

`python scripts\release_audit_public.py --json`

Result: `status=PASS`, `secret_block=false`, `reconstruction=true`, `package_files=162`.

## Hashes

| path | before | after |
|---|---|---|
| `publish_staging/medioevo-duat-public-release/08_QA_WITNESSLOG/SECRET_SCAN_RESULTS.json` | `FCABD5FE6CF3C7166221B2C9A96760AD1EB4D7C783E4AF093A8C052DC1F605E3` | `FCABD5FE6CF3C7166221B2C9A96760AD1EB4D7C783E4AF093A8C052DC1F605E3` |
| `publish_staging/medioevo-duat-public-release/08_QA_WITNESSLOG/SECRET_SCAN_RESULTS.md` | `FB95414A1AD589EABE9AA32E2DE89E21B4B0EF915CB7AF8920B36E98164F1F52` | `FB95414A1AD589EABE9AA32E2DE89E21B4B0EF915CB7AF8920B36E98164F1F52` |
| `publish_staging/medioevo-duat-public-release/public/prompts/02_ahorro_tokens_extremo.md` | `393B4BB2D9869297DAEE6FB5701549D83FAA4A5A427FAAF92BB4253F9EE95668` | `393B4BB2D9869297DAEE6FB5701549D83FAA4A5A427FAAF92BB4253F9EE95668` |
| `publish_staging/medioevo-duat-public-release/public_release_package/public/prompts/02_ahorro_tokens_extremo.md` | `393B4BB2D9869297DAEE6FB5701549D83FAA4A5A427FAAF92BB4253F9EE95668` | `393B4BB2D9869297DAEE6FB5701549D83FAA4A5A427FAAF92BB4253F9EE95668` |
| `tools/release/scan_secrets.py` | changed | `1EB221CCBDBDFD2A0FAC95D73413BFB681A2F059DC55C97B8603C82FF8B0530F` |
| `publish_staging/medioevo-duat-public-release/scripts/release_audit_public.py` | changed | `26582B3C6D65873B303580EE806BD02E38B4F9BCDC87DA528C226FAB442D8C45` |

## Decision

The four findings are closed as `FALSE_POSITIVE_FILENAME_ONLY`.

Publication remains blocked because the worktree/diff is mixed with prior changes and external publication is explicitly out of scope for this round.
