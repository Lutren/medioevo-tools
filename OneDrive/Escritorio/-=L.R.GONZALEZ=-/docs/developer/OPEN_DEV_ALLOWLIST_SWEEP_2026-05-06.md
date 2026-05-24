# Open Dev Allowlist Sweep - 2026-05-06

Estado: `LOCAL_VALIDATION_ONLY / NO_PUBLICATION`

Este barrido valida los paquetes `open-dev` por allowlist, pruebas locales
ligeras, imports y scan focalizado. No se publico, no se hizo push, no se
generaron ZIPs, no se cambiaron licencias y no se tocaron rutas privadas.

## Gate

| item | valor |
|---|---|
| operador | autorizo continuar con criterio |
| host gate | `CONTAMINADO/REVIEW` |
| accion permitida | `recalibrate` |
| `R` | `0.474` |
| `Phi_eff` | `0.493` |
| `lambda_sat` | `0.875` |
| dominante | `r_mem` |

Lectura: se permite evidencia local ligera. No se permite publicacion externa ni
expansion amplia.

## Tests / Imports

| target | resultado |
|---|---|
| `packages/open-dev/obsai-core` | `29 passed in 1.19s` |
| `packages/open-dev/residueos` | `7 passed in 1.07s` |
| `packages/open-dev/gemma-observacionismo-cleanup` | `3 passed in 0.02s` |
| `packages/open-dev/obs-safe-integration-kit` | `4 passed in 0.10s` |
| `packages/open-dev/duat-genesis` | `3 passed in 0.22s` |
| `packages/open-dev/observacionismo-gate` | import OK: `observacionismo_gate` |
| `packages/open-dev/claudio-os-blueprint` | manifest/hash only; no pytest dedicado en runner |

## Secret Scan Focalizado

Todos los targets reportaron `count_reported=0` con:

```powershell
python tools\release\scan_secrets.py --product <target> --json
```

Targets escaneados:

- `obsai-core`
- `residueos`
- `gemma-observacionismo-cleanup`
- `obs-safe-integration-kit`
- `duat-genesis`
- `observacionismo-gate`
- `claudio-os-blueprint`

## Manifest Summary

| target | files | blocked | excluded | bytes |
|---|---:|---:|---:|---:|
| `obsai-core` | 28 | 0 | 21 | 129090 |
| `residueos` | 13 | 0 | 12 | 44427 |
| `gemma-observacionismo-cleanup` | 12 | 0 | 7 | 12473 |
| `obs-safe-integration-kit` | 20 | 0 | 10 | 56161 |
| `duat-genesis` | 11 | 0 | 8 | 15711 |
| `observacionismo-gate` | 9 | 0 | 1 | 15319 |
| `claudio-os-blueprint` | 35 | 0 | 0 | 41465 |

## Resultado

`open-dev` queda verificado localmente por allowlist actual. Esto no autoriza
publicacion nueva ni re-publicacion. Para push/release externo se requiere:

- host gate no bloqueante y target-specific ActionGate;
- staging limpio o allowlist exacta;
- path scrub publico;
- claims scan publico;
- licencia por target confirmada;
- verificacion post-publicacion.
