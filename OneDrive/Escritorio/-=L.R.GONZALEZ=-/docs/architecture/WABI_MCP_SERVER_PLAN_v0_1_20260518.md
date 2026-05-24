# Wabi MCP Server Plan v0.1 - 2026-05-18

Status: LOCAL DESIGN / READ-ONLY FIRST

## Purpose

The Wabi MCP Server is a local bridge between compatible agents and the Wabi/Claudio operator API. It is not a public execution endpoint and it is not a dependency on free chat interfaces as workers.

Wabi remains the runtime. Claudio remains the coordinator and gatekeeper. External agents may receive only safe tools, with read-only access first, prepare-only tools second, and gated write tools only after explicit local gates.

## Architecture

- Local MCP Server, bound to localhost by default.
- Wabi/Claudio API as the internal source of truth.
- Mission Control as a read-only aggregate state.
- Local Hub and Workpack Bridge for prepared local work.
- Local Execute for sandbox/docs-local execution only.
- Agent Chat persistence/search for local coordination context.
- WitnessLog and rollback evidence for any future write path.
- BoundaryScan and SecretScan before public artifacts or exports.

## Modes

### READ_ONLY

Allowed:

- Mission Control state.
- Agent hub state.
- Agent Chat search and thread reconstruction.
- Workpack list and scheduler state.
- Evidence summaries and latest handoff.
- BrowserBridge status.
- Provider, tree health and coding acceptance state.

Not allowed:

- Creating tasks.
- Ticking scheduler.
- Executing workpacks.
- Sending browser payloads.
- Publishing, pushing or deploying.

### PREPARE_ONLY

Allowed:

- Create TaskSpec draft.
- Create Workpack draft.
- Attach a message to a workpack.
- Write a handoff draft.

The prepare layer does not execute. Prepared objects must remain reviewable and reversible.

### GATED_WRITE

Allowed only for local sandbox/docs tasks and only after all gates pass:

- TaskSpec exists.
- GhostGate returns APPROVE.
- Rollback evidence exists.
- WitnessLog can append.
- Lane is allowlisted.
- No cloud, publication, protected material or credentials.

Candidate gated tools:

- run_ghostgate(task_spec_id)
- queue_workpack(workpack_id)
- scheduler_tick(queue_id)
- execute_local_workpack(workpack_id)

### BLOCKED

No MCP tool is planned for:

- publish, push or deploy;
- direct delete;
- cloud execution over private workspace;
- Kimi, NVIDIA or DeepSeek calls;
- sending workspace material;
- exposing secrets;
- reading protected books or Fragmentos content;
- exporting internal chat as public-safe material.

## Initial Tool Set

Read-only:

- get_mission_control()
- get_agent_hub()
- search_agent_chat(query, filters)
- reconstruct_agent_thread(message_id)
- get_workpacks()
- get_scheduler_state()
- get_browser_bridge_status()
- get_provider_status()
- get_tree_health()
- get_coding_acceptance()
- get_latest_handoff()

Prepare-only:

- create_taskspec_draft(source_type, source_id)
- create_workpack_draft(task_id)
- attach_message_to_workpack(message_id, workpack_id)
- write_handoff_draft(scope)

Gated-write:

- run_ghostgate(task_spec_id)
- queue_workpack(workpack_id)
- scheduler_tick(queue_id)
- execute_local_workpack(workpack_id)

## Auth And Boundary

- Localhost default.
- Optional API token only via environment.
- No token in files.
- Redacted logging by default.
- CORS default deny.
- Public exposure requires a separate owner-approved run.
- Any future public endpoint starts read-only.

## Logging

- Every MCP call writes an audit event.
- Any write also writes WitnessLog.
- MCP audit may use a hash chain.
- Request bodies are redacted when they may contain private context.

## v0.1 Decision

This run creates the design and endpoint inventory only. The executable MCP scaffold is deferred to v0.2 to keep v0.1 public-safe and read-only by construction.

