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

## Decision

El arbol no se migra fisicamente en este ciclo. La forma limpia se mantiene por
mapas, allowlists, indices y fronteras.
