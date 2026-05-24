# RPHI_CALIBRATION_v0_1

Status: `LOCAL_ONLY`

## Purpose

Calibration checks whether the deterministic R/Phi budget moves in the expected
direction across controlled local episodes.

This is not external validation. It is a reproducible synthetic harness for
catching regressions before the budget is used on richer local work episodes.

## Episodes

The fixture corpus lives at:

```txt
tests/fixtures/rphi_episodes/
```

It contains:

- `clean_episode`: low residue, high efficiency;
- `missing_evidence_episode`: missing Source Card/evidence signals;
- `contradiction_episode`: contradictory synthetic claims;
- `failed_command_episode`: failed local command outcomes;
- `review_block_episode`: REVIEW/BLOCK-heavy gate events;
- `rollback_success_episode`: reversible write with successful restore;
- `rollback_failure_episode`: restore failure that must trigger BLOCK;
- `stale_memory_episode`: stale memory records;
- `mixed_realistic_sanitized_episode`: bounded local work with mixed residue.

Each episode uses synthetic data only:

- `task_board.json`;
- `witnesslog.jsonl`;
- `memory.json`;
- `command_outcomes.json`;
- `rollback_manifest.json`.

The calibration harness materializes those files into a temporary runtime state
and then calls the same R/Phi budget used by `budget status`.

## Direction Checks

The required directional checks are:

1. `clean_episode` has lower R than `missing_evidence_episode`.
2. `clean_episode` has higher Phi than `failed_command_episode`.
3. `contradiction_episode` has `contradiction_component > 0`.
4. `missing_evidence_episode` has `missing_evidence_component > 0`.
5. `rollback_failure_episode` returns `ActionGate BLOCK`.
6. `rollback_success_episode` does not return `BLOCK`.
7. `stale_memory_episode` has `stale_state_component > 0`.
8. `review_block_episode` has higher `review_block_component` than clean.
9. `mixed_realistic_sanitized_episode` is not `OPTIMO`.
10. Generated JSON schema remains stable.

## Status Semantics

`PASS` means all synthetic directional expectations passed.

`REVIEW` means at least one weak expectation failed. Inspect the failed
component before changing weights.

`BLOCK` means a critical safety expectation failed: rollback failure did not
block, or clean work was classified as `JAMMING`.

## Why Calibration Is Needed

Low R with missing signals is only a baseline. It is not proof that a work
episode is safe, complete, or externally valid.

R and Phi are operational telemetry. They help agents decide whether to keep
closing local work, request review, or block execution. They do not authorize
publication, deployment, provider activation, or private material exposure.

## CLI

```powershell
python -m claudio_agent_runtime budget calibrate --output-root qa_artifacts --json
```

The command writes:

- `qa_artifacts/rphi-calibration-latest.json`;
- `qa_artifacts/rphi-calibration-report-latest.md`.

## Current Calibration Result

Current synthetic calibration status: `PASS`.

Default weights remain unchanged. No weight review is required from this
synthetic pass.

## Known Limitations

- Fixtures are synthetic and intentionally small.
- Directional checks are not statistical validation.
- The harness does not prove external safety or publication readiness.
- Real calibration must use sanitized local episodes with WitnessLog, task
  board, memory, command outcomes and rollback evidence.

## Future Path

Next calibration should add one or more real sanitized local work episodes and
compare results against the synthetic matrix. Weight changes should remain
`REVIEW_REQUIRED` unless a concrete bug prevents correct directional movement.
