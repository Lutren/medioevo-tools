# Claudio Agent Runtime

Status: `P0_LOCAL_DRY_RUN`

Claudio Agent Runtime is a public-safe local CLI surface for agent work:
permissions, skills, memory summaries, task board state and handoff briefs.

This package is inspired by the Mercury Agent product pattern, but it does not
copy Mercury code and does not depend on Mercury.

## Safety posture

- No network.
- No external channels.
- No daemon/service install.
- No dependency install.
- No push, deploy, publish, Gumroad, Telegram, GitHub write or Spotify action.
- Secret handling is presence-only; values are never printed.
- RPG/TCG, books, private runtime and raw secret material are blocked.

## Commands

```powershell
python -m claudio_agent_runtime doctor --json
python -m claudio_agent_runtime ghostgate tools --json
python -m claudio_agent_runtime ghostgate check fixtures\ghostgate_plan_blocked.json --json
python -m claudio_agent_runtime permissions check fixtures\permission_local_write.json
python -m claudio_agent_runtime execute write fixtures\execute_write_approved.json --root <temp-root> --json
python -m claudio_agent_runtime rollback restore <rollback-id> --root <temp-root> --json
python -m claudio_agent_runtime skills list --root fixtures\skills --json
python -m claudio_agent_runtime memory status --root fixtures\state --json
python -m claudio_agent_runtime tasks list --root fixtures\state --json
python -m claudio_agent_runtime brief --root fixtures\state
python -m claudio_agent_runtime witness status --root fixtures\state --json
python -m claudio_agent_runtime budget status --root fixtures\state --json
python -m claudio_agent_runtime budget report --root fixtures\state --output-root qa_artifacts --json
python -m claudio_agent_runtime budget calibrate --output-root qa_artifacts --json
```

Add `--witness-root <state-root>` to any P0/P1 command to append a redacted JSONL
event under `<state-root>/witness/witness_log.jsonl`.

`execute write` only supports local reversible file writes after `ActionGate`
returns `APPROVE`. It does not run shell commands, git writes, network actions,
publication actions or external channel actions.

## R/Phi budget

The local R/Phi budget is deterministic telemetry, not a subjective model
score. It reads available runtime artifacts and falls back safely when a signal
does not exist:

- task board state;
- WitnessLog JSONL summaries;
- memory records;
- command and test outcomes from local continuity artifacts;
- rollback manifests and restore events;
- GhostGate and ActionGate decisions.

Machine-readable output includes `r_total`, `phi_eff`, `regime`,
`actiongate_suggestion`, `components`, `raw_counts`, `recommendations`,
`source_files_used` and `generated_at`.

`budget calibrate` runs synthetic local episodes for clean, missing evidence,
contradiction, failed command, review/block-heavy, rollback success, rollback
failure, stale memory and mixed realistic sanitized work. It checks directional
movement only; it does not change weights or authorize external actions.

## License

`LEGAL_REVIEW_REQUIRED` until this package is explicitly prepared for external
publication.
