# Agent Chat Routing v0.2 Status - 2026-05-18

Agent Chat Routing v0.2 is implemented locally.

Current verified capabilities:

- route messages by mention and room;
- inbox/outbox per agent;
- create TaskSpec drafts from messages;
- create Workpack drafts from messages;
- attach messages to Workpacks;
- append system status messages;
- no direct execution from chat.

Execution remains gated by Workpack Bridge, Local Execute, TaskSpec, GhostGate
APPROVE, rollback snapshot and WitnessLog.
