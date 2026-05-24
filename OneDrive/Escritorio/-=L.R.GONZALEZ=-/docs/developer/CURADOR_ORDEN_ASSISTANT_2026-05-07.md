# CURADOR ORDEN ASSISTANT

Status: `ACTIVE_LOCAL_DESIGN`

Date: `2026-05-07`

Purpose: give the Curador SETO lane a small assistant that keeps order and
teaches workspace hygiene to humans and agents without performing destructive
cleanup.

## Contract

Name: `curador_orden_assistant`

Mode: `READ_ONLY_PLUS_REPORTS`

Primary implementation:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd curator-assistant --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd curator-fichas --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Allowed writes:

- `runtime/outputs/curator_assistant_report_*.json`
- `runtime/outputs/curator_assistant_report_*.md`
- `runtime/outputs/curator_fichas_*.json`
- `runtime/outputs/curator_fichas_*.md`
- `docs/intake/CURADOR_ORDEN_FICHAS_*.md`
- Wabi/Sabi local logs and witness DB

Never does:

- delete files;
- move or rename files;
- `git add .`;
- commit, reset, checkout or broad revert;
- publish, push, deploy or upload;
- read or print secret values;
- touch private game, TCG or game bridge lanes.

## Teaching Rules

1. Start with status: run `worktree-status` or `curator-assistant` before broad
   folder work.
2. No broad staging: stage only files owned by the current task.
3. No physical cleanup during concurrency: if other agents are active, do not
   delete, move, revert or rename their files.
4. Use evidence folders: generated outputs go to `runtime/outputs`, logs to
   `runtime/logs`, handoffs to `NEXT_SESSION_BRIEF.md` and
   `SESSION_FINGERPRINT.json`.
5. Ficha before archive: unknown material needs ficha, hash or manifest before
   archive/delete candidates are trusted.
6. Keep private lanes blocked: game, TCG, secrets, paid content and publication
   actions remain `BLOCK` unless a specific gate authorizes them.
7. Close with verification: use `claim-contract`, `project-scan`, `test-plan`
   and `run-safe-tests` before claiming implementation closure.

## Output States

| category | meaning | allowed action |
|---|---|---|
| `CONCURRENT_TRACKED_CHANGE` | tracked file changed while agents may be active | preserve, do not revert |
| `UNTRACKED_REVIEW` | new or unknown material | create ficha/owner |
| `ROOT_LOOSE_REVIEW` | loose root item | move only after migration map |
| `CACHE_OR_BUILD_REVIEW` | likely generated residue | review regenerability before cleanup |
| `HANDOFF_EVIDENCE` | session state, test report or brief | keep/update only when owned |
| `RUNTIME_EVIDENCE` | generated evidence | keep unless retention policy exists |
| `BOUNDARY_BLOCKED` | secret/private/payment/game/publication risk | block |

## Relationship To SETO

This assistant implements the safe opening move for the Curador SETO contract:
dry-run inventory, order rules, candidate table, ObservationEnvelope and
WitnessLog. It does not replace `DELETE_CANDIDATES.md`, `MIGRATION_MAP.md`,
fichas, secret scans, duplicate hashes or manual review.

## Ficha Pass

`curator-fichas` converts the dry-run candidate table into review cards. It is
still not cleanup. Each ficha records:

- path and git status;
- `CERTEZA`, `INFERENCIA`, `INCOGNITA` or `BLOQUEADO`;
- ActionGate result;
- risk flags;
- owner assigned by an agent lane;
- evidence that content was not read;
- `curation.last_record.actor_type`;
- blocked actions;
- next safe action.

Invariant: `delete_approved_count=0`.

Owner invariant: each ficha receives an agent owner before cleanup review. The
assignment is valid only when `owner_assignment.assigned_by_actor_type=agent`
and `owner_assignment.status=AGENT_ASSIGNED`.

Processing invariant: data curation is considered processed only when the
latest curation record is agent-owned. If a human changes owner, edits a ficha
or appends a manual review note, the ficha must remain
`NEEDS_AGENT_PROCESSING` until a later agent pass records
`owner_assignment.assigned_by_actor_type=agent` and
`curation.last_record.actor_type=agent` again.
