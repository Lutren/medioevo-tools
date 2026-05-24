# Wabi API Bridge Contract v0.1 - 2026-05-18

Status: LOCAL_ONLY / NO EXTERNAL EXPOSURE

## Contract

The Wabi API Bridge exposes local Wabi/Claudio state to approved tools without exposing the private workspace. It is a bridge to selected endpoints and actions, not a remote shell, not a tunnel, and not a public API.

## Access Classes

| Class | Meaning | Examples | Mutation |
| --- | --- | --- | --- |
| READ_ONLY | Inspect local state | mission control, provider status, tree health | no |
| PREPARE_ONLY | Create reviewable drafts | TaskSpec draft, Workpack draft, handoff draft | draft only |
| GATED_WRITE | Mutate local runtime after gates | queue approved workpack, manual scheduler tick | yes, gated |
| BLOCKED | Never exposed as a bridge tool | publish, deploy, direct delete, cloud run | no tool |

## Minimum Endpoint Inventory

- /api/mission-control
- /api/local-hub
- /api/agent-hub
- /api/agent-chat/search
- /api/agent-chat/messages
- /api/agent-chat/hash-chain
- /api/workpacks
- /api/workpack-scheduler
- /api/browser-bridge/status
- /api/provider/diagnostic
- /api/tree-health
- /api/coding-acceptance

## Write Preconditions

Any future GATED_WRITE tool must verify:

- action lane is allowlisted;
- TaskSpec exists;
- GhostGate APPROVE exists;
- rollback evidence exists;
- WitnessLog append works;
- protected material is absent;
- no secret values are present;
- cloud/private workspace gate remains BLOCK;
- PublicationGate is not bypassed.

## External Agents

An external assistant can program against Wabi only if one of these exists:

1. A local MCP server with authorized tools.
2. An authorized API connector.
3. A public API with correct CORS/auth and a public-safe scope.
4. Codex or another local tool running on the same owner machine.

If Wabi only runs on localhost, an external assistant cannot call it directly without an authorized bridge.

## Non-Goals

- No dependency on free chats as reliable workers.
- No workspace upload.
- No credential handling.
- No direct public tunnel.
- No automatic publication.
- No direct execution from Mission Control.

