# A2A / MCP Compatibility Plan

## Objetivo

Hacer que MEDIOEVO MessageBus pueda traducirse a A2A y MCP sin convertir Run 2 en un servidor externo.

## Mapeo A2A

| MEDIOEVO | A2A |
|---|---|
| `AgentRecord` | Agent Card / AgentSkill parcial |
| `AgentMessage.thread_id` | context/task grouping |
| `AgentMessage.id` | message id |
| `MessageKind.task` | Task |
| `MessageKind.handoff` | task transition / message continuation |
| `artifact_refs` | Artifact |
| `created_at`, `updated_at` | task/message timestamps |
| `priority`, `R_estimado` | metadata extension |

Regla: A2A se adopta como protocolo de frontera entre agentes/sistemas, no como reemplazo del bus local. Primero se estabiliza el ledger local.

## Mapeo MCP

| MEDIOEVO | MCP |
|---|---|
| Agent Channels | Resources list/read |
| Bulletin export | Prompt o resource markdown |
| `createMessage` | Tool local con approval |
| `ackMessage` / `resolveMessage` | Tool local con audit |
| Artifact Registry | Resource templates |
| Operator Console | Cliente/host MCP futuro |

Regla: MCP se usa para exponer herramientas y recursos controlados. No se usa para saltar ActionGate, leer secretos o publicar.

## Orden recomendado

1. JSONL/SQLite local append-only.
2. Validador local de schema/hash/canales.
3. MCP server read-only: listar canales, leer bulletin, leer handoffs.
4. MCP tools con approval: ack/resolve/create task.
5. A2A Agent Card local para `codex_engineer`, `security_gate`, `cerebro_canon`.
6. A2A tasks solo en loopback o entorno local privado.

## No tomar todavia

- Descubrimiento remoto publico.
- HTTP externo.
- OAuth/credenciales.
- Push notifications.
- Agentes remotos escribiendo en el ledger sin gate local.
