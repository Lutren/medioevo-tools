# EML en el Motor

**Fingerprint:** DUAT-v1.3.0-EML-ENGINE

> Math canon update 2026-05-20: la formula vieja queda `DEPRECATED`. Usar
> `07b_MATEMATICAS_RIGUROSO.md` y EML sigmoidal para cualquier calculo nuevo.

## Fórmula

```
DEPRECATED: EML(x, y) = exp(x) - ln(y)
CANON_07B: EML(s,c; alpha,beta,theta) = sigma(alpha*s - beta*log(1+c) - theta)
CANON_07B: sigma(z) = 1 / (1 + exp(-z))
```

## Interpretación Operacional

| Modo | Condición | Acción |
|------|-----------|--------|
| EXPAND | EML > 0.5 | Más subpasos, full detail, emissive ON |
| THRESHOLD | EML = 0.5 | Pasos normales, propagated detail |
| COMPRESS | EML < 0.5 | Menos pasos, ambient only, emissive OFF |

## Parámetros

- **s (señal):** energía local, lux, presión, velocidad
- **c (costo/residuo):** R_scene, contradicción vecinal, ruido
- **alpha, beta, theta:** parametros aprendibles o calibrados por benchmark

## Usos

1. **Substepping físico:** `emlSubsteps(energy, residue, maxSteps)`
2. **Selector LOD luz:** `emlLOD(complexity, sceneResidue)`
3. **Gate de integración:** `emlGate(clarity, residue)` → INTEGRATE/TEST/HOLD/BLOCK

## Propiedad Clave

EML no es umbral fijo. Es **selector dinámico** que expande donde la señal es fuerte y el residuo bajo, y comprime donde el costo supera el beneficio.
