# OSIT Epistemic Engine API - 2026-05-22

## Estado

API local minima implementada en `obsai-core` sin dependencias nuevas.

## Superficie

- Module: `obsai_core.epistemic_engine.OSITEpistemicEngine`
- CLI: `python -m obsai_core.cli classify-text --text "..."`
- Local server: `python -m obsai_core.cli serve-epistemic-engine --host 127.0.0.1 --port 8789`
- Endpoints:
  - `GET /health`
  - `POST /classify`

## Contrato

`POST /classify` acepta:

```json
{
  "text": "claim or paragraph",
  "task": "optional task name"
}
```

Devuelve:

- `ObservationEnvelope v2.1`
- `claimResult.gate_contract`
- `SourceCard`
- `R_or`, `phi_moi`, `gate`, `next_action`

## Frontera

- `publication_gate=BLOCK`
- `calibration=DEMO_ONLY`
- `cloud_provider_called=false`
- `applied_to_sources=false`
- No Flask, no red externa, no persistencia obligatoria.

## Evidencia

- `python -B -m pytest tests/test_epistemic_engine.py tests/test_claim_gate_contract.py tests/test_observation_envelope_schema.py tests/test_claim_classifier.py -q -p no:cacheprovider`
  -> `42 passed in 1.50s`.
- `python -B -m py_compile obsai_core/epistemic_engine.py obsai_core/cli.py tests/test_epistemic_engine.py`
  -> PASS.
- `python -B -m pytest tests -q -p no:cacheprovider`
  -> `71 passed in 3.78s`.
- CLI smoke `classify-text` -> `gate=APPROVE`, `publication_gate=BLOCK`.
- HTTP smoke efimero -> `/health` 200, `/classify` strong claim `gate=BLOCK`.
