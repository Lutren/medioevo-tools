## 2026-05-18 - Claudio Mission Control dashboard v0.1

- StateFingerprint: CLAUDIO-MISSION-CONTROL-v0-1-20260518.
- Implemented `/api/mission-control` as LOCAL_ONLY_READONLY aggregator for agents, Agent Chat, workpacks, scheduler, BrowserBridge, provider, tree health, coding acceptance, risks and evidence.
- Wabi UI includes `Claudio Mission Control` panel with no execution buttons in the Mission Control section.
- Static internal snapshot exists at `qa_artifacts/release_validation/RUN_CLAUDIO_MISSION_CONTROL_v0_1_20260518/mission_control_snapshot/index.html`.
- Gates preserved: Cloud BLOCK_THIS_RUN, Kimi BLOCK_THIS_RUN, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- QA: focal 223 passed; 02_CLAUDIO 733 passed; Wabi 309 passed; safe-tests ok=true witness 41; GEODIA 74; DUAT 117; compileall PASS; HTTP smoke PASS; SecretScan/BoundaryScan/ScienceClaimGate PASS.
- No cloud, Kimi, NVIDIA, DeepSeek, push, deploy, publication or direct delete ran.

# TEST_REPORT

## Comandos ejecutados

- `python tools/live_tree_scan.py`
- `python tools/secret_scan.py`
- Verificacion PowerShell de artefactos requeridos: `MISSING_COUNT=0`

## Resultado

- Inventario vivo: `2592` registros.
- Secret scan: `2601` archivos candidatos escaneados, `475` hallazgos enmascarados.
- Artefactos obligatorios verificados: `18/18`.

## Estado

PASSED para generacion de artefactos locales.

BLOCK para publicacion/push/deploy por hallazgos de secret scan.

## Run 2 - DUAT Telecom Core

- `npm test -- --runInBand`: `FAILED_EXPECTED`; Vitest 2.1.9 no reconoce esa bandera.
- `npm run build`: `PASSED` en `C:\Users\L-Tyr\OneDrive\Documentos\New project 3`.
- `npm test`: `PASSED`, 2 test files, 15 tests.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python `test_*.py` / `*_test.py`.
- `Start-Process npm.cmd run dev -- --port 5174`: `PASSED_LOCAL`; Vite sirve la app nueva.
- `Invoke-WebRequest http://127.0.0.1:5174/telecom`: `PASSED_LOCAL`; root de Vite servido.
- `Invoke-WebRequest http://127.0.0.1:5174/src/App.tsx`: `PASSED_LOCAL`; contiene `TelecomCore` y `/telecom`.
- `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx`: `PASSED_LOCAL`; contiene paneles clave del Telecom Core.

Reporte detallado: `10_QUALITY/TELECOM_CORE_TEST_REPORT.md`.

## Run 3 - MessageBus Validator / Append-only Core

- `npm test -- src/messagebus`: `PASSED`, 5 test files, 15 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm test`: `PASSED`, 6 test files, 26 tests.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python `test_*.py` / `*_test.py`.
- `Invoke-WebRequest http://127.0.0.1:5174/telecom`: `PASSED_LOCAL`.
- `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx`: `PASSED_LOCAL`; contiene `MessageBus Health`, `Validate Log` y `Export JSONL`.
- Canon ZIP SHA256: `PASSED_MATCH`; no se extrajo contenido.

Reportes detallados:

- `10_QUALITY/MESSAGEBUS_VALIDATOR_TEST_REPORT.md`
- `10_QUALITY/MESSAGEBUS_HASHCHAIN_REPORT.md`
- `10_QUALITY/MESSAGEBUS_APPEND_ONLY_REPORT.md`
- `10_QUALITY/MESSAGEBUS_MCP_READONLY_PLAN_STATUS.md`
- `10_QUALITY/CANON_ZIP_SECURITY_REVIEW_STATUS.md`

## Run 4 - Durable MessageBus JSONL + Replay Verifier

- `npm test -- src/messagebus`: `PASSED`, 6 test files, 24 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm test`: `PASSED`, 7 test files, 35 tests.
- `npm run messagebus:append-sample`: `PASSED`.
- `npm run messagebus:verify`: `PASSED`, `ok=true`, `totalEntries=1`.
- `npm run messagebus:replay`: `PASSED`, `totalEntries=1`.
- `npm run messagebus:stats`: `PASSED`, `fileSizeBytes=2883`.
- `npm run messagebus:export-md`: `PASSED`.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python.
- `/telecom`: `PASSED_LOCAL`.

Reporte detallado: `10_QUALITY/MESSAGEBUS_DURABLE_TEST_REPORT.md`.

## Run 5 - MessageBus MCP Read-only Server

- `npm install @modelcontextprotocol/sdk`: `PASSED`; SDK 1.29.0 instalado.
- `npm test -- src/messagebus`: `PASSED`, 7 test files, 37 tests.
- `npm test`: `PASSED`, 8 test files, 48 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: `PASSED`, `ok=true`, resources 7, tools 8.
- MCP server factory import: `PASSED`, `hasConnect=true`.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python.
- `/telecom`: `PASSED_LOCAL`, HTTP 200.
- `TelecomCore.tsx`: `PASSED_LOCAL`; contiene `MCP Read-Only Layer` y no contiene SDK MCP ni Node-only imports.
- `npm audit --omit=dev --json`: `PASSED`, 0 prod vulnerabilities.
- `npm audit --json`: `REVIEW`, 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain.

Reporte detallado: `10_QUALITY/MESSAGEBUS_MCP_READONLY_TEST_REPORT.md`.

## Run 6 - Agent Bridge / A2A local adapter

- `npm test -- src/messagebus`: `PASSED`, 8 test files, 51 tests.
- `npm test`: `PASSED`, 9 test files, 62 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: `PASSED`, `ok=true`, resources 7, tools 8.
- `npm run agents:bridge:smoke`: `PASSED`, `ok=true`, agents 6.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python.
- `/telecom`: `PASSED_LOCAL`, HTTP 200.
- `TelecomCore.tsx`: `PASSED_LOCAL`; contiene `Agent Bridge / Local A2A Layer` y no contiene SDK MCP ni Node-only imports.
- `npm audit --omit=dev --json`: `PASSED`, 0 prod vulnerabilities.
- `npm audit --json`: `REVIEW`, 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain.

Reporte detallado: `10_QUALITY/AGENT_BRIDGE_RUN_6_TEST_REPORT.md`.

## Run 9 - Pending closeout / MessageBus transition events

- `npm ci`: `PASSED`; dependencias restauradas desde `package-lock.json`, sin modificar manifests. `npm audit` reporto 5 moderadas dev en Vite/Vitest/esbuild.
- `node scripts\messagebus\verify.mjs`: `PASSED`, `ok=true`, `totalEntries=1`.
- `node scripts\messagebus\replay.mjs`: `PASSED`, `ok=true`, `openTasks=0`, `p0Count=0`.
- `node scripts\messagebus\export-md.mjs`: `PASSED`, export a `02_RUNTIME/messagebus/exports/messagebus-replay.md`.
- `node scripts\messagebus\stats.mjs`: `PASSED`, `fileSizeBytes=2883`.
- `npm test -- src/messagebus`: `PASSED`, 10 test files, 88 tests.
- `npm test`: `PASSED`, 11 test files, 99 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: `PASSED`, `ok=true`, resources 7, tools 8.
- `npm run agents:bridge:smoke`: `PASSED`, `ok=true`, agents 6, remote network disabled, write tools disabled.
- `npm run actiongate:smoke`: `PASSED`, `status=PASS`, proposal ledger verified, `mainMessageBusMutation=NOT_DETECTED`.
- `npm run actiongate:sandbox:smoke`: `PASSED`, sandbox-only execution, production mutation false, publish/delete blocked.
- `npm audit --omit=dev --json`: `PASSED`, 0 prod vulnerabilities.
- `npm audit --json`: `REVIEW`, 5 moderate dev vulnerabilities; fix requires semver-major Vite/Vitest upgrade.

Cambio validado:

- `ackMessage`, `resolveMessage` y `blockMessage` conservan compatibilidad legacy y agregan eventos derivados `message.ack`, `message.resolve` y `message.block` en WitnessLog append-only.
- `blockMessage` registra `status=blocked` sin persistir la razon sensible dentro del evento derivado.

## Run 9B - Derived MCP resources / evidence ref redaction

- `npm test -- src/messagebus`: `PASSED`, 10 test files, 90 tests.
- `npm test`: `PASSED`, 11 test files, 101 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: `PASSED`, `ok=true`, resources 10, tools 8.
- `npm run agents:bridge:smoke`: `PASSED`, `ok=true`, agents 6.
- `npm run actiongate:smoke`: `PASSED`, `status=PASS`, `mainMessageBusMutation=NOT_DETECTED`.
- `npm run actiongate:sandbox:smoke`: `PASSED`, sandbox-only, production mutation false.
- `npm audit --omit=dev --json`: `PASSED`, 0 prod vulnerabilities.
- `npm audit --json`: `REVIEW`, 5 moderate dev vulnerabilities; fix requires semver-major Vite/Vitest upgrade.

Cambio validado:

- MCP read-only expone `messagebus://artifacts`, `messagebus://bulletin/latest` y `messagebus://security/p0`.
- `evidence_refs` y `artifact_refs` secret-like se exponen como `REDACTED_REF` con fingerprint, no como valor/ruta completa.
- Se creo `03_SYSTEMS/MESSAGEBUS_LOCALSTORAGE_TO_JSONL_MIGRATION.md` como diseno seguro de migracion browser `localStorage` -> JSONL durable.

## 2026-05-18 - Agent Chat Persistence/Search v0.3

- StateFingerprint: AGENT-CHAT-PERSISTENCE-SEARCH-v0-3-20260518.
- Agent Chat now has append-only persistent JSONL storage, hash-chain verification, local keyword search, filters, thread reconstruction and internal JSONL/Markdown export.
- Search/export/reconstruction do not execute tasks; draft creation still routes through TaskSpec/Workpack flows and execution remains behind GhostGate, rollback and WitnessLog.
- UI exposes Agent Chat Search with filters, hash-chain status, results and thread panel.
- Gates preserved: CloudLiveGate BLOCK_THIS_RUN, Kimi not run, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.
- Evidence: qa_artifacts/release_validation/RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518/.
- Tests: Agent Chat focal 204 passed; Wabi 309 passed; safe-tests ok witness 40; 02_CLAUDIO 714 passed; GEODIA 74 passed; DUAT predictive 117 passed; compileall PASS; HTTP smoke PASS; SecretScan artifacts PASS; BoundaryScan PASS; ScienceClaimGate PASS.
- Next: Claudio Mission Control dashboard v0.1 or public-safe Agent Chat architecture docs.
