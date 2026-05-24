# ObservationEnvelope v2.1 JSON Schema - 2026-05-21

## Gate Contract Update

- `claimResult.gate_contract` is now part of the schema surface.
- The contract unifies `TruthGate`, `C-GATE`, `PhysicsHonestyGate` and
  `ScienceClaimGate` in one `obsai.claim_gate_contract.v1` payload.
- Calibration remains `DEMO_ONLY`; this is an engineering control contract, not
  a public science claim.

## Estado

JSON Schema canonico creado para el output `ObservationEnvelope v2.1` emitido
por `obsai_core.claim_classifier.ClaimClassifier`.

## Artefacto

- `obsai_core/schemas/observation_envelope_v2_1.schema.json`

## Evidencia

- `python -B -m pytest tests/test_observation_envelope_schema.py tests/test_claim_classifier.py -q -p no:cacheprovider`
  -> `33 passed in 0.20s`.
- `python -B -m py_compile obsai_core\claim_classifier.py tests\test_observation_envelope_schema.py`
  -> PASS.

## Frontera

- Schema y tests son locales.
- No se publico paquete externo.
- Calibration permanece `DEMO_ONLY`.
