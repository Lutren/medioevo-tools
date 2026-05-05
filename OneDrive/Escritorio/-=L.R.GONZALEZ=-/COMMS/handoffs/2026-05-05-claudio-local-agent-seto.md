# SETO Handoff To Claudio Local Agent 2026-05-05

Status: `READY_FOR_READ_ONLY_INTAKE`

Recipient: `claudio-local-agent`

Sender: `curador-seto`

This handoff gives Claudio the operational decision contract produced by SETO.
It is not a request to edit files, train a model, publish, push or execute
external actions.

## Inputs

| artifact | role | sha256 |
|---|---|---|
| `docs\developer\SETO_OBSERVACIONISMO_DECISION_LEARNING_2026-05-05.md` | decision-learning contract | `86E0FBC05B4C897DADB8481F86D4F7C121B567AD6805EF17EC9E74C9F4303C26` |
| `qa_artifacts\release_validation\seto-observacionismo-decision-examples-2026-05-05.jsonl` | machine-readable examples | `B00114556582418EFD3AE37C453B2B5FC0E2659EDB6D57CF4032A0F2DDE2E4D3` |
| `docs\intake\SETO_PSI_VAULT_RESIDUAL_REVIEW_2026-05-05.md` | residual PSI review | `6224F70782EDCA944030DFD6A703C4665403F6D5FD6CCC60ADDD33679A1664AA` |
| `qa_artifacts\release_validation\seto-psi-vault-residual-review-2026-05-05.json` | residual PSI evidence | `D07980496DFCD43DB17D41C74FE3D175EB5267C9BBFD3FF840224FA9D22C940C` |

## Local Agent Use

Claudio may consume these files to implement or test local decision routing:

- parse `ObservationEnvelope`;
- distinguish `psi_state` from `action_gate`;
- prefer `REVIEW` when canonical lineage is unclear;
- require post-validation before claiming success;
- emit handoff envelopes instead of touching uncertain files.

## Blocks

Claudio must not use this handoff to:

- delete residual PSI files;
- edit language-agent or local-agent owned source without a later handoff;
- copy raw Downloads or vault material into canon;
- publish, push, post, deploy or operate browser/auth state;
- act on medical, physics-strong or social-prediction claims.

## Acceptance Criteria

The local agent lane can mark this handoff consumed only after it can show:

- schema parse of the JSONL examples;
- gate tests for `APPROVE`, `REVIEW` and `BLOCK`;
- a no-write dry run for uncertain paths;
- WitnessLog or equivalent local append-only evidence for decisions.

## ObservationEnvelope

```json
{
  "envelope_version": "seto-observation-v1",
  "source_path": "docs/developer/SETO_OBSERVACIONISMO_DECISION_LEARNING_2026-05-05.md",
  "source_kind": "handoff_contract",
  "sha256": "86E0FBC05B4C897DADB8481F86D4F7C121B567AD6805EF17EC9E74C9F4303C26",
  "size_bytes": 0,
  "evidence": [
    "decision contract",
    "decision examples JSONL",
    "residual PSI review",
    "secret scan count_reported 0"
  ],
  "psi_state": "CERTEZA",
  "claim_level": "operational",
  "falsifiers": [
    "JSONL examples fail schema parse",
    "local agent cannot separate psi_state from action_gate",
    "local agent writes to uncertain files during dry run"
  ],
  "risk_flags": [
    "local_agent_write_risk",
    "raw_source_claim_risk"
  ],
  "action_gate": "REVIEW",
  "decision": "KEEP_COORDINATION_BOUNDARY",
  "fingerprint": "SETO_CLAUDIO_LOCAL_AGENT_HANDOFF_2026-05-05"
}
```
