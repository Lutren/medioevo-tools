# Wabi MCP Security Boundary v0.1 - 2026-05-18

Status: LOCAL SAFETY BOUNDARY

## Public-Safe Boundary

The MCP bridge may describe architecture and status publicly, but it must not publish private runtime code, internal chat, real workpacks, local routes with private data, protected canon, raw prompts, datasets or credentials.

## Default Deny

Default mode is READ_ONLY. PREPARE_ONLY must still produce drafts, not side effects. GATED_WRITE is disabled until its tests, gates and audit trail exist.

## Blocked Payload Classes

- Private workspace content.
- Secret or credential values.
- Protected literary or game material.
- Internal prompts and datasets.
- Full internal chat exports.
- Direct file deletion requests.
- Publication, push or deploy instructions.

## Required Controls

- Localhost bind by default.
- CORS deny by default.
- Token only from environment if auth is added later.
- Request and response redaction.
- Audit event for every call.
- WitnessLog for every write.
- Rollback evidence before local apply.
- BoundaryScan and SecretScan before public packaging.

## Provider Gates

- Cloud private workspace: BLOCK.
- Kimi send: BLOCK in this run.
- NVIDIA smoke: DO_NOT_CALL.
- DeepSeek: REVIEW_QUOTA_OR_BILLING.
- Publication: public-safe only after QA.

## Failure Handling

The bridge must fail closed when a gate is missing, a payload is unsafe, a lane is not allowlisted, a secret-like value is detected, or a write lacks rollback/WitnessLog evidence.

