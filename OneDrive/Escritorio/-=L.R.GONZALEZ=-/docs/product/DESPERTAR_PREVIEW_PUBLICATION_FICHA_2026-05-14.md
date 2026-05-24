# DESPERTAR_PREVIEW_PUBLICATION_FICHA_2026-05-14

## Ruta

`PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES\despertar-preview-gumroad_20260513_232758`

## Clasificacion

`COMMERCIAL_BOOKS_PUBLIC_SAFE_PREVIEW`

## Decision

Public-safe local package ready for Gumroad/medioevo.space publication when host/ActionGate allows external actions.

## Includes

- Public preview of `MEDIOEVO: Despertar`.
- Reader note.
- Public boundary.
- Gumroad listing JSON.
- SHA256 manifest and ZIP QA.

## Excludes

- Full 35-book archive.
- RPG/TCG.
- Claudio runtime, credentials, sessions or private automation state.
- External scientific claims.
- Real bestseller claim.

## Evidence

- Secret scan package/artifact: `count_reported=0`.
- ZIP QA: `testzip=None`, executables `0`, nested_zips `0`.
- Anti-AI text review: `PASS`.
- Live deploy/Gumroad API: blocked while host gate is `JAMMING/BLOCK`.

## Next Gate

Run host gate again. If not BLOCK, run target-specific ActionGate and Gumroad/Cloudflare publication flow.
