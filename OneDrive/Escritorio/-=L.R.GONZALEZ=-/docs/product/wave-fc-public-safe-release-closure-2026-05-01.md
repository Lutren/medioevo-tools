# Wave FC Public-Safe Release Closure - 2026-05-01

Status: `LOCAL_DEMO_READY / PUBLICATION_BLOCK`

Decision: Wave FC has enough local evidence for a private/demo sales
conversation, but not for public sale or broad publication. The first public
surface must be low-claim, installation-light and explicit about human review.

## Evidence Available

- Evidence pack: `runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01`
- Release gate: `runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01`
- Captures: `qa_artifacts\2026-05-01-wave-fc-captures`
- Tests: `61 passed` for Wave FC client demo, release gate, collapse report and local server.

## Public-Safe Landing Copy

Use this positioning:

```text
Wave FC is a local evidence pack generator for authorized workspaces. It scans
approved documents read-only, builds a review packet, creates draft requests
for human review and records what evidence was used.
```

Allowed claims:

- local-first workspace intake;
- read-only source handling;
- evidence manifests and hashes;
- human-review queues;
- draft artifacts for review, not final advice;
- synthetic demo data for public examples.

Do not claim:

- legal, financial or compliance advice;
- automatic deletion, automatic filing or autonomous customer action;
- guaranteed accuracy, guaranteed safety or guaranteed anti-hallucination;
- access to private MEDIOEVO/Claudio internals;
- production-ready hosted service.

## Install / Demo Boundary

Current acceptable customer-facing mode:

- private demo call;
- local synthetic evidence pack;
- screenshots from existing QA captures;
- Markdown/JSON handoff packet;
- no customer secrets and no real workspace data in public artifacts.

Not acceptable yet:

- public download;
- SaaS promise;
- paid release page;
- automated external posting;
- final DOCX visual-quality claim.

## Remaining Blockers

- DOCX visual render QA is blocked on missing `artifact-tool` or LibreOffice.
- EULA/license needs final legal review.
- ActionGate must approve any external listing/post.
- Video is not required now because desktop/mobile captures already exist; generate video only for a concrete listing or Devpost need.

## Current Decision

`VIDEO_NOT_REQUIRED_NOW` is closed. `PUBLICATION_READY` remains blocked.
