# CORE_MODULE_INVENTORY

Fecha: 2026-05-06
Scope: Fase 2, inventario antes de crear codigo nuevo.

## Evidencia Leida

Busquedas locales sobre:

- `packages/open-dev`
- `apps/residueos`
- `tools/release`
- `schemas`

Comandos:

```powershell
rg -n "RMonitor|PhiEff|Phi_eff|RegimeAutomaton|ActionGate|TaskManager|DecisionLog|SessionFingerprint|NextSessionBrief|ArtifactCompiler|CodexTaskPacket|Fingerprint|residue|jamming|regime|APPROVE|REVIEW|BLOCK" packages\open-dev apps\residueos tools\release schemas
```

```powershell
rg -n "class .*Task|TaskManager|tasks|DecisionLog|decision log|NextSessionBrief|brief|ArtifactCompiler|artifact compiler|CodexTaskPacket|task packet|packet" packages\open-dev apps\residueos tools\release schemas
```

## Mapa Del Nucleo

| modulo del prompt | estado | evidencia | decision |
|---|---|---|---|
| RMonitor | equivalente funcional parcial | `packages/open-dev/obsai-core/obsai_core/residue.py` tiene `ResidueTracker`; `metrics.py` estima R desde senales | no duplicar; envolver si hace falta nombre estable |
| PhiEffMeter | equivalente funcional | `obsai_core.metrics.phi_eff_power`; `residueos.metrics.phi_eff`; `obs_safe_integration_kit.core.EstadoPSI` actualiza `Phi_eff` | no crear nuevo sin interfaz comun |
| RegimeAutomaton | equivalente funcional | `obsai_core.metrics.Regime` y `estimate_regime`; `obs_safe_integration_kit.core.EstadoPSI.regime()` | no duplicar |
| ActionGate | existe | `obsai_core.gate.evaluate_action`; `residueos.gate.evaluate_action`; `obs_safe_integration_kit.gates.ActionGate`; schemas con `APPROVE/REVIEW/BLOCK` | usar existente segun carril |
| TaskManager | implementado en este ciclo | `packages/open-dev/obsai-core/obsai_core/tasks.py`; test en `tests/test_task_manager.py` | usar stub testeado |
| DecisionLog | parcial | `ResidueStore` registra decisiones/audit events; docs `DECISIONS.md` existen, pero no hay API comun | crear adaptador simple si se necesita |
| SessionFingerprint | existe | `obsai_core.fingerprint.SessionFingerprint`; storage/fingerprint en obs-safe | usar existente |
| NextSessionBrief | hueco real | existen briefs Markdown, pero no modulo comun de generacion | crear generador minimo si se necesita |
| ArtifactCompiler | hueco real/parcial | `tools/release/product_manifest.py` y packaging scripts compilan manifests/artifacts, pero no hay API pequena con ese nombre | crear wrapper minimo sobre manifests |
| CodexTaskPacket | hueco real | busquedas solo muestran `SignalPacket`; no hay paquete Codex task packet dedicado | crear schema/stub minimo si se necesita |

## Primer Stub Recomendado

`TaskManager` fue el primer candidato porque conecta:

- tareas;
- evidencia;
- estado;
- prioridad;
- cierre;
- `pending_review`.

Forma ejecutada:

1. creado dentro de `packages/open-dev/obsai-core`;
2. no se tocaron `PENDIENTES_MASTER.md`, COMMS activos ni backlog real;
3. usa JSON local;
4. testea add/list/close/bloqueo/persistencia;
5. `python -m pytest tests -q` paso con `29 passed in 1.13s`.

## No Implementar Todavia

- Dashboard.
- API local nueva.
- Frontend.
- Migracion de tareas existentes.
- Publicacion.

## Decision

Fase 2 no debe crear todos los modulos de golpe. El codigo existente ya cubre
R, Phi_eff, regimenes, ActionGate y SessionFingerprint. El primer hueco,
`TaskManager`, queda cubierto con un stub testeado y local.

## Evaluacion 2026-05-06 Bajo Host BLOCK

Host observado: `JAMMING/BLOCK` a `2026-05-06T16:17:51Z`. Con ese gate, la
accion correcta es cerrar evaluacion y no abrir codigo nuevo.

Resultado por wrapper:

- `DecisionLog`: candidato futuro a adaptador delgado sobre `TaskManager`,
  `TaskEvidence` y `DECISIONS.md`, solo cuando haya un consumidor estable.
- `NextSessionBrief`: no crear wrapper ahora; mantener handoff Markdown y
  espejo de continuidad. Un generador minimo requiere host `APPROVE`.
- `ArtifactCompiler`: no crear wrapper ahora; ya existen manifests y scripts
  de release suficientes para el carril local.
- `CodexTaskPacket`: diferir hasta que COMMS o No-LLM necesiten un schema
  consumible. Definirlo antes de tener consumidor agregaria superficie muerta.

Conclusion: la evaluacion queda cerrada como documentacion. No hay nuevo stub
seguro bajo el gate actual.
