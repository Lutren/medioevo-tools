# MESSAGEBUS MCP READONLY PLAN

Fecha: 2026-05-12

Producto: DUAT Telecom Core

Nombre tecnico: MEDIOEVO MessageBus

Estado: READONLY_PLAN / NO_SERVER_YET

## Objetivo

Exponer el MessageBus como recursos MCP locales de solo lectura antes de habilitar herramientas de escritura. El primer servidor MCP no debe publicar, sincronizar, borrar, mover ni leer secretos; solo debe servir vistas derivadas del ledger local validado.

## Recursos MCP propuestos

| Resource URI | Lectura | Fuente local |
|---|---|---|
| `medioevo://messagebus/latest` | Ultimo bulletin o estado del bus | append-only JSONL / `exportBulletinMarkdown()` |
| `medioevo://messagebus/channels` | Registry de canales permitidos | `channelRegistry.ts` |
| `medioevo://messagebus/handoffs/latest` | Ultimo handoff Markdown | `exportLatestHandoffMarkdown()` |
| `medioevo://messagebus/tasks/open` | Tareas no resueltas | append-only log filtrado por `kind=task` |
| `medioevo://messagebus/witnesslog/recent` | Eventos y mensajes de cierre recientes | append-only log + WitnessLog futuro |
| `medioevo://messagebus/security/p0` | P0 abiertos y security review | append-only log filtrado por `priority=P0` |

## Herramientas futuras

Estas herramientas quedan FUTURE / REQUIRES ACTIONGATE:

| Tool | Estado | Gate |
|---|---|---|
| `create_message` | FUTURE | Validacion schema/canal/hash + ActionGate |
| `ack_message` | FUTURE | Append-only transition, no overwrite |
| `append_witness_event` | FUTURE | WitnessLog hash-chain |
| `create_handoff` | FUTURE | Fingerprint + evidencia obligatoria |
| `claim_task` | FUTURE | Actor permitido + task abierta |
| `resolve_task` | FUTURE | Evidencia de cierre obligatoria |

## No implementar todavia

- Servidor HTTP externo.
- Supabase.
- Credenciales.
- Escritura remota.
- Push/deploy/publicacion.
- Lectura de contenidos internos de ZIP en `SECURITY_REVIEW`.

## Criterio de entrada al servidor MCP

APPROVE local solo si:

- `npm run build` pasa.
- `npm test` pasa.
- `verifyLog()` retorna `ok=true`.
- `MESSAGEBUS_HASHCHAIN_REPORT.md` confirma SHA-256 o documenta fallback.
- Los recursos exponen solo rutas/estado, no secretos ni contenido editorial privado.
