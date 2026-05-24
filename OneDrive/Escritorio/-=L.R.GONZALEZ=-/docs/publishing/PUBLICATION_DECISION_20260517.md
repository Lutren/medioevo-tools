# Publication Decision - 2026-05-17

Run: RUN_PUBLIC_SAFE_MEDIOEVO_UPDATE_20260517

## Decision

Proceed with a public-safe update only.

## Approved Public Scope

- High-level MEDIOEVO / OSIT status update.
- DUAT evidence panel v0.4 summary.
- Smallville-DUAT synthetic simulation summary.
- OSIT runtime architecture summary.
- Canon Tripartito v1.0.1 local active status.
- Fragmentos DOCX QA status.

## Explicitly Not Published

- Complete canon.
- Manuscript or book contents.
- Private runtime internals.
- Private datasets.
- Private prompts.
- Credentials or local configuration.
- Private game material.
- Claims of real-world prediction or scientific proof.

## Gate Evidence

- Public-safe packet: created.
- SecretScan: PASS, findings_count=0.
- BoundaryScan: PASS_PUBLIC_SAFE.
- ScienceClaimGate: PASS_PUBLIC_SAFE.
- RemoteComputeGate: BLOCK_THIS_RUN.
- COMMSLiveGate: BLOCK_THIS_RUN.

## Rollback Plan

- GitHub: revert the public-safe update commit or close the branch/PR.
- Site: revert the update page commit or redeploy the previous build.
- LinkedIn: edit or delete the post if a boundary issue is later discovered.
- Local evidence: preserve append-only reports.
