# RPHI_BUDGET_v0_1

Status: `LOCAL_ONLY`

## Purpose

The R/Phi budget converts available local runtime artifacts into deterministic
operational telemetry for agent work.

It does not ask a language model to guess quality. It reads local files, counts
observable signals and returns bounded values:

- `r_total`: normalized informational residue, `0.0` to `1.0`;
- `phi_eff`: verified useful output divided by coordination cost, `0.0` to
  `1.0`;
- `regime`: `OPTIMO`, `FUNCIONAL`, `CARGADO`, `SATURADO` or `JAMMING`;
- `actiongate_suggestion`: `APPROVE`, `REVIEW` or `BLOCK`.

## Inputs

The budget reads only local artifacts and treats missing files as unavailable
signals:

- `tasks/task_board.json`;
- `memory/memory_lite.jsonl`;
- `witness/witness_log.jsonl`;
- `runtime/rollback/*/manifest.json`;
- `SESSION_FINGERPRINT.json`;
- `TEST_REPORT.md`.

No network, service, external channel or dependency install is required.

## R Formula

`R_total` is a weighted sum of normalized components:

```txt
R_total =
  0.14 * uncertainty_component +
  0.14 * contradiction_component +
  0.16 * missing_evidence_component +
  0.08 * ambiguity_component +
  0.08 * stale_state_component +
  0.14 * irreversible_risk_component +
  0.10 * coordination_overhead_component +
  0.06 * rollback_component +
  0.05 * failure_component +
  0.05 * review_block_component
```

The result is clamped to `[0.0, 1.0]`.

## Phi_eff Formula

```txt
verified_output =
  completed_tasks +
  passed_tests +
  created_handoffs +
  evidence_backed_claims +
  successful_rollbacks +
  approved_local_gate_events

coordination_cost =
  total_actions +
  reviews +
  blocks +
  failed_commands +
  missing_evidence +
  rollback_count +
  stale_state_count +
  unresolved_items

Phi_eff =
  verified_output / max(verified_output + coordination_cost, 1)
```

The result is clamped to `[0.0, 1.0]`.

## Regime

```txt
R < 0.15 -> OPTIMO
R < 0.40 -> FUNCIONAL
R < 0.70 -> CARGADO
R < 0.90 -> SATURADO
R >= 0.90 -> JAMMING
```

## ActionGate Suggestion

`APPROVE` requires low residue, high efficiency, no block events and low
irreversible risk.

`REVIEW` is returned when local work is bounded but evidence, reversibility or
coordination cost should be closed before widening scope.

`BLOCK` is returned when private/sensitive path findings, publication attempts,
destructive actions, failed rollback restore or jamming-level residue are
observed.

## CLI

```powershell
python -m claudio_agent_runtime budget status --root fixtures\state --json
python -m claudio_agent_runtime budget report --root fixtures\state --output-root qa_artifacts --json
python -m claudio_agent_runtime budget calibrate --output-root qa_artifacts --json
```

The report command writes:

- `qa_artifacts/rphi-budget-latest.json`;
- `qa_artifacts/rphi-budget-report-latest.md`.

The calibration command writes:

- `qa_artifacts/rphi-calibration-latest.json`;
- `qa_artifacts/rphi-calibration-report-latest.md`.

Calibration is synthetic and directional. It checks that R rises and Phi falls
under known local residue scenarios. It does not prove external validity and it
does not authorize publication or weight changes.

## Integration

`doctor` now includes the full `rphi_budget` object.

`brief` includes `R_est`, `Phi_eff_est`, `Regimen` and
`ActionGate_suggestion`.

## Boundary

This module is public-safe and local-only. It must not be used as publication
permission. It is an operational budget for local agent coordination and
evidence closure.
