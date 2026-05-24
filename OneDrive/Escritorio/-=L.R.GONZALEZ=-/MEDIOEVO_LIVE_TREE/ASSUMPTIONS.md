## 2026-05-18 - Claudio Mission Control dashboard v0.1

- StateFingerprint: CLAUDIO-MISSION-CONTROL-v0-1-20260518.
- Implemented `/api/mission-control` as LOCAL_ONLY_READONLY aggregator for agents, Agent Chat, workpacks, scheduler, BrowserBridge, provider, tree health, coding acceptance, risks and evidence.
- Wabi UI includes `Claudio Mission Control` panel with no execution buttons in the Mission Control section.
- Static internal snapshot exists at `qa_artifacts/release_validation/RUN_CLAUDIO_MISSION_CONTROL_v0_1_20260518/mission_control_snapshot/index.html`.
- Gates preserved: Cloud BLOCK_THIS_RUN, Kimi BLOCK_THIS_RUN, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- QA: focal 223 passed; 02_CLAUDIO 733 passed; Wabi 309 passed; safe-tests ok=true witness 41; GEODIA 74; DUAT 117; compileall PASS; HTTP smoke PASS; SecretScan/BoundaryScan/ScienceClaimGate PASS.
- No cloud, Kimi, NVIDIA, DeepSeek, push, deploy, publication or direct delete ran.

# ASSUMPTIONS

- La primera corrida debe reducir R sin crear archivo frio ni vault paralelo.
- `ROOT_BRAIN_OS` es canon base vivo, pero necesita validacion de runtime externo a ZIP.
- Las rutas sucias se revisan por valor, no por extraccion profunda completa.
- Candidatos de limpieza requieren confirmacion humana futura con la frase exacta definida.
- `New project 3` es la superficie React/Vite disponible para alojar `/telecom`.
- Run 2 prioriza central local mock antes de backend real.
# Run 3 - supuestos operativos

- La app React disponible para `/telecom` sigue siendo `C:\Users\L-Tyr\OneDrive\Documentos\New project 3`.
- Run 3 prioriza estabilidad y trazabilidad sobre features visuales grandes.
- `localStorage` es aceptable solo como primera capa local; el siguiente paso debe ser JSONL/SQLite.
- MCP debe arrancar read-only y solo desde ledger validado.
- Listar el directorio central del ZIP no equivale a validar contenido ni a autorizar expansion.

# Run 4 - supuestos operativos

- El path canonico del ledger durable es `02_RUNTIME/messagebus/logs/messagebus-main.jsonl`.
- El navegador no escribe a disco; solo puede exportar archivos descargables.
- Los scripts Node-only pueden leer/escribir JSONL local porque corren fuera del cliente.
- Run 5 debe construir MCP read-only sobre el JSONL verificado, no sobre estado browser.

# Run 5 - supuestos operativos

- `@modelcontextprotocol/sdk` es aceptable para MCP local stdio porque el prompt Run 5 autorizo instalarlo si era seguro.
- MCP read-only debe operar solo sobre el ledger JSONL durable y handlers derivados.
- El navegador debe mostrar estado MCP, no conectarse al servidor MCP.
- `messagebus:mcp:smoke` es la prueba minima de salud para Run 6 antes de crear A2A local.
- Run 6 puede crear fixtures/simulaciones locales, pero no debe escribir al ledger principal ni abrir red publica.

# Run 6 - supuestos operativos

- `scripts/agents` es la ubicacion correcta para codigo Node-only del bridge.
- Las Agent Cards locales son suficientes para simular routing sin adoptar A2A remoto.
- Reusar handlers puros de MCP es mas estable que invocar stdio desde tests.
- El panel `/telecom` debe reportar estado del bridge, no conectar el navegador al bridge.
- Run 7 debe crear propuestas firmadas en memoria antes de cualquier storage de proposals.

# Run 9 - supuestos operativos

- Restaurar dependencias con `npm ci` desde `package-lock.json` no cambia el set de dependencias del proyecto.
- Registrar `ack/resolve/block` como WitnessEvents derivados es el cierre local minimo compatible con la UI legacy.
- La validacion de `evidence_refs` debe ser el siguiente P2 antes de exponer mas resources derivados.
- Los resources derivados pueden salir en MCP porque son read-only y usan refs redactados.
- El siguiente paso seguro de migracion es un script dry-run que no toque el ledger principal.

## 2026-05-18 - Agent Chat Persistence/Search v0.3

- StateFingerprint: AGENT-CHAT-PERSISTENCE-SEARCH-v0-3-20260518.
- Agent Chat now has append-only persistent JSONL storage, hash-chain verification, local keyword search, filters, thread reconstruction and internal JSONL/Markdown export.
- Search/export/reconstruction do not execute tasks; draft creation still routes through TaskSpec/Workpack flows and execution remains behind GhostGate, rollback and WitnessLog.
- UI exposes Agent Chat Search with filters, hash-chain status, results and thread panel.
- Gates preserved: CloudLiveGate BLOCK_THIS_RUN, Kimi not run, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- Evidence: qa_artifacts/release_validation/RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518/.
- Tests: Agent Chat focal 204 passed; Wabi 309 passed; safe-tests ok witness 40; 02_CLAUDIO 714 passed; GEODIA 74 passed; DUAT predictive 117 passed; compileall PASS; HTTP smoke PASS; SecretScan artifacts PASS; BoundaryScan PASS; ScienceClaimGate PASS.
- Next: Claudio Mission Control dashboard v0.1 or public-safe Agent Chat architecture docs.
