# Formal Cleanup Gate - 2026-05-08

## Gate Status

Decision: `BLOCK_DELETE_MOVE_RENAME`

Reason:

- `Formal` has `0` exact duplicates against the current PSI/master/runtime index targets in the first pass; the later `banananana.txt` delta is a secret/config item, not a deletion candidate.
- Several files contain potential unique theory, code, prompts, datasets or visual evidence.
- Unsafe execution sources are evidence and requirements sources; they are not safe to execute, but that does not make them disposable.

## Cleanup Preconditions

A file from `Formal` may enter third-pass deletion only when all conditions are true:

1. Full SHA256 recorded.
2. Canonical destination or explicit discard reason recorded.
3. Evidence that no unique insight, technique, original code, original idea or experimental evidence remains.
4. Claim delta closed or intentionally rejected.
5. Code insight either extracted as contract/test or rejected with reason.
6. Binary/media/archive content rendered or quarantined-intaked if relevant.
7. Entry added to `DELETE_CANDIDATES.md`.
8. Cleanup gate approved after path containment verification.

## Current File Groups

| Group | Files | Cleanup decision |
|---|---:|---|
| Canon/formal candidates | 7 | `KEEP_REVIEW` until excerpt comparison and claim merge decision. |
| Raw/session sources | 20 | `KEEP_REVIEW` until split and no-unique-delta proof. |
| Code insights | 8 | `KEEP_REVIEW` until contract/test comparison with Wabi/Sabi. |
| Experiment evidence | 8 | `KEEP_REVIEW` until dataset/visual evidence is linked or rejected. |
| Blocked execution sources | 4 | `KEEP_EVIDENCE_BLOCK_EXECUTION`; may later archive, not execute. |

## Explicit Blocks

| Source | Block |
|---|---|
| `uno.py` | No host process priority, memory purge, browser kill or infinite monitor loop execution. |
| `nucleo.txt` | No admin/privileged host tuning based on this source. |
| `Para materializar este Pipeline Dir.txt` | No generated shell execution, package install or app launch. |
| `The Solution deploy_overlord.shThis.txt` | No API-key workflow, dependency install or deploy script execution. |

## No-Delete Decision

No file in `C:\Users\L-Tyr\OneDrive\Escritorio\Formal` was added to `DELETE_CANDIDATES.md` in this pass.

## Secret cleanup hold

`banananana.txt` is under `SECRET_CLEANUP_HOLD`.

It may not be deleted, copied or normalized until all of the following exist:

- full SHA256 and owner intent;
- confirmation whether the underlying keys were rotated or remain active;
- redacted replacement path if credentials are needed by Wabi/Sabi or Claudio;
- proof that no unique provider setup note remains in the file;
- explicit cleanup gate approval.

Until then the state is `KEEP_PRIVATE_REDACTED_EVIDENCE`, not archive, not canon, and not trash.

## Next Gate

Next gate is `FORMAL_PASS_2_DELTA_EXTRACTION`:

- Compare canon candidates against master docs and `16_CLAIMS_REGISTER.md`.
- Compare code candidates against Wabi/Sabi runtime contracts.
- Quarantine-intake ZIPs.
- Visual-review PNG/PDF files where a claim depends on a figure.
- Only then nominate specific files for archive/delete review.
