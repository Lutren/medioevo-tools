# TREE_PLAN

Fecha: 2026-05-06
Estado: plan de arbol, sin movimientos en este ciclo.

## Arbol Actual Gobernado

```txt
/
  AGENTS.md
  README.md
  SECURITY.md
  ROADMAP.md
  CONTRIBUTING.md
  PRODUCT_MAP.md
  VISIBILITY_MATRIX.md
  RISK_REGISTER.md
  DUPLICATES_AND_DEAD_CODE.md
  MIGRATION_MAP.md
  apps/
  books/
  claudio/
  COMMS/
  data/
  docs/
  game-private/
  packages/
  PRODUCTOS_MEDIOEVO/
  qa_artifacts/
  release_manifests/
  releases/
  research/
  runtime/
  schemas/
  tests/
  tools/
  website/
  _archive/
```

## Estructura Objetivo Del Prompt

La estructura objetivo ya existe parcialmente. No debe imponerse con movimientos
masivos. Se mantiene esta regla:

- crear wrappers e indices faltantes;
- mover solo por allowlist;
- registrar todo movimiento en `MIGRATION_MAP.md`;
- no tocar juego/TCG ni privados;
- no borrar directamente.

## Faltantes De Raiz Cubiertos En Este Ciclo

- `CHANGELOG.md`
- `RELEASE_CHECKLIST.md`
- `AUDIT_CLAUDIO.md`
- `SECRET_SCAN_REPORT.md`
- `IMPLEMENTATION_PLAN.md`
- `PRIVATE_BOUNDARY.md`

## Indices Importantes

Indices nuevos o existentes:

- `docs/INDEX.md`
- `apps/INDEX.md`
- `packages/INDEX.md`
- `data/INDEX.md`
- `tools/INDEX.md`

## 2026-05-31 - Consolidaciones ejecutadas

- `apps/local/wabi-sabi/` archivado a `_archive/legacy/wabi-sabi-legacy-2026-05-31/`.
  El runtime canónico de Wabi-Sabi está en `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\wabi_sabi` y `core/wabi*.py`.
- `scripts/wabi_sabi_startup.*` archivados junto con el legacy.
- Wabi consolidation completada: un solo tronco operativo.

## Decision

El arbol no se migra fisicamente en este ciclo. La forma limpia se mantiene por
mapas, allowlists, indices y fronteras.
