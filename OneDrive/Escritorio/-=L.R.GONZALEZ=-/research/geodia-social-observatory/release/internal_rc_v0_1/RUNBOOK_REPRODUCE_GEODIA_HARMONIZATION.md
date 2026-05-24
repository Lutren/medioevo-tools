# Runbook: Reproduce GEODIA Harmonization

release_id: GEODIA_INTERNAL_RELEASE_RC_v0.1
publication_gate: BLOCK

## Precondiciones

- Ejecutar desde la raiz del workspace MEDIOEVO / CLAUDIO o una copia local equivalente con la misma estructura relativa.
- No usar red para la armonizacion.
- No usar credenciales.
- Mantener `publication_gate=BLOCK`.

## QA completa

```powershell
python -m pytest
```

## Wrapper QA default offline

```powershell
python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty
```

## Wrapper QA con tres fixtures explicitos

```powershell
python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty --fixtures research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json
```

## Output esperado

- `qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-harmonization-qa-wrapper-report-2026-05-14.json`
- `publication_gate=BLOCK`
- `harmonization_network_used=false`
- Sin ranking, prediccion o causalidad.

## Fallos esperados seguros

Si falta fixture, crosswalk o schema, el wrapper debe fallar de forma segura y no debe publicar nada.
