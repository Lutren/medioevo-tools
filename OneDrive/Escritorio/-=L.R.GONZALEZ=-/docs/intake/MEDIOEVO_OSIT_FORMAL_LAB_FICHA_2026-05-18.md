# MEDIOEVO OSIT Formal Lab Ficha - 2026-05-18

## Ruta

`publish_staging\open-dev\medioevo-osit-formal-lab`

## Clasificacion

`OPEN_PUBLIC_SAFE_CANDIDATE`

## Fuente

Prompt operativo del usuario en la sesion 2026-05-18 para crear un laboratorio reproducible de metricas OSIT.

## Decision Curador

- `Adopcion cruda`: `BLOCK`
- `Extraccion selectiva`: `APPROVE_LOCAL_PUBLIC_SAFE`
- `Publicacion GitHub`: `APPROVE_WITH_USER_OVERRIDE`
- `medioevo.space`: `APPROVE_WITH_USER_OVERRIDE`

## Frontera

Incluye:

- paquete Python `osit_lab`;
- metricas `H_eff`, `R`, `Phi_eff`, residuo MTS y gates;
- tests `pytest`;
- notas LaTeX y notebooks placeholder;
- `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md` y `LICENSE.md` con `LEGAL_REVIEW_REQUIRED`.

Excluye:

- libros privados;
- RPG/TCG;
- runtime privado Claudio/Wabi/DUAT/GEODIA;
- prompts internos;
- datasets reales;
- secretos, tokens y credenciales;
- claims fuertes de fisica, conciencia, AGI, prediccion garantizada o seguridad garantizada.

## Evidencia

- `python -m pytest -q` con `PYTHONPATH=src`: `12 passed`.
- `python -m compileall -q src tests`: `exit 0`.
- `python tools\release\scan_secrets.py --path 'publish_staging\open-dev\medioevo-osit-formal-lab' --json --fail-on-findings`: `count_reported=0`.
- `git diff --check` en el repo formal: `exit 0`.

## Riesgo Residual

El host gate externo del 2026-05-18 devolvio `REVIEW` por `disco_precaucion` y `residuo_precaucion`. La publicacion queda justificada solo por autorizacion explicita del usuario en esta sesion y por scans focalizados limpios. No autoriza publicar el workspace completo ni targets nuevos.

