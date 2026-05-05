# Observacionista Engine + Inverse Contract 2026-05-05

Estado: `REVIEW_VALIDATED_LOCAL_CONTRACT`

Este contrato implementa el metodo solicitado como capa operativa local. No
declara fisica nueva, diagnostico medico ni verdad social externa. Extrae de
PSI/Downloads patrones utiles para el motor:

- `TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md`: `R`, `Phi_eff`, `J_c`, `ActionGate`,
  `WitnessLog` y reduccion de perdida por handoff.
- `tuip_sigma_core.py`: firma observacional, estado PSI, gate determinista y
  log local.
- `sensorium_inversion_lab.py`: perfiles de observador, canales no visuales,
  invariantes entre observadores y reconstruccion inversa de sesgo.
- `observacionismo_v8_1_addons.txt`: falsadores, controles y bloqueo de claims
  fuertes sin validacion.

## Definicion Operativa

Ingenieria observacionista:

1. Recibe una fuente, mensaje, claim o accion candidata.
2. Calcula evidencia local, riesgos, `R`, `J_c` y `Phi_eff`.
3. Pasa por `ActionGate`: `APPROVE`, `REVIEW` o `BLOCK`.
4. Devuelve falsadores y recomendaciones para Claudio/Wabi-Sabi antes de
   cualquier accion autonoma.

Ingenieria observacionista inversa:

1. Toma la misma observacion y la perturba con perfiles de observador:
   `human_visual`, `instrument_balanced`, `dark_observer`, `phase_observer`,
   `low_bandwidth_human`.
2. Mide dependencia visual, cobertura de canales, distancia de firma y
   estabilidad del resultado.
3. Si el resultado cambia demasiado entre observadores, baja el estado a
   `INFERENCIA` o `INCOGNITA`.
4. Si detecta claims medicos, fisicos fuertes, prediccion social real,
   publicacion, accion externa o patrones de secreto, fuerza `BLOQUEADO`.

## Artefactos

- Motor: `COMMS/tools/observacionista_engine.py`
- Esquema: `COMMS/schemas/observacionista-engine-result.schema.json`
- Evidencia: `qa_artifacts/release_validation/seto-observacionista-engine-result-2026-05-05.json`
- Escaneo: `qa_artifacts/release_validation/seto-observacionista-engine-scan-2026-05-05.json`

## Contrato Para Claudio/Wabi-Sabi

Claudio debe consumir el JSON del motor antes de escribir, mover, borrar,
publicar o ejecutar una accion externa. La regla minima es:

- `APPROVE`: accion local, reversible o ya validada, sin secretos ni claims
  bloqueados.
- `REVIEW`: crear ficha, evidence pack, handoff y esperar confirmacion o nueva
  evidencia. No ejecutar escritura autonoma.
- `BLOCK`: detener la accion y registrar falsadores. Claims medicos, fisicos
  fuertes, predicciones sociales reales, publicacion externa y secretos quedan
  aqui por defecto.

El motor puede operar como preflight de `ObservationEnvelope` y como compilador
de handoff. No reemplaza tests, schema validation, secret scan ni review humana
cuando el gate devuelve `REVIEW` o `BLOCK`.

## Falsadores

- El hash de fuente no coincide con la ficha registrada.
- La conclusion cambia de `CERTEZA`/`INFERENCIA` a `INCOGNITA` bajo perfiles de
  observador alternos.
- `Phi_eff` queda en `0.60` o menos despues de comprimir evidencia.
- `validate_seto_comms.py` falla o el tail de WitnessLog no verifica hash-chain.
- Cualquier salida intenta promover teoria PSI como claim fisico, medico o
  social externo.

## Validacion 2026-05-05

- El motor corre localmente sobre `COMMS/inbox/claudio-local-agent.jsonl`.
- El resultado queda en `REVIEW` porque es contrato de autonomia local y debe
  permanecer gated antes de writes.
- El escaneo de secretos sobre artefactos creados/tocados reporta `0`
  hallazgos no permitidos.
- No se copiaron prototipos completos desde Downloads.
- No hubo movimiento, borrado, publicacion ni accion externa.
