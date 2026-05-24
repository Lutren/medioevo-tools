# WABI UI TASKSPEC MULTI SMOKE 2026-05-19

Fingerprint: `WABI_UI_TASKSPEC_MULTI_SMOKE_20260519`

## Server

- URL: `http://127.0.0.1:8787/`
- Restarted local Wabi server PID: `30920`
- BrowserBridge live: false
- graphics_live: false
- cloud live call: false
- publication gate: BLOCK

## UI Smoke

Evidence directory:

`C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_UI_TASKSPEC_MULTI_SMOKE_20260519`

Artifacts:

- Screenshot: `wabi_ui_smoke_127_0_0_1_8787.png`
- HTML snapshot: `wabi_ui_html_snapshot.html`
- Text snapshot: `wabi_ui_text_snapshot.md`
- UI smoke summary: `ui_smoke_summary.json`
- Conversation turn: `conversation_turn.json`
- Gate Preview: `gate_preview.json`
- Apply Local Preview: `apply_local_preview.json`

Confirmed by HTML/text snapshot:

- Wabi Conversation present: true
- Review TaskSpec present: true
- Gate Preview present: true
- Apply Local Preview present: true
- Apply Local present: true
- Apply Local initial state: disabled until preview readiness

## TaskSpec Multiarchivo

`ConversationEngine.create_task_spec()` now includes:

- `affected_paths`
- `changes`
- `suggested_tests`
- `rollback_required`
- `rollback_strategy`
- `next_action`
- `proposal_only=true`
- `applied_to_sources=false`

For the validated JSON helper request, TaskSpec expands to two files:

- `wabi_sabi/core/json_safety.py`
- `tests/test_json_safety.py`

The UI receives a redacted review. The server retains the raw TaskSpec only in memory for the current local apply path, so the UI does not persist full prompt text or source content.

## WitnessLog

- Event `48`: UI TaskSpec multi smoke
- Event `49`: Assets Du WABI audit/strip
- Witness DB: `C:\Users\L-Tyr\.medioevo\wabi\runtime\witness\wabi_patch_witness.sqlite`
- Chain verify: PASS

## QA

- Wabi focal: `33 passed`
- BRAIN_OS local apply API focal: `5 passed`
- BRAIN_OS server/UI focal: `250 passed`
- Wabi full regression: `376 passed`
- BRAIN_OS full regression: `765 passed`
- py_compile touched modules: PASS
- Secret scan focal: `concrete_secret_value_matches=0`

## Gates

- Apply legacy remains blocked.
- Apply Local is disabled until `Apply Local Preview` returns readiness.
- CloudProposal only.
- Graphics plan-only.
- No push.
- No deploy.
- No publication.
