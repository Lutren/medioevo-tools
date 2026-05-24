# Next Technical Run - Execute Local v0.2

## Mission

Implement Local Execute v0.2 for Claudio/Wabi after the public Hub follow-up is closed.

## Rules

- Local only.
- No cloud LLM.
- No NVIDIA smoke.
- No publication.
- No direct delete.
- No execution without TaskSpec.
- No execution without ActionGate and GhostGate.
- No apply without rollback snapshot.
- No writes outside sandbox or documentation allowlist.
- WitnessLog append-only.

## Minimum Flow

1. Load pending task.
2. Create TaskSpec.
3. Evaluate ActionGate.
4. Run GhostGate.
5. Validate target allowlist.
6. Create rollback snapshot.
7. Apply only if all gates pass.
8. Run tests or verification.
9. Roll back if verification fails.
10. Append WitnessLog and update handoff.

## Acceptance Criteria

- Execute is blocked without TaskSpec.
- Execute is blocked without GhostGate PASS.
- Execute is blocked without rollback.
- Apply is limited to sandbox/docs allowlist.
- Failed verification triggers rollback.
- Successful run records WitnessLog.
- No cloud, no NVIDIA, no public side effect.
