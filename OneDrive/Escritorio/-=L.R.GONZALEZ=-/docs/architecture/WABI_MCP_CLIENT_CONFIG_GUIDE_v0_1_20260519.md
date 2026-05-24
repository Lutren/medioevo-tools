# Wabi MCP Client Config Guide v0.1

Status: LOCAL_CLIENT_CONFIG_ONLY  
Server mode: LOCALHOST_ONLY_READ_PREPARE  
PublicationGate: BLOCK

This guide explains how to connect a compatible local MCP client or wrapper to the Wabi MCP Server v0.3 without exposing Wabi/Claudio outside the machine. It is a configuration guide only. It does not enable execution, gated-write tools, public tunnels, cloud calls, publication, push, deploy or delete actions.

## Current Server Mode

Wabi MCP Server v0.3 runs as a local-first bridge around Wabi/Claudio endpoints.

- host: 127.0.0.1
- mode: LOCALHOST_ONLY_READ_PREPARE
- read-only tools: enabled
- prepare-only draft tools: enabled
- gated-write tools: blocked
- execution_allowed: false
- cloud_allowed: false
- publication_gate: BLOCK

## What A Compatible Client May Do

A local compatible client may call read-only tools:

- read Mission Control
- read Agent Hub
- search Agent Chat
- reconstruct an Agent Chat thread
- verify the Agent Chat hash-chain
- read Workpacks
- read Scheduler state without ticking
- read BrowserBridge status
- read Provider status
- read Tree Health
- read Coding Acceptance
- read the latest sanitized handoff summary

A local compatible client may call prepare-only draft tools when explicitly configured for prepare mode:

- create a TaskSpec draft from a local source
- create a Workpack draft from a local source
- attach a local message to a local Workpack
- write a handoff draft

Prepare-only tools may mutate local draft state. They do not execute, approve, queue, tick, roll back, publish or call cloud services.

## What A Client Must Not Do

The client must not:

- bind the MCP server to 0.0.0.0 or any external interface
- open a tunnel
- expose a public URL
- place tokens, passwords or API keys in config files
- send the private workspace to any cloud service
- run cloud LLM calls
- call Kimi, NVIDIA or DeepSeek
- run scheduler_tick
- execute workpacks
- run Local Execute
- run GhostGate as a write action
- publish, push or deploy
- delete files
- read protected material or private source vaults
- export internal chat as public-safe content

## Client Requirements

Use only a client that can run locally and can point to localhost.

Minimum requirements:

- client runs on the same machine as Wabi/Claudio
- server host remains 127.0.0.1 or localhost
- configuration uses placeholders, not real credentials
- logs are redacted
- gated-write tools remain disabled
- execution_allowed remains false
- external_exposure_allowed remains false

Do not assume that a named product supports MCP unless current official documentation and local configuration confirm it. Use the templates in this run as redacted examples for a compatible local client, a local wrapper, or an external client with MCP support if available and configured by the owner.

## Generic Local Configuration

Use the templates under:

`02_CLAUDIO/mcp/wabi_mcp_server/client_configs/`

Required placeholders:

- `<CLIENT_NAME>`
- `<LOCALHOST_PORT>`
- `<OPTIONAL_LOCAL_TOKEN_ENV_VAR>`

Keep these values as placeholders in versioned files. If an optional local token is ever used, it must be supplied through the local environment and redacted from logs.

## Smoke Test

Default smoke is read-only:

```powershell
python examples/local_client_smoke.py --json
```

Expected behavior:

- list tools
- call get_mission_control
- call get_agent_hub
- call search_agent_chat with a synthetic query
- call scheduler_tick and confirm it is blocked
- report mutated=false
- report execution_allowed=false

Prepare smoke is not the default. If run in a future local-only check, it must use an explicit flag and a synthetic local message id. It still must not execute tasks.

## Troubleshooting

- If the client cannot connect, verify that Wabi is listening on localhost and that the configured port is local.
- If the client tries to use a public URL, stop and replace it with localhost.
- If a config file asks for a token value, stop and use an environment variable placeholder instead.
- If scheduler_tick appears enabled, stop. v0.3 must keep gated-write blocked.
- If a cloud, Kimi, NVIDIA or DeepSeek path appears, stop. This guide does not authorize live provider calls.

## Boundary

INTERNAL_LOCAL / DO_NOT_PUBLISH / CONFIG_ONLY

The public layer may describe the architecture. The local layer is where tools operate, and even there execution remains blocked in this run.
