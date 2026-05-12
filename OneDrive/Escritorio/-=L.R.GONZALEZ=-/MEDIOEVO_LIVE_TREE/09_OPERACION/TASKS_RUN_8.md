# TASKS RUN 8

Fecha: 2026-05-12

Fingerprint entrada esperado: `MDV-ACTIONGATE-RUN7-6B2E`

## Objetivo

Crear Operator-approved execution sandbox para propuestas ActionGate.

Run 8 no debe abrir ejecucion general. Debe permitir solo dry-run y ejecucion segura limitada bajo aprobacion local explicita.

## P0

- Mantener MCP read-only.
- No habilitar write tool MCP operacional.
- No escribir al MessageBus principal salvo una futura propuesta low-risk con aprobacion manual local y sandbox.
- No deploy.
- No push.
- No publicacion.
- No delete/move/rename.
- No DNS.
- No Supabase/backend externo.
- No secretos.
- No ZIP canon.

## P1

- Crear dry-run executor para propuestas ActionGate.
- Crear approval token manual local.
- Validar token contra proposalHash y decisionHash.
- Ejecutar solo en sandbox temporal.
- Permitir inicialmente solo:
  - `create_task` sandbox;
  - `update_handoff` sandbox;
  - `append_message` sandbox contra log temporal, no principal.
- Mantener `publish_release`, `modify_file` high-risk y `delete_or_move` como no ejecutables.
- Crear rollback evidence antes de cualquier apply.
- Crear tests para:
  - token ausente bloquea;
  - token incorrecto bloquea;
  - seal alterado bloquea;
  - policy BLOCK bloquea;
  - execution writes only sandbox paths;
  - MessageBus principal unchanged;
  - deploy/delete/move/DNS siguen bloqueados.

## P2

- Disenar promocion futura de sandbox a apply real con gate humano.
- Crear resource read-only futuro:
  `actiongate://proposals/pending`.
- Crear export Markdown de proposal + decision + plan.
- Conectar `/telecom` a snapshot estatico generado, sin browser filesystem directo.

## Criterio de cierre

- Dry-run executor existe.
- Approval token manual local existe.
- Sandbox ejecuta solo low-risk en rutas temporales.
- MessageBus principal no cambia.
- Propuestas bloqueadas no se ejecutan.
- Tests pasan.
- `messagebus:mcp:smoke` pasa.
- `agents:bridge:smoke` pasa.
- `actiongate:smoke` pasa.
- `/telecom` responde 200.
