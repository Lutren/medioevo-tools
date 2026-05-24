# Q-State Unificado: Audio, Luz, Física, Mecánicas

**Fingerprint:** DUAT-v1.3.0-Q-STATE-UNIFIED

## Codificación

| Q | Nombre | Audio | Luz | Física | Mecánicas |
|---|--------|-------|-----|--------|-----------|
| 00 | Silencio/Oscuridad Esperada | low hum, silence | oscuridad estable, sin sorpresas | equilibrio, inercia mínima | zona segura, recuperación |
| 01 | Señal Ausente/Anomalía | missing signal pulse | luz que debería estar y no está | inestabilidad, precursor de cambio | intriga, quest hook |
| 10 | Estable/Confirmado | tono sostenido, armónico | iluminación natural del entorno | movimiento predecible, colisiones normales | progresión normal |
| 11 | Burst/Evento | event burst, gate sound | flash, emisión brusca, revelación | colisión, explosión, transición de fase | gate abierto, NPC reactivo, quest trigger |

## Transiciones

Las transiciones Q generan eventos automáticos:

- `00 → 01`: missing_signal_pulse (audio) + luz ausente (visual)
- `01 → 11`: anomaly_burst (audio) + flash anómalo (visual)
- `10 → 11`: stable_burst (audio) + revelación (visual)
- `11 → 10`: burst_stabilize (audio) + calma post-evento (visual)

## Agregación

`qAggregate(states[], weights?)` — votación ponderada para determinar estado de grupo.

Usado para:
- Estado lumínico de una región
- Estado emocional de NPCs cercanos
- Estado de quest (residuo grupal)
