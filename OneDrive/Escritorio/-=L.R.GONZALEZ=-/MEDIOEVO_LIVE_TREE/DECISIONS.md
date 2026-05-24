## 2026-05-18 - Claudio Mission Control dashboard v0.1

- StateFingerprint: CLAUDIO-MISSION-CONTROL-v0-1-20260518.
- Implemented `/api/mission-control` as LOCAL_ONLY_READONLY aggregator for agents, Agent Chat, workpacks, scheduler, BrowserBridge, provider, tree health, coding acceptance, risks and evidence.
- Wabi UI includes `Claudio Mission Control` panel with no execution buttons in the Mission Control section.
- Static internal snapshot exists at `qa_artifacts/release_validation/RUN_CLAUDIO_MISSION_CONTROL_v0_1_20260518/mission_control_snapshot/index.html`.
- Gates preserved: Cloud BLOCK_THIS_RUN, Kimi BLOCK_THIS_RUN, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- QA: focal 223 passed; 02_CLAUDIO 733 passed; Wabi 309 passed; safe-tests ok=true witness 41; GEODIA 74; DUAT 117; compileall PASS; HTTP smoke PASS; SecretScan/BoundaryScan/ScienceClaimGate PASS.
- No cloud, Kimi, NVIDIA, DeepSeek, push, deploy, publication or direct delete ran.

# DECISIONS

- 2026-05-12T01:31:46: Primera corrida `MDV-LIVE-TREE-NO-ARCHIVE-v2` queda no destructiva.
- `ROOT_BRAIN_OS` queda como canon base `PARTIAL`, no como reemplazo completo del runtime vivo.
- `DELETE_AFTER_COVERAGE` es una categoria de revision, no permiso de borrado.
- Publicacion, push y deploy quedan bloqueados mientras `10_QUALITY/SECRET_SCAN_REPORT.md` tenga hallazgos.
- 2026-05-12 Run 2: `DUAT Telecom Core` queda definido como bus local mock, no como backend externo.
- 2026-05-12 Run 2: `/telecom` en React/Vite es la consola local del MessageBus.
- 2026-05-12 Run 2: A2A y MCP quedan como adaptadores futuros, no como red publica ni servidor remoto en esta corrida.
# Run 3 - MessageBus Validator / Append-only Core

- `MEDIOEVO MessageBus` queda endurecido localmente con validador TypeScript, registry de canales, hash-chain y append-only log.
- La persistencia Run 3 sigue en `localStorage`; JSONL/SQLite durable queda para Run 4.
- El hash preferido es Web Crypto SHA-256; el fallback existe solo como `NOT_CRYPTOGRAPHIC` para runtimes sin soporte.
- MCP queda como plan read-only; no se implementan tools de escritura sin ActionGate.
- El ZIP reconstructivo v12.2.1 sigue en `SECURITY_REVIEW`; se calculo SHA256 y se listaron nombres internos sin extraccion.

# Run 4 - Durable JSONL

- El acceso durable a disco del MessageBus se implementa solo en scripts Node-only; no entra al bundle React/Vite.
- `messagebus-main.jsonl` queda como ledger durable inicial para Run 5.
- `/telecom` conserva `localStorage` y solo muestra estado/plan durable.
- MCP read-only queda como siguiente run; no se crea servidor en Run 4.

# Run 5 - MCP read-only

- `MEDIOEVO MessageBus` queda expuesto por servidor MCP real stdio/local usando `@modelcontextprotocol/sdk`.
- Los handlers MCP son Node-only y viven bajo `scripts/messagebus`; React no importa SDK MCP ni acceso a disco.
- Resources habilitadas: `messagebus://logs`, `messagebus://channels`, `messagebus://agents`, `messagebus://tasks`, `messagebus://handoffs`, `messagebus://witnesslog`, `messagebus://health`.
- Tools habilitadas son solo lectura: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `get_agent_outbox`, `get_task_queue`, `export_handoff`, `export_witnesslog`.
- Cualquier tool con verbo write queda bloqueada por `mcpReadOnlyGuards`.
- Run 6 debe construir Agent Bridge / A2A local adapter sobre MCP read-only, no sobre backend externo.

# Run 6 - Agent Bridge / A2A local

- `Agent Bridge` queda implementado como capa Node-only local bajo `scripts/agents`.
- Las Agent Cards locales definen capacidades, handoff targets, forbidden actions y aprobaciones requeridas.
- El protocolo `medioevo-a2a-local` es solo envelope de simulacion y routing; no es red publica.
- El MCP adapter reutiliza handlers puros read-only de Run 5; no llama tools de escritura.
- El router prioriza seguridad sobre publicacion cuando hay secreto, token o frontera privada.
- Run 7 debe construir ActionGate write proposals en memoria antes de cualquier escritura real.

# Run 9 - cierre de pendientes locales

- Los pendientes duplicados/stale de MessageBus, MCP, Agent Bridge, ActionGate y sandbox se cierran solo con evidencia fresca del 2026-05-13.

# Run 10 - Handoff humano y escala R

- Todo handoff humano debe separar `prompt_started_at` y `work_delivered_at`.
- El Markdown de handoff debe abrir con `BRIEF INTELIGENTE` y despues conservar `DETALLE COMPLETO`.
- `/telecom` debe mostrar primero el brief humano, `Lo importante`, tiempos y escala R.
- R se comunica como `0 verde -> 1 rojo/jamming`, con etiqueta textual aun cuando la UI soporte color.
- `ackMessage`, `resolveMessage` y `blockMessage` mantienen compatibilidad legacy y registran eventos derivados `message.ack`, `message.resolve` y `message.block`.
- El evento derivado de `blockMessage` no copia la razon sensible; solo deja `status=blocked`.
- `npm ci` se uso para restaurar dependencias desde `package-lock.json`; no se agregaron dependencias ni se cambiaron manifests.
- El upgrade de Vite/Vitest/esbuild queda en REVIEW porque requiere semver-major.
- `messagebus://artifacts`, `messagebus://bulletin/latest` y `messagebus://security/p0` quedan habilitados como resources MCP read-only.
- `evidence_refs` y `artifact_refs` secret-like quedan redactados como `REDACTED_REF` con fingerprint.
- La migracion browser `localStorage` -> JSONL queda en diseno; no se ejecuto import real.

## 2026-05-18 - Agent Chat Persistence/Search v0.3

- StateFingerprint: AGENT-CHAT-PERSISTENCE-SEARCH-v0-3-20260518.
- Agent Chat now has append-only persistent JSONL storage, hash-chain verification, local keyword search, filters, thread reconstruction and internal JSONL/Markdown export.
- Search/export/reconstruction do not execute tasks; draft creation still routes through TaskSpec/Workpack flows and execution remains behind GhostGate, rollback and WitnessLog.
- UI exposes Agent Chat Search with filters, hash-chain status, results and thread panel.
- Gates preserved: CloudLiveGate BLOCK_THIS_RUN, Kimi not run, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- Evidence: qa_artifacts/release_validation/RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518/.
- Tests: Agent Chat focal 204 passed; Wabi 309 passed; safe-tests ok witness 40; 02_CLAUDIO 714 passed; GEODIA 74 passed; DUAT predictive 117 passed; compileall PASS; HTTP smoke PASS; SecretScan artifacts PASS; BoundaryScan PASS; ScienceClaimGate PASS.
- Next: Claudio Mission Control dashboard v0.1 or public-safe Agent Chat architecture docs.

## 2026-05-20 - Cosmologia del fluido noumenico (canon ficcional)

- Se adopta como canon ficcional de la saga MEDIOEVO la cosmologia del fluido noumenico (10 postulados P1-P10, reglas R1-R5, tabla de traduccion fisica real / canon). Documento canonico reubicado 2026-05-20 al workbench: `-= BRAIN_OS =-/-=LR WORKING BENCH=-/CANON_ACTUALIZADO/MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17/03_TEORIAS_ACTUALIZADAS/07_COSMOLOGIA_FLUIDO_NOUMENICO.md`. La copia en `06_RESEARCH_LAB/` queda como puntero.
- Estatus: canon ficcional / worldbuilding, no fisica real. Cada afirmacion lleva sello epistemico (CERTEZA/INFERENCIA/INCOGNITA/BLOQUEO/POSTULADO/ANALOGIA/DIVERGENCIA).
- El nucleo mesonico de eta-prima (GSI/FAIR, abril 2026) queda como ancla de inspiracion marcada ANALOGIA; se cita como evidencia (~2 sigma), no como descubrimiento confirmado.
- El operador Fibonacci-Mobius (mu_F) queda como recurso narrativo en la cosmologia; su matematica formal vive en `07b_MATEMATICAS_RIGUROSO.md` (teorema de inversion = CERTEZA matematica; utilidad practica F5 = INCOGNITA, sin cerrar).
- Correccion 2026-05-20: la afirmacion previa de que `07b_MATEMATICAS_RIGUROSO.md` no existia fue un error de busqueda incompleta (solo se reviso `-=L.R.GONZALEZ=-`). El archivo SI existe en `-= BRAIN_OS =-/-=LR WORKING BENCH=-/`, es riguroso y honesto. La cosmologia se remite a 07b; no lo duplica ni lo contradice.
- Tarea de documentacion local: sin envios externos, push, deploy ni publicacion.
