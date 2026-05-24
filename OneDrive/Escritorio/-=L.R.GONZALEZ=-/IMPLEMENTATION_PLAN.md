# IMPLEMENTATION_PLAN

Fecha: 2026-05-06
Estado: ejecucion local por fases, sin red, sin publicacion.

## Principio

No abrir features si el estado real no lo justifica. En este ciclo el
`pending_review` reporto cero pendientes abiertos, pero el worktree tiene
cambios activos de otros agentes. Por eso la accion correcta es cierre y
evidencia, no refactor amplio.

## Fase 0 - Auditoria

Estado: ejecutada en este ciclo.

Evidencia:

- `AUDIT_CLAUDIO.md`
- `SECRET_SCAN_REPORT.md`
- `docs/pending/PENDING_REVIEW_2026-05-06.md`
- `qa_artifacts/pending/pending_review_2026-05-06.json`

## Fase 1 - Arbol Limpio

Estado: wrappers creados, sin movimientos.

Acciones:

- Crear `TREE_PLAN.md`.
- Crear `PRIVATE_BOUNDARY.md`.
- Crear indices minimos en carpetas importantes si faltan.
- No mover nada sin `MIGRATION_MAP.md`.

## Fase 2 - Nucleo Funcional

Estado: `TaskManager` implementado y evaluacion de wrappers restantes cerrada
como documentacion bajo host `JAMMING/BLOCK`.

Resultado de la evaluacion 2026-05-06:

1. `DecisionLog`: primer candidato futuro, pero solo como adaptador delgado
   sobre `TaskManager` si aparece un consumidor estable.
2. `NextSessionBrief`: mantener Markdown y espejo; no generar modulo comun con
   host bloqueado.
3. `ArtifactCompiler`: usar manifests/scripts existentes hasta que un target de
   release pida una API pequena.
4. `CodexTaskPacket`: diferir schema hasta que COMMS o No-LLM lo consuman.

Siguiente ruta segura con host `APPROVE`:

1. confirmar consumidor real para `DecisionLog`;
2. crear wrapper minimo;
3. cubrirlo con test focalizado;
4. registrar resultado en `TEST_REPORT.md`.

Modulos objetivo del prompt:

- RMonitor
- PhiEffMeter
- RegimeAutomaton
- ActionGate
- TaskManager
- DecisionLog
- SessionFingerprint
- NextSessionBrief
- ArtifactCompiler
- CodexTaskPacket

Inventario creado en `CORE_MODULE_INVENTORY.md`. No duplicar R, Phi_eff,
regimenes, ActionGate ni SessionFingerprint; ya existen equivalentes
funcionales. `TaskManager` quedo implementado en `obsai-core`.

## Fase 3 - CLI / API Local

Estado: pendiente de inventario focalizado.

No crear frontend pesado antes de confirmar que el nucleo funcional ya esta
testeado.

## Fase 4 - Tests Y Evidencia

Estado de este ciclo: hubo cambio focal de `TaskManager` y luego cierre
documental de wrappers restantes.

Evidencia:

```powershell
cd packages\open-dev\obsai-core
python -m pytest tests -q
```

Resultado base previo: `27 passed in 1.19s`.

Resultado tras `TaskManager`: `29 passed in 1.13s`.

Scan focalizado: `count_reported=0`.

## Fase 5 - Dashboard Local

Estado: no iniciar en este ciclo.

Condicion de entrada: nucleo funcional y CLI/API con tests.

## Fase 6 - Release Prep Local

Estado: preparar, no publicar.

Artefactos:

- `RELEASE_CHECKLIST.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `README.md`
- `docs/release/RELEASE_READINESS_SCORE.md`

## Fase 7 - Autonomia Controlada

Nivel usado en este ciclo: `LEVEL 2`.

Limite: crear artefactos nuevos y ejecutar comandos locales seguros. No se
tocan archivos modificados por otros agentes, no se mueve nada y no se publica.

## Proxima Accion Verificable

Esperar host `APPROVE` antes de abrir mas codigo. Si vuelve a `APPROVE`, tomar
solo el primer workpack con consumidor real: `DecisionLog` minimo sobre
`TaskManager`, test focalizado y registro en `TEST_REPORT.md`.
