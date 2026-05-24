# GhostGate / Sistema de Atención

## Principio

Si no reduce residuo, no pasa.

## Filtros por Defecto

| Canal | Umbral | Ruido Máx | R Máx | Patrón |
|-------|--------|-----------|-------|--------|
| Audio | 0.1 | 0.6 | 0.7 | reduce_residue |
| Visual | 0.2 | 0.5 | 0.6 | novelty_or_goal |
| Physics | 0.05 | 0.8 | 0.8 | delta_state |
| NPC | 0.3 | 0.4 | 0.5 | goal_aligned |

## Bloqueo

- Señal débil (< umbral)
- Ruido alto (> máx)
- Sistema saturado (R > máx)
- Aumenta residuo (predicción > 0)
