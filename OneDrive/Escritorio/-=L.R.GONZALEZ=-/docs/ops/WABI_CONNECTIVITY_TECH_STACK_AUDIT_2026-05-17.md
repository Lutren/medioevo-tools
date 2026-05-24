# WABI_CONNECTIVITY_TECH_STACK_AUDIT_2026-05-17

## Alcance

Analisis local de conexion entre Wabi, Claudio, MessageBus, MCP/A2A, proveedores LLM y tecnologia externa comparable a Lovable/GDevelop.

Frontera aplicada:

- No se reparo Wabi.
- No se modifico codigo dentro de `apps/local/wabi-sabi`.
- No se detuvieron procesos, ventanas Codex ni servidores locales.
- No se publico, no se hizo push, no se instalo dependencias con red.
- Este reporte queda en `docs/ops/` para no interferir con el agente que esta trabajando Wabi.

ActionGate: `APPROVE` para lectura local, health checks HTTP locales y reporte. `REVIEW` para instalar tecnologia nueva o cambiar arquitectura. `BLOCK` para publicar, exponer secretos, borrar, tocar videojuego privado o saltar seguridad del host.

## Conclusion ejecutiva

La direccion tecnica correcta no es meter otra plataforma completa encima de Wabi. La mejor ruta es consolidar un solo plano de control local:

```txt
Humano / Operador
  -> Wabi CLI / Cockpit / Telecom
  -> ActionGate
  -> MessageBus append-only + WitnessLog
  -> MCP read-only resources
  -> A2A/Agent Cards locales para agentes
  -> Codex / OpenAI Responses / Ollama / proveedores cloud gated
  -> PatchPlan + SafeExecutor + RollbackStore
  -> Artifacts + NEXT_SESSION_BRIEF + SESSION_FINGERPRINT
```

MCP debe ser el protocolo de herramientas y recursos. A2A debe ser el protocolo entre agentes. OpenAI Responses/Codex debe quedar como motor de razonamiento/programacion de alta calidad. Ollama debe quedar como bucle local barato y opcional. GDevelop, Dyad, OpenHands y bolt.diy deben usarse como fuentes de ingenieria/patrones bajo curaduria, no como otro silo vivo.

El problema principal observado no es falta de tecnologia. Es falta de un contrato unico de salud/conexion que diga, en una sola salida JSON, que ruta Wabi manda, que servidor esta vivo, que bus central existe, que proveedor esta activo, que gates aplican y que evidencia de test respalda el estado.

## Verdad operacional observada

Rutas y servicios locales relevantes:

- Ruta canonica Wabi segun documentos locales: `apps/local/wabi-sabi`.
- Cockpit Wabi activo en BRAIN_OS: `127.0.0.1:8787`, servicio `wabi-local-cockpit`, version `0.6`, provider activo `nvidia`, `publication_gate=BLOCK`.
- Claudio HTTP server activo: `127.0.0.1:7474`.
- Ollama activo: `127.0.0.1:11434`, version `0.24.0`.
- Proceso `apps/local/wabi-sabi/adapters/stub_nemotron.py` activo, pero sin puerto escuchando observado en `netstat`.
- No se observo listener en `127.0.0.1:3737` durante este pase.
- Hay sesiones Codex visibles ejecutando con `--sandbox danger-full-access --yolo`; no se tocaron porque pueden ser sesiones humanas/agentes activas, pero no deben ser arquitectura productiva para Wabi.

Estado de backlog:

- `pending_review.py --write --quiet` genero snapshot de 2026-05-17.
- Resultado: `active_dedup=19`, `claudio_open=0`.
- Esto confirma que hay deuda de continuidad, pero no hay un bloqueo Claudio abierto en ese snapshot.

## Stack recomendado

### 1. Bus y memoria operacional

Usar MessageBus local como centro:

- Persistencia append-only en JSONL/SQLite.
- Hashchain y replay para verificar continuidad.
- `WitnessLog` para evidencia de acciones.
- `NEXT_SESSION_BRIEF` y `SESSION_FINGERPRINT` como salida humana/agente.

Esto encaja con Observacionismo: los datos persisten, el operador no. No se resuelve cargando mas contexto; se resuelve externalizando estado verificable.

### 2. MCP como frontera de lectura/herramientas

MCP debe exponer:

- Logs.
- Agents.
- Tasks.
- Handoffs.
- WitnessLog.
- Artifacts.
- Health.
- Bulletin/latest.

Primero read-only. Las herramientas de escritura deben quedar atras de ActionGate, PatchPlan, SafeExecutor y rollback.

### 3. A2A como frontera entre agentes

A2A debe usarse para que agentes se descubran y colaboren sin compartir memoria interna ni herramientas privadas. El patron local correcto es:

- Agent Cards locales.
- JSON-RPC/HTTP o transporte local solo cuando haya contrato.
- Cero descubrimiento publico.
- Cero push externo.
- A2A para cooperacion entre agentes, MCP para herramientas/recursos.

### 4. Wabi como motor modular, no como silo paralelo

Wabi debe ser el ejecutor local que sabe:

- Crear planes de parche.
- Ejecutar cambios seguros.
- Correr tests seguros.
- Guardar rollback.
- Redactar secretos.
- Registrar evidencia.
- Usar proveedores con gate.

No debe duplicar MessageBus ni COMMS. Debe consumirlos.

### 5. Proveedores LLM

Orden recomendado:

1. `codex` / OpenAI Responses para programacion, razonamiento y refactors complejos.
2. `ollama` local para bucles baratos, clasificacion, resumen, revision preliminar y tareas sin red.
3. Proveedores cloud compatibles OpenAI solo con `WABI_ALLOW_CLOUD_PROVIDERS` y reporte presence-only, sin imprimir secretos.
4. `dry-run` siempre disponible como fallback verificable.

El codigo local de Wabi ya va en esa direccion: blueprint policy conservadora, cloud adapters gated, redaccion de errores, Codex bridge con modo CLI read-only y OpenAI Responses.

### 6. Ingenieria externa aprovechable

Usar estas fuentes como tarjetas de ingenieria, no como absorcion ciega:

- GDevelop: patrones de motor 2D/3D, eventos, extensiones, behaviors, export HTML5, separacion IDE/engine.
- Dyad: app builder local, BYO keys, privacidad, Electron/TypeScript, alternativa Lovable/Bolt/v0.
- OpenHands: agente de desarrollo con SDK, CLI, GUI local y arquitectura para agentes de software.
- bolt.diy: multi-provider app builder, diffs, snapshots, file locking, MCP, Electron, proyectos full-stack en navegador.

Regla: si se reusa codigo, registrar licencia y avisos. Para Wabi conviene mas clean-room: extraer patrones y contratos, no importar repos completos.

## Brechas reales

1. Existen dos superficies Wabi vivas:
   - `apps/local/wabi-sabi`.
   - `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py` en `127.0.0.1:8787`.

   Falta declarar si BRAIN_OS Cockpit es UI/servidor operador de Wabi, o si es una implementacion paralela que debe ser absorbida por la ruta canonica.

2. Falta un `wabi health --json` o endpoint equivalente que una:
   - canonical_path.
   - active_server.
   - provider_status.
   - ollama_status.
   - codex_status.
   - mcp_status.
   - messagebus_status.
   - actiongate_status.
   - publication_gate.
   - last_test_evidence.

3. El status documental de MessageBus/MCP esta atrasado:
   - Docs antiguas dicen plan read-only.
   - En `New project 3` ya existe `scripts/messagebus/mcp-server.mjs` y adaptadores/test MCP.
   - Debe reconciliarse en un solo documento de verdad, sin copiar codigo a ciegas.

4. El arbol git esta muy sucio y con muchos cambios/untracked. Antes de cualquier commit o migracion, se requiere aislamiento por modulo y no broad-stage.

5. Las sesiones Codex con `danger-full-access --yolo` son un riesgo operacional. No las toque, pero Wabi no debe depender de ese modo. La arquitectura Wabi debe usar read-only por defecto y write via PatchPlan/SafeExecutor.

## Decision tecnica recomendada

Declarar esta regla:

```txt
Wabi no es "otro proyecto".
Wabi es la capa de ejecucion local modular dentro del sistema MEDIOEVO/CLAUDIO.
MessageBus es el bus central.
MCP expone estado y herramientas.
A2A conecta agentes.
ActionGate decide acciones.
WitnessLog prueba lo que ocurrio.
Codex/Responses/Ollama/proveedores son motores intercambiables, no dueños del sistema.
```

## Proxima accion segura para el agente que esta reparando Wabi

Crear primero el contrato unico de salud:

```txt
wabi health --json
```

Debe devolver una sola verdad local, aunque internamente lea `provider-status`, Cockpit `8787`, Ollama `11434`, MCP/MessageBus y ActionGate.

No debe escribir codigo de features nuevas hasta que ese health contract exista y pueda probarse.

## Evidencia local

Comandos ejecutados:

```powershell
python tools\release\pending_review.py --write --quiet
git status --short
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'wabi|Wabi|codex|ollama|claudio_api_server|startup_sequence' }
netstat -ano | Select-String -Pattern ':8787|:7474|:47747|:3737|:11434'
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8787/health' -TimeoutSec 5
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:11434/api/version' -TimeoutSec 5
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:7474' -TimeoutSec 5
```

Resultados clave:

- `pending_review date=2026-05-17 active_dedup=19 claudio_open=0`.
- `127.0.0.1:8787` responde 200 con `wabi-local-cockpit`, version `0.6`.
- `127.0.0.1:11434` responde 200 con Ollama `0.24.0`.
- `127.0.0.1:7474` responde 200.
- No listener observado en `3737`.
- `stub_nemotron.py` esta vivo como proceso, pero no como puerto escuchando.

## Fuentes externas consultadas

- MCP official docs: https://modelcontextprotocol.io/docs/getting-started/intro
- A2A official docs: https://a2a-protocol.org/latest/
- A2A GitHub: https://github.com/a2aproject/A2A
- OpenAI tools / Responses docs: https://platform.openai.com/docs/guides/tools?api-mode=responses
- OpenAI Responses migration docs: https://platform.openai.com/docs/guides/migrate-to-responses
- GDevelop GitHub: https://github.com/4ian/GDevelop
- Dyad GitHub: https://github.com/dyad-sh/dyad
- OpenHands GitHub: https://github.com/OpenHands/OpenHands
- bolt.diy GitHub: https://github.com/stackblitz-labs/bolt.diy
