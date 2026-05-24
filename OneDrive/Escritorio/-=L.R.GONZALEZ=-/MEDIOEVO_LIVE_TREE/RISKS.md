## 2026-05-18 - Claudio Mission Control dashboard v0.1

- StateFingerprint: CLAUDIO-MISSION-CONTROL-v0-1-20260518.
- Implemented `/api/mission-control` as LOCAL_ONLY_READONLY aggregator for agents, Agent Chat, workpacks, scheduler, BrowserBridge, provider, tree health, coding acceptance, risks and evidence.
- Wabi UI includes `Claudio Mission Control` panel with no execution buttons in the Mission Control section.
- Static internal snapshot exists at `qa_artifacts/release_validation/RUN_CLAUDIO_MISSION_CONTROL_v0_1_20260518/mission_control_snapshot/index.html`.
- Gates preserved: Cloud BLOCK_THIS_RUN, Kimi BLOCK_THIS_RUN, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- QA: focal 223 passed; 02_CLAUDIO 733 passed; Wabi 309 passed; safe-tests ok=true witness 41; GEODIA 74; DUAT 117; compileall PASS; HTTP smoke PASS; SecretScan/BoundaryScan/ScienceClaimGate PASS.
- No cloud, Kimi, NVIDIA, DeepSeek, push, deploy, publication or direct delete ran.

# RISKS

- Secret scan con hallazgos: bloquea publicacion, push y deploy.
- ZIPs grandes no extraidos pueden contener `.git`, secretos, rutas locales o material privado.
- Clasificacion automatica puede producir falsos positivos; no borrar desde heuristica.
- E: fue escaneado de forma limitada; no representa cobertura completa del disco.
- Run 2 usa `localStorage` y hash mock: suficiente para UI/local demo, insuficiente para ledger verificable real.
- Seed de UI y seed runtime deben consolidarse en un canon JSONL/SQLite para evitar divergencia futura.
# Run 3 - riesgos MessageBus

- `localStorage` es manipulable: hash-chain detecta alteraciones al validar, pero no impide escritura local manual.
- Fallback `fnv1a-NOT_CRYPTOGRAPHIC` no sirve como seguridad; solo como compatibilidad local si Web Crypto no existe.
- `service.ts` conserva algunas mutaciones legacy para la UI; el ledger append-only ya existe, pero falta migrar transiciones a eventos derivados.
- MCP write tools quedan bloqueadas hasta ActionGate, evidencia y ledger durable.
- Canon ZIP sigue sin validacion de contenido; solo se verifico SHA256/listado central sin extraccion.

# Run 4 - riesgos Durable JSONL

- El log JSONL es durable, pero no anti-manipulacion fisica; la defensa es verificacion hash-chain, no control de acceso.
- El log principal contiene una muestra inicial; aun no es espejo completo de `localStorage`.
- Los scripts Node-only deben mantenerse fuera de imports React para no romper Vite/browser.
- MCP Run 5 debe ser read-only; cualquier write tool queda bloqueada por ActionGate.

# Run 5 - riesgos MCP read-only

- MCP read-only reduce riesgo de mutacion, pero un agente externo aun puede malinterpretar datos si ignora `messagebus://health`.
- `messagebus-main.jsonl` sigue siendo sample inicial; no representa historial completo de `localStorage`.
- El guard bloquea nombres de tools write, pero futuras write tools deben requerir ActionGate y nuevos tests.
- `npm audit --json` reporta 5 vulnerabilidades moderadas dev en Vite/Vitest/esbuild; `npm audit --omit=dev` queda en 0, por lo que no bloquea MCP local read-only.
- Run 6 A2A debe mantenerse local/simulado; cualquier red publica, push, deploy o publish sigue bloqueado.

# Run 6 - riesgos Agent Bridge local

- El Agent Bridge valida que sus operaciones no cambien el JSONL, pero no impide manipulacion fisica externa del archivo.
- Agent Cards son contratos locales; no deben presentarse como A2A publico ni interoperabilidad remota completa.
- El router es por palabras clave; decisiones criticas deben pasar por ActionGate y evidencia.
- Las propuestas de Run 7 pueden amplificar riesgo si se convierten en escritura automatica sin aprobacion explicita.
- `npm audit --json` mantiene 5 vulnerabilidades moderadas dev; upgrade mayor queda en REVIEW y no se ejecuto en Run 6.

# Run 9 - riesgos residuales

- `npm audit --json` sigue reportando 5 vulnerabilidades moderadas dev en Vite/Vitest/esbuild; no hay vulnerabilidades prod con `npm audit --omit=dev`.
- El upgrade recomendado requiere saltos semver-major y puede romper Vite/Vitest, por lo que no se aplica dentro del cierre de pendientes.
- Los eventos derivados `message.block` evitan copiar razones sensibles, pero los mensajes legacy aun conservan `bloqueo`; no imprimir exports sin scrub de secretos.
- `messagebus-main.jsonl` sigue siendo ledger principal con una muestra; los receipts de sandbox no sustituyen historial operativo completo.
- La redaccion de refs reduce exposicion en MCP, pero no sustituye secret scan global antes de cualquier release.
- La migracion `localStorage` -> JSONL esta disenada; ejecutar import real sin dry-run/ActionGate podria duplicar mensajes o romper continuidad de hashes.

## 2026-05-18 - Agent Chat Persistence/Search v0.3

- StateFingerprint: AGENT-CHAT-PERSISTENCE-SEARCH-v0-3-20260518.
- Agent Chat now has append-only persistent JSONL storage, hash-chain verification, local keyword search, filters, thread reconstruction and internal JSONL/Markdown export.
- Search/export/reconstruction do not execute tasks; draft creation still routes through TaskSpec/Workpack flows and execution remains behind GhostGate, rollback and WitnessLog.
- UI exposes Agent Chat Search with filters, hash-chain status, results and thread panel.
- Gates preserved: CloudLiveGate BLOCK_THIS_RUN, Kimi not run, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- Evidence: qa_artifacts/release_validation/RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518/.
- Tests: Agent Chat focal 204 passed; Wabi 309 passed; safe-tests ok witness 40; 02_CLAUDIO 714 passed; GEODIA 74 passed; DUAT predictive 117 passed; compileall PASS; HTTP smoke PASS; SecretScan artifacts PASS; BoundaryScan PASS; ScienceClaimGate PASS.
- Next: Claudio Mission Control dashboard v0.1 or public-safe Agent Chat architecture docs.
