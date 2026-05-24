# Formal / Wabi Contract Comparison - 2026-05-13

Estado: `CONTRATOS_TESTEADOS_SIN_IMPORT`

## Alcance

Fuentes Formal comparadas solo por contrato:

- `medioevo_agent_core.py`
- `medioevo_core_v01.py`
- `Completar04.txt`
- `Completar07.txt`
- `PR11.txt`

Targets Wabi/Sabi revisados:

- `apps/local/wabi-sabi/wabi_sabi/core/gate.py`
- `apps/local/wabi-sabi/wabi_sabi/core/safe_executor.py`
- `apps/local/wabi-sabi/wabi_sabi/core/rollback_store.py`
- `apps/local/wabi-sabi/wabi_sabi/core/decision_log.py`
- `apps/local/wabi-sabi/wabi_sabi/core/eml.py`
- `apps/local/wabi-sabi/wabi_sabi/core/geodia_math_core.py`

Target Claudio revisado para Phi_eff:

- `-=MEDIOEVO=-\-=LIBROS\claudio\core\session_cosmos.py`

No se ejecuto, importo ni copio codigo de Formal.

## Resultado Por Contrato

| Contrato candidato | Evidencia Formal | Estado en Wabi/Claudio | Decision |
|---|---|---|---|
| `GateDecision` / `ActionGate` | `medioevo_agent_core.py`, `medioevo_core_v01.py`, `PR11.txt` | `gate.py` ya expone `GateDecision(gate, reasons)` y bloqueo de destruccion, publicacion y secretos | `NO_IMPORT`; preservar Wabi como fuente activa |
| `AgentOutput` / envelope | `medioevo_agent_core.py` | `observation.py` ya crea `ObservationEnvelope` con `certainty/inference/unknown/artifacts/evidence/fingerprint` | `TEST_CONTRACT`; no crear nuevo modelo paralelo |
| GhostGate / simulacion previa | `medioevo_agent_core.py`, `Completar04.txt`, `Completar07.txt` | `patch_planner.py`, `safe_executor.py` y `rollback_store.py` ya cubren plan, diff, rollback y witness | `NO_IMPORT`; usar como requisito negativo |
| Handoff / fingerprint | `medioevo_agent_core.py`, `medioevo_core_v01.py`, `PR11.txt` | `decision_log.py`, `ObservationEnvelope` y `WitnessLog` ya dejan estado persistente | `NO_DUPLICATE`; documentar como convergencia |
| R / Phi_eff | `medioevo_agent_core.py`, `medioevo_core_v01.py` | `session_cosmos.py` usa Phi_eff lineal operativo; `geodia_math_core.py` usa Phi_eff sintetico exponencial; `eml.py` queda `RESEARCH_ONLY` | `RESEARCH_ONLY`; no sustituir runtime |

## Phi_eff Boundary

Hay tres formulas con usos distintos:

- Claudio `session_cosmos`: `Phi_eff = 1 - R / J_c` y en estado compacto
  `Phi_eff = 1 - max(R_universal, dark_energy, average_epsilon)`. Es contrato
  operativo de sesion.
- Wabi `geodia_math_core.compute_phi_eff`: colapso sintetico exponencial como
  helper OSIT/GEODIA.
- Wabi `eml.py`: helper instrumental `RESEARCH_ONLY`, con guards de dominio.

Decision: cualquier `compute_phi_eff` de Formal se conserva como investigacion
hasta que una prueba demuestre equivalencia de dominio y utilidad. No debe
reemplazar `session_cosmos` ni `geodia_math_core`.

## Pruebas Nuevas

Se agregaron pruebas locales en Wabi/Sabi:

- `apps/local/wabi-sabi/tests/test_formal_contract_intake.py`
- `apps/local/wabi-sabi/tests/test_observacionista_evaluation_fixture.py`

Cobertura:

- `GateDecision` conserva forma minima y razones.
- `ActionGate` bloquea secretos/publicacion/destruccion.
- `SafeExecutor` rechaza planes no `APPROVE` antes de escribir.
- `ObservationEnvelope` cubre el shape de salida formal sin importar Formal.
- Phi_eff/EML quedan acotados y `RESEARCH_ONLY`.
- Fixture observacionista compara tres rutas sin red real: local mock,
  `codex/dry-run` con `WABI_DISABLE_BASE_MODEL=1`, y cloud mock.

## Decision

Los archivos Formal tienen valor como especificacion de contraste, pero no como
runtime importable. El cierre correcto es contrato/test/documento, no fusion de
codigo.

