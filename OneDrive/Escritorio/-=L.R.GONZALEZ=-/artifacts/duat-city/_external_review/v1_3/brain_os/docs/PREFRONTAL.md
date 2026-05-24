# Prefrontal / ActionGate Executive

## Principio

No ejecutar sin gate. No gastar sin presupuesto.

## Reglas

| Condición | Acción |
|-----------|--------|
| R > 0.5 | Comprimir LOD de todos los motores |
| Phi_eff < 0.3 | Bloquear tareas no críticas |
| CPU > 80% | Bajar render LOD, mantener audio |
| Memoria > 400MB | Desactivar simulación social |
| JAMMED | Solo audio, todo lo demás OFF |

## Prioridades de Motor

1. Audio (10) — nunca se corta
2. Physics (8) — base del mundo
3. NPC (7) — inteligencia
4. Light (6) — ambiente
5. Render (5) — visual (puede bajar)
6. Quest (4) — misiones
7. Simulation (3) — social
