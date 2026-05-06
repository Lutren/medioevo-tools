# OBS EOR / AIA / Topologia - Revision 2026-05-01

Status: `KEEP_GATED / INTERNAL_RESEARCH`

Fuente cruda: `C:\Users\L-Tyr\Downloads\Sí, Luis René. Radicalmente. Has pu.txt`

SHA256: `283EFD73F932BB9574253693E03B271FF9A78306331B37DBF59882DD9A303018`

## Decision

Se integra como material de investigacion para `research\obs-info-kernel`, no
como canon publico ni producto. La parte aceptada es operacional:

- `R_info = H(M|X_i)/H(M)` cuando existe una distribucion definida.
- `R_operativo` como proxy de fallos, redundancia, contradicciones, pendientes y acciones bloqueadas.
- Guardas epistémicas `[A]/[D]/[C]/[H]/[M]/[X]`.
- Test de equivalencia operacional de cinco filtros.
- Informacion oscura con estados `dark_candidate`, `dark_testable`, `dark_validated`, `dark_rejected`.
- AIA no-antropocentrica como procedimiento: grafos, ausencias, invariantes, pruebas negativas y reduccion medible de incertidumbre.
- AIA v5 se reencuadra como `Atlas de Operadores Perdidos / Operator Discovery Engine`: detectar operadores, omisiones, calibraciones y falsadores entre dominios.

## Correcciones Obligatorias

No se acepta como claim fuerte:

- `R es entropia`.
- `La entropia ahora tiene dueño`.
- `Controlar R es controlar la realidad observable`.
- `La mecanica cuantica es jamming`.
- `La conciencia queda probada por topologia`.

Version segura:

> `R_info` puede modelarse como entropia condicional normalizada cuando el
> fenomeno, la representacion y la distribucion estan definidos. En agentes,
> `R_operativo` es un proxy de runtime. `R_fisico` queda como hipotesis de
> investigacion, no validacion.

## Integracion Realizada

Entraron al kernel interno sin dependencias externas:

- `obs_info_kernel/eor.py`
- `obs_info_kernel/epistemic_guard.py`
- `obs_info_kernel/equivalence.py`
- `obs_info_kernel/operator_profile.py` crea `K_source` por fuente.
- `obs_info_kernel/hypothesis.py` calcula prioridad de hipotesis con `delta_R`, transferencia, testabilidad, orfandad y riesgo de sobreclaim.
- `anti_information.py` usa compuerta de `coverage` para evitar falsos positivos cuando dos fuentes apenas comparten nucleo.
- `dark_information.py` ahora marca `dark_candidate`, `dark_testable`, `dark_validated` o `dark_rejected` y expone `testability`.
- `tests/test_eor_guard.py`

La topologia consciente, el compresor termodinamico con grafos y el cartografo
`C_ij` quedan como experimento opcional porque dependen de `NetworkX` y de un
`GrafoEpistemicoHibrido` todavia no canonizado en este paquete.

## Pendientes

- Validar EOR con corpus real y distribuciones trazables.
- Completar un `OperatorGraph` mas rico si el perfil `K_source` demuestra utilidad en corpus real.
- Implementar topologia `C_ij` solo como extra opcional, con pruebas y README de claims.
- No publicar este paquete ni convertirlo en copy de venta hasta resolver licencia, fuentes primarias y frontera de claims.
