# SETO COMMS

`COMMS` is the local file protocol for agent coordination.

Rules:

- messages are append-only or superseded by a new envelope;
- every action proposal cites an `ObservationEnvelope`;
- `REVIEW` leaves files untouched and emits a handoff;
- `BLOCK` prevents publication, external action, private-boundary access and
  strong claims;
- no agent overwrites another agent's lane without a handoff.

Current schemas:

- `schemas\observation-envelope.schema.json`
- `schemas\action-gate.schema.json`
- `schemas\witness-log-event.schema.json`
