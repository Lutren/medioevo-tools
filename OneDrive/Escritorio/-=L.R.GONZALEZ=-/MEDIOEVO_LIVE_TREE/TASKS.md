## 2026-05-18 - Claudio Mission Control dashboard v0.1

- StateFingerprint: CLAUDIO-MISSION-CONTROL-v0-1-20260518.
- Implemented `/api/mission-control` as LOCAL_ONLY_READONLY aggregator for agents, Agent Chat, workpacks, scheduler, BrowserBridge, provider, tree health, coding acceptance, risks and evidence.
- Wabi UI includes `Claudio Mission Control` panel with no execution buttons in the Mission Control section.
- Static internal snapshot exists at `qa_artifacts/release_validation/RUN_CLAUDIO_MISSION_CONTROL_v0_1_20260518/mission_control_snapshot/index.html`.
- Gates preserved: Cloud BLOCK_THIS_RUN, Kimi BLOCK_THIS_RUN, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- QA: focal 223 passed; 02_CLAUDIO 733 passed; Wabi 309 passed; safe-tests ok=true witness 41; GEODIA 74; DUAT 117; compileall PASS; HTTP smoke PASS; SecretScan/BoundaryScan/ScienceClaimGate PASS.
- No cloud, Kimi, NVIDIA, DeepSeek, push, deploy, publication or direct delete ran.

# TASKS

## P0

- Revisar `10_QUALITY/SECRET_SCAN_REPORT.md` por allowlist de target antes de cualquier publicacion.
- Mantener bloqueado push/deploy/publicacion mientras existan hallazgos enmascarados de secret scan.

## P1

- Migrar MEDIOEVO MessageBus de `localStorage` a JSONL/SQLite local append-only.
- Crear validador de schema/canales/hash-chain para `AgentMessage` y `WitnessEvent`.
- Revisar `08_CLEANUP/UNKNOWN_REVIEW.md`.
- Subir cobertura de candidatos `DELETE_AFTER_COVERAGE` solo con hash, destino claro y no-secretos.

## P2

- Crear MCP read-only local para listar canales, bulletin, handoffs y P0.
- Afinar fichas de `01_SOURCE_CARDS` para los 20 candidatos de mayor valor.
# Run 3 cierre / Run 4 entrada

- [x] P1 Crear adaptador JSONL local en disco para `appendOnlyLog`. Evidencia: `node scripts\messagebus\verify.mjs` 2026-05-13 `ok=true`.
- [x] P1 Crear replay test: export JSONL -> import JSONL -> `verifyLog().ok === true`. Evidencia: `npm test -- src/messagebus` 2026-05-13, `88 passed`.
- [x] P1 Migrar `ack/resolve/block` legacy a eventos derivados append-only. Evidencia: `src/messagebus/service.test.ts` registra `message.ack`, `message.resolve`, `message.block`; `npm test -- src/messagebus` 2026-05-13, `88 passed`.
- [x] P1 Crear MCP read-only local para `medioevo://messagebus/*`. Cerrado como `messagebus://*` local read-only. Evidencia: `npm run messagebus:mcp:smoke` 2026-05-13 `ok=true`, resources 7, tools 8.
- [x] P2 Validar `evidence_refs` sin imprimir secretos. Evidencia: `sanitizeRefs()` y tests MCP 2026-05-13; refs secret-like devuelven `REDACTED_REF` + fingerprint.
- [x] P2 Crear fixture de ledger Run 3 con hash-chain SHA-256. Evidencia: `src/messagebus/fixtures/valid-log.jsonl` validado por `npm test -- src/messagebus` 2026-05-13.

# Run 4 cierre / Run 5 entrada

- [x] P1 Crear MCP read-only server local sobre `messagebus-main.jsonl`.
- [x] P1 Exponer resource `messagebus://logs`.
- [x] P1 Exponer resource `messagebus://channels`.
- [x] P1 Exponer resource `messagebus://agents`.
- [x] P1 Exponer resource `messagebus://tasks`.
- [x] P1 Exponer resource `messagebus://handoffs`.
- [x] P1 Exponer resource `messagebus://witnesslog`.
- [x] P1 Exponer resource `messagebus://health`.
- [x] P1 Tools read-only: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `get_agent_outbox`, `get_task_queue`, `export_handoff`, `export_witnesslog`.
- [x] P2 Diseñar migracion de historial browser `localStorage` hacia JSONL durable. Evidencia: `03_SYSTEMS/MESSAGEBUS_LOCALSTORAGE_TO_JSONL_MIGRATION.md`.

# Run 5 cierre / Run 6 entrada

- [x] P1 Crear Agent Bridge / A2A local adapter sobre MCP read-only. Evidencia: `npm run agents:bridge:smoke` 2026-05-13 `ok=true`.
- [x] P1 Crear agent cards locales: Codex Agent, Publisher Agent, Canon Auditor Agent, Security Gate Agent, UI Agent. Evidencia: `npm run agents:bridge:smoke` 2026-05-13 agents 6.
- [x] P1 Simular handoff local entre agentes sin escritura remota. Evidencia: `npm run agents:bridge:smoke` 2026-05-13 bloquea deploy/publicacion y permite lectura local.
- [x] P1 Agregar smoke `messagebus:a2a:smoke`. Cerrado como `agents:bridge:smoke`. Evidencia: `npm run agents:bridge:smoke` 2026-05-13 `ok=true`.
- [x] P1 Verificar que `messagebus:mcp:smoke`, `npm test`, `npx tsc -b` y `npm run build` siguen pasando. Evidencia 2026-05-13: `messagebus:mcp:smoke ok=true`, `npm test 99 passed`, `npx tsc -b` passed, `npm run build` passed.
- [x] P2 Disenar resources derivados `messagebus://artifacts`, `messagebus://bulletin/latest`, `messagebus://security/p0`. Evidencia: `npm run messagebus:mcp:smoke` 2026-05-13 lista 10 resources.

# Run 6 cierre / Run 7 entrada

- [x] P1 Crear Agent Bridge / A2A local adapter sobre MCP read-only.
- [x] P1 Crear agent cards locales: Codex Agent, Publisher Agent, Canon Auditor Agent, Security Gate Agent, UI Agent, MessageBus Reader Agent.
- [x] P1 Simular handoff local entre agentes sin escritura remota.
- [x] P1 Agregar smoke `agents:bridge:smoke`.
- [x] P1 Verificar `messagebus:mcp:smoke`, `npm test`, `npx tsc -b` y `npm run build`.
- [x] P1 Crear ActionGate write proposal layer. Evidencia: `npm run actiongate:smoke` 2026-05-13 `status=PASS`.
- [x] P1 Crear proposals firmadas: `append_message`, `create_task`, `update_handoff`, `publish_release`. Evidencia: `npm run actiongate:smoke` 2026-05-13, seals `true`.
- [x] P1 Simular aprobacion/rechazo del operador. Evidencia: `npm run actiongate:smoke` 2026-05-13 `approved_simulated` y `rejected_simulated`.
- [x] P2 Disenar storage separado de proposals sin tocar `messagebus-main.jsonl`. Evidencia: `02_RUNTIME/actiongate/proposals/actiongate-proposals.jsonl`; smoke reporta `mainMessageBusMutation=NOT_DETECTED`.

# Run 9 cierre / Run 10 entrada

- [x] P1 Revalidar MessageBus/Agent Bridge/ActionGate tras restaurar dependencias desde `package-lock.json`.
- [x] P1 Convertir transiciones `ack/resolve/block` legacy en eventos `WitnessEvent` derivados append-only sin imprimir razones sensibles.
- [x] P2 Validar `evidence_refs` sin imprimir secretos en fixtures y exports. Evidencia: `src/messagebus/mcpReadOnly.test.mjs`, `npm test -- src/messagebus` 90 passed.
- [x] P2 Disenar resources derivados `messagebus://artifacts`, `messagebus://bulletin/latest`, `messagebus://security/p0`. Evidencia: resources MCP read-only agregados y smoke `ok=true`.
- [x] P2 Disenar migracion de historial browser `localStorage` hacia JSONL durable. Evidencia: `03_SYSTEMS/MESSAGEBUS_LOCALSTORAGE_TO_JSONL_MIGRATION.md`.
- [x] REVIEW Upgrade mayor Vite/Vitest/esbuild para resolver 5 vulnerabilidades moderadas dev sin romper build. Registrado como REVIEW, no ejecutado en Run 9.

# Run 10 cierre / Run 11 entrada

- [x] P1 Separar `prompt_started_at` y `work_delivered_at` en el contrato de handoff. Evidencia: `src/messagebus/types.ts`, `src/messagebus/service.ts`, `03_SYSTEMS/AGENT_MESSAGE_SCHEMA.md`.
- [x] P1 Agregar `BRIEF INTELIGENTE` y `DETALLE COMPLETO` al export Markdown. Evidencia: `src/messagebus/exporters.ts`, `scripts/messagebus/lib/export-md.mjs`, `npm test -- src/messagebus` 90 passed.
- [x] P1 Actualizar `/telecom` con `Brief humano`, `Lo importante`, tiempos y escala R verde-rojo. Evidencia: browser check local `http://127.0.0.1:5173/telecom`.
- [x] P2 Documentar escala R `0 verde -> 1 rojo/jamming`. Evidencia: `01_CANON/R_PHI_JC.md`, `02_RUNTIME/HANDOFF.md`.
- [x] P1 En el proximo handoff real, capturar `prompt_started_at` desde origen y no desde timestamp operativo aproximado. Cerrado 2026-05-21: el fingerprint de este ciclo registra `prompt_started_at_source=not_available_in_codex_context` y separa `work_delivered_at_utc`; no se invento timestamp aproximado.

## 2026-05-18 - Agent Chat Persistence/Search v0.3

- StateFingerprint: AGENT-CHAT-PERSISTENCE-SEARCH-v0-3-20260518.
- Agent Chat now has append-only persistent JSONL storage, hash-chain verification, local keyword search, filters, thread reconstruction and internal JSONL/Markdown export.
- Search/export/reconstruction do not execute tasks; draft creation still routes through TaskSpec/Workpack flows and execution remains behind GhostGate, rollback and WitnessLog.
- UI exposes Agent Chat Search with filters, hash-chain status, results and thread panel.
- Gates preserved: CloudLiveGate BLOCK_THIS_RUN, Kimi not run, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- Evidence: qa_artifacts/release_validation/RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518/.
- Tests: Agent Chat focal 204 passed; Wabi 309 passed; safe-tests ok witness 40; 02_CLAUDIO 714 passed; GEODIA 74 passed; DUAT predictive 117 passed; compileall PASS; HTTP smoke PASS; SecretScan artifacts PASS; BoundaryScan PASS; ScienceClaimGate PASS.
- Next: Claudio Mission Control dashboard v0.1 or public-safe Agent Chat architecture docs.
