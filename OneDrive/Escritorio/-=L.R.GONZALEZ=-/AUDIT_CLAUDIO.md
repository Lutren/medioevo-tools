# AUDIT_CLAUDIO

Fecha: 2026-05-06
Raiz auditada: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`
Modo: Fase 0 local, no destructiva, sin red.

## Estado

Este workspace ya tenia una auditoria principal en
`docs/control/AUDIT_REPO_TREE.md`. Este archivo es el wrapper operativo exigido
por el prompt maestro para el carril MEDIOEVO / CLAUDIO.

## Evidencia Ejecutada

- `python tools\release\pending_review.py --write --quiet`
  - `active_dedup=0`
  - `claudio_open=0`
  - `qa_artifacts/pending/pending_review_2026-05-06.json`
  - `docs/pending/PENDING_REVIEW_2026-05-06.md`
- `python tools\release\scan_secrets.py --json`
  - `count_reported=200`
  - `truncated_at=200`
  - `default_workspace_scan=True`
- `git status --short -- .`
  - worktree con cambios activos en COMMS, Wabi-Sabi, publishing, tools y otros
    artefactos.

## Que Existe

- Gobierno local: `AGENTS.md`, `README.md`, `SECURITY.md`, `ROADMAP.md`,
  `CONTRIBUTING.md`.
- Auditoria/capas: `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`,
  `RISK_REGISTER.md`, `DUPLICATES_AND_DEAD_CODE.md`,
  `docs/control/AUDIT_REPO_TREE.md`.
- Release local: `docs/release/RELEASE_READINESS_SCORE.md`,
  `docs/release/RELEASE_CHECKLIST.md`.
- Pending snapshot: `docs/pending/PENDING_REVIEW_LATEST.md`.
- Open-dev: `packages/open-dev/*`.
- Comercial: `apps/commercial/*`, `packages/paid/*`.
- Local apps: `apps/local/*`.
- Coordinacion local: `COMMS/*`.
- Privado/frontera: `game-private`, `docs/private/PRIVATE_GAME_BOUNDARY.md`.

## Que Falta En Raiz

Faltaban los wrappers de raiz solicitados por el prompt maestro:

- `AUDIT_CLAUDIO.md`
- `SECRET_SCAN_REPORT.md`
- `IMPLEMENTATION_PLAN.md`
- `TREE_PLAN.md`
- `PRIVATE_BOUNDARY.md`
- `CHANGELOG.md`
- `RELEASE_CHECKLIST.md`
- `SESSION_FINGERPRINT.json`
- `NEXT_SESSION_BRIEF.md`
- `DECISIONS.md`
- `TASKS.md`
- `RISKS.md`
- `ASSUMPTIONS.md`
- `TEST_REPORT.md`

Estos archivos se crean en este ciclo como artefactos nuevos.

## Duplicados Y Dead Code

La fuente vigente es `DUPLICATES_AND_DEAD_CODE.md`. No se movieron ni borraron
duplicados durante este ciclo. Cualquier limpieza debe pasar por ficha,
MIGRATION_MAP y ActionGate.

## Riesgos

- El scan global sigue en `NO APTO PARA PUBLICACION DIRECTA`.
- El workspace contiene rutas privadas, editoriales, comerciales, vendors,
  historicos y releases ya generados.
- Hay worktree sucio por trabajo activo de otros agentes.
- La raiz no debe publicarse ni empaquetarse por glob amplio.

## Capas

| capa | rutas guia | estado |
|---|---|---|
| CLAUDIO CORE | `-=MEDIOEVO=-\-=LIBROS\claudio`, `claudio`, `packages/open-dev/*` | usar por interfaces y allowlists |
| TOOLKIT / PSI-IA | `packages/open-dev`, `research`, `schemas` | publicable solo por paquete verificado |
| CANON / LIBROS | `books`, `-=MEDIOEVO=-\-=LIBROS`, `vault_medioevo` | privado/editorial por defecto |
| COMERCIAL | `apps/commercial`, `packages/paid`, `PRODUCTOS_MEDIOEVO` | propietario, QA/legal requerido |
| PRIVADO | `game-private`, `metaevo-tcg`, `tcg`, `runtime/game_bridge` | no tocar/no publicar |
| LEGACY / ARCHIVE | `_archive`, vendors, caches, builds | excluir de releases |

## Tests Disponibles

- Workspace/release:
  - `python tools\release\pending_review.py --write --quiet`
  - `python tools\release\scan_secrets.py --json`
  - `python tools\release\run_tests.py --execute --json`
- Claudio runtime:
  - `python -m pytest tests/ -x --quiet`
- JS/Electron por producto:
  - `npm run typecheck`
  - `npm run build`

## Producto Minimo Realista

El minimo realista no es publicar el workspace. Es operar por carriles:

1. mantener gobierno y snapshots locales al dia;
2. verificar paquetes allowlist;
3. no tocar privado ni publicar nuevos targets sin ActionGate;
4. cerrar tareas con evidencia en `SESSION_FINGERPRINT.json` y
   `NEXT_SESSION_BRIEF.md`.

## Decision Fase 0

Fase 0 queda ejecutada como documentacion actualizada. No se modifico codigo
existente. La siguiente accion segura es correr tests focalizados en un paquete
allowlist que no tenga cambios activos de otros agentes.
