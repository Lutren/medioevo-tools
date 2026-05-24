# HANDOFF

Handoff resume estado, decisiones, evidencias, pendientes y proxima accion verificable.

## Formato obligatorio

Todo handoff operativo debe separar:

- `prompt_started_at`: fecha/hora ISO cuando se mando el prompt o inicio la solicitud.
- `work_delivered_at`: fecha/hora ISO cuando el agente entrega el trabajo.
- `BRIEF INTELIGENTE`: resumen humano, estado R, tiempos, siguiente accion y bloqueo principal.
- `DETALLE COMPLETO`: estado, cuerpo, certeza, inferencia, incognita, accion, artefactos, evidencia, hash y fingerprint.

## Escala R

R se muestra de `0 verde` a `1 rojo/jamming`. En Markdown sin color se escribe la etiqueta textual: `VERDE`, `AMARILLO`, `NARANJA`, `ROJO` o `JAMMING`.

## Regla de dashboard

El dashboard de agentes debe abrir con el brief humano y despues mostrar todo el bus: bulletin, inbox, outbox, canales, handoffs, WitnessLog, P0, tareas, canon, seguridad y artefactos.
