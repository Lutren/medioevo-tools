# DUAT Telecom Core

Producto: DUAT Telecom Core

Nombre tecnico: MEDIOEVO MessageBus

Estado: LOCAL_MOCK_FUNCIONAL

## Objetivo

Convertir el handoff estatico del arbol vivo en una central de telecomunicaciones entre agentes. El sistema no intenta ejecutar agentes externos ni publicar informacion; organiza continuidad, tareas, evidencia y alertas como mensajes verificables.

## Componentes

| Componente | Rol | Canal base |
|---|---|---|
| Bulletin Board | Boletin visible para todos los agentes | `#system_announcements` |
| Agent Inbox | Mensajes entrantes por agente | derivado de `to_agents` y `cc_agents` |
| Agent Outbox | Mensajes emitidos por agente | derivado de `from_agent` |
| Task Queue | Trabajo abierto con prioridad y evidencia | `#tasks` |
| Handoff Stream | Transferencias de continuidad con fingerprint | `#handoffs` |
| WitnessLog Stream | Eventos append-only con hash | `#witnesslog` |
| Alert Channel | P0, bloqueo, riesgos inmediatos | `#security_review` |
| Canon Update Channel | Cambios de canon y frontera epistemica | `#canon_updates` |
| Security Review Channel | Secretos, privacidad, publicacion, ZIPs | `#security_review` |
| Artifact Registry | Reportes, builds, exports y rutas | `#build_reports` |
| Decision Ledger | Decisiones con evidencia y no reapertura sin prueba | `#witnesslog`, `#canon_updates` |
| Human Brief Board | Resumen visible para operador humano con R, tiempos y accion | `/telecom` |
| Operator Console | Vista humana local | `/telecom` |

## Principios

- Local first: no backend externo en Run 2.
- Append-only por defecto: WitnessLog y decisiones se agregan, no se reescribe historia.
- Evidencia antes que volumen: todo mensaje importante apunta a `evidence_refs` o `artifact_refs`.
- Seguridad primero: rutas con secreto, publicacion o ZIP grande quedan en `security_review`.
- A2A/MCP compatible sin depender de red: los IDs, canales y mensajes se pueden traducir a Agent Cards, tasks, resources, tools y prompts.
- Lectura humana primero: `/telecom` debe abrir con brief inteligente antes de mostrar todo el detalle.
- R visible: `R_estimado` se muestra como escala `0 verde -> 1 rojo/jamming`; en medios sin color se conserva la etiqueta textual.

## Formato humano `/telecom`

La consola debe mostrar:

- Titulo del ultimo handoff o bulletin relevante.
- `summary` o resumen derivado del mensaje.
- `prompt_started_at`: cuando se mando el prompt o inicio la solicitud.
- `work_delivered_at`: cuando se entrego el trabajo.
- Estado R con gradiente verde, amarillo, naranja, rojo y etiqueta textual.
- Lo importante: P0 abiertos, handoffs abiertos, tareas abiertas, hash-chain/schema y accion o bloqueo principal.
- Detalle completo: todos los paneles de mensajes, canales, WitnessLog, tareas, canon, seguridad y artefactos.

## Estado Run 2

CERTEZA:

- Existe servicio mock TypeScript en `New project 3/src/messagebus/service.ts`.
- Existe UI local en `New project 3/src/ui/TelecomCore.tsx`.
- Build y tests React pasaron.

INFERENCIA:

- El sistema ya sirve como bulletin/inbox/outbox local.
- El siguiente salto real es persistencia local append-only.

INCOGNITA:

- No hay backend real.
- No hay autenticacion de agentes.
- No hay reconciliacion automatica con COMMS Claudio.

## Gate

APPROVE:

- Crear/leer mensajes locales.
- Exportar bulletin Markdown local.
- Exportar JSON local.
- Ejecutar tests/build locales.

REVIEW:

- Conectar con COMMS vivo.
- Usar SQLite compartido.
- Importar ZIP reconstructivo.
- Exponer por HTTP.

BLOCK:

- Publicar, deploy, push.
- Imprimir secretos.
- Mover/borrar/renombrar fuentes.
