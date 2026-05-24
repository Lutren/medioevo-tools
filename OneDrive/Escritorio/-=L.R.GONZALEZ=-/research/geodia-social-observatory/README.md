# GEODIA Social Observatory

Estado: MVP local privado / research-only.

GEODIA Social Observatory simula epocas y cambios sociales desde snapshots
trazables. No predice resultados garantizados y no autoriza publicacion externa.
El flujo v1 es:

1. fuente allowlist -> snapshot con hash, fecha, licencia y rol;
2. normalizacion de indicadores/eventos;
3. modelo de epoca con DUAT, especialistas Conway y gate de Observacionismo;
4. reporte con evidencia por claim, incertidumbres y backtest offline.

## Contratos

- `claudio.social_source_snapshot.v1`
- `claudio.social_epoch_model.v1`
- `claudio.social_scenario_report.v1`
- `motor.duat_v2_intake.v1`

## Fuentes allowlist v1

- World Bank Indicators API
- IMF Data APIs
- OECD API
- Eurostat SDMX API
- FRED API
- Our World in Data Grapher API
- GDELT DOC 2.0
- Awesomedata Awesome Public Datasets

Notas de seguridad:

- GDELT solo cuenta como senal mediatico-narrativa, no como hecho social bruto.
- FRED requiere API key y aviso de no-endoso antes de uso live.
- OWID requiere revisar la licencia del proveedor original por dataset.
- Awesomedata cuenta solo como indice de descubrimiento: cada dataset enlazado
  requiere licencia, hash, procedencia y frontera de claims propia.
- El MVP no hace fetch de red: `--offline` es obligatorio.

## Uso local

```powershell
cd research\geodia-social-observatory
python -m geodia_social_observatory.cli intake --pretty
python -m geodia_social_observatory.cli signature --text "Observo evidencia porque quizas conviene pedir otra prueba?" --pretty
python -m geodia_social_observatory.cli route --features-json "{\"uncertainty\":0.7,\"impact\":0.8}" --pretty
python -m geodia_social_observatory.cli simulate-duat --seed 7 --size 12 --steps 5 --pretty
python -m geodia_social_observatory.cli duat-v2-intake --pretty
python -m geodia_social_observatory.cli run --offline --fixture fixtures\social_epoch_fixture.json --pretty
python -m geodia_social_observatory.cli backtest --offline --fixture fixtures\social_epoch_fixture.json --pretty
python -m pytest tests -q
```

## Separacion funcional/laboratorio

- Funcional: intake con SHA256, event store JSONL, artifact graph, router
  `cache/small/strong/sim/human`, firma conductual como riesgo continuo,
  salud DUAT y simulacion DUAT/Conway deterministica.
- Laboratorio: Gemma 4, LoRA/QLoRA, MoE surgery, ADEPT/CLaSp/MoR/SWIFT/MTP,
  world models entrenados, despliegues GPU/cloud y claims cientificos.
- Bloqueo: ningun archivo bruto de `Downloads` se copia al motor; solo se
  destilan contratos, tests y reglas con hashes de origen.

## Intake DUAT v2 2026-05-01

Los archivos `deep-research-report (4).md`, `Esto es material
extraordinariament.txt`, `duat_v2.html` y `deep-research-report (5).md` quedan
registrados como material local privado con SHA256. Lo funcional que entra ahora
es: frontera entre verdad
ultima y adecuacion operacional, separacion fenomeno/observacion/accion, grafo
de artefactos con `supports`, `contradicts` y `verified_by`, vocabulario de
fases DUAT, forma de simulacion offline seeded, roadmap DUAT de tres carriles,
maquina de eventos y frontera de identidad conductual continua.

Queda en laboratorio privado: dashboard DUAT v2, puente EEG, memoria
conformacional, visualizaciones fractales, Mesa/PettingZoo, FAISS/Qdrant y rutas
Gemma/vLLM/Ray/LoRA/world model. Queda bloqueado: prediccion social garantizada,
validacion neurocientifica, publicacion externa, copia de fuentes brutas,
ontologia como prerequisito del MVP y cirugia interna del modelo.

Bloqueos resueltos localmente: mezcla de capas, ingestion bruta de Downloads,
confusion de claims y falta de contratos nucleares. Bloqueos que siguen por
gate: modelos pesados y publicacion externa.

## Claim boundary

Los indicadores del fixture son sinteticos y solo existen para validar el
contrato, hashing, rechazo de fuentes no allowlist y backtest reproducible. Un
uso con datos reales requiere revisar licencia, fecha de captura, hash del
payload y claims bajos por cada fuente.

## Fixtures oficiales locales 2026-05-14

- `fixtures/world_bank_mexico_2018_2023_fixture.json`: World Bank Mexico,
  2018-2023; reporte local con `publication_gate=BLOCK`.
- `fixtures/eurostat_social_epoch_2018_2023_fixture.json`: Eurostat Germany,
  2018-2023; SHA256
  `FEF2CE8E3B523A48C0675646705033465BBCE788EAC8B532C18E0C3461098AD7`;
  reporte local con `publication_gate=BLOCK`.
- `fixtures/inegi_mexico_social_2018_2023_fixture.json`: INEGI ENOE Mexico,
  2018-2023, derivado de descarga oficial XLSX sin credenciales; SHA256 bruto
  `0add6e88da29b8f5eddcafe889f94c353edaab8a9d5ec272565a55c84cae8bd5`;
  reporte local con `publication_gate=BLOCK`.

La comparacion multi-source en
`qa_artifacts/release_validation/geodia-multisource-comparison-2026-05-14.json`
es QA metodologico y mantiene conclusiones sustantivas en `INFERENCIA`.

## Harmonization Layer v0.1

La capa de armonizacion v0.1 vive en:

- `schemas/geodia_indicator_harmonization_v0_1.schema.json`
- `docs/GEODIA_INDICATOR_HARMONIZATION_v0_1.md`
- `fixtures/geodia_indicator_crosswalk_v0_1.json`
- `geodia_social_observatory/harmonization.py`
- `tests/test_harmonization.py`

Reglas de cierre:

- No hay `EXACT` para los indicadores actuales.
- Desempleo y esperanza de vida quedan como `STRONG_PROXY`.
- Economia queda en `REVIEW`.
- Cruces de dominios distintos son `NOT_COMPARABLE`.
- No hay ranking Mexico vs Alemania.
- `publication_gate=BLOCK` en todo artefacto.

Reporte:
`qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json`.

## Regenerar armonizacion offline

Comando reproducible desde esta carpeta:

```powershell
python -m geodia_social_observatory.cli harmonize --offline --fixtures fixtures/world_bank_mexico_2018_2023_fixture.json fixtures/eurostat_social_epoch_2018_2023_fixture.json --crosswalk fixtures/geodia_indicator_crosswalk_v0_1.json --schema schemas/geodia_indicator_harmonization_v0_1.schema.json --pretty --out ../../qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json
```

Comando explicito con tres fixtures oficiales:

```powershell
python -m geodia_social_observatory.cli harmonize --offline --fixtures fixtures/world_bank_mexico_2018_2023_fixture.json fixtures/eurostat_social_epoch_2018_2023_fixture.json fixtures/inegi_mexico_social_2018_2023_fixture.json --crosswalk fixtures/geodia_indicator_crosswalk_v0_1.json --schema schemas/geodia_indicator_harmonization_v0_1.schema.json --pretty --out ../../qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json
```

Inputs requeridos:

- fixtures offline explicitos;
- crosswalk explicito;
- schema explicito;
- output explicito.

Output esperado:

- `schema=claudio.geodia_harmonization_report.v0_1`;
- `offline_mode=true`;
- `network_used=false`;
- `publication_gate=BLOCK`;
- desempleo y esperanza de vida como `STRONG_PROXY`;
- economia como `REVIEW`;
- cruces invalidos como `NOT_COMPARABLE`.

Limites epistemologicos:

- no publicar;
- no usar red, credenciales ni FRED;
- no ordenar paises;
- no inferir causalidad;
- no hacer predicciones sociales, electorales o personales;
- no convertir `STRONG_PROXY` en `EXACT`;
- no convertir `REVIEW` en conclusion.

## QA wrapper offline

Comando reproducible desde la raiz del workspace:

```powershell
python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty
```

Comando equivalente desde esta carpeta:

```powershell
python scripts/run_harmonization_qa.py --offline --pretty
```

El wrapper ejecuta en local:

- `harmonize --offline` con fixtures, crosswalk, schema y output explicitos;
- validacion JSON del reporte generado;
- scans focales de rutas privadas, clasificaciones, forma del reporte,
  acciones externas bloqueadas y valores sensibles;
- verificacion de `pending_review`;
- reporte final en
  `qa_artifacts/release_validation/geodia-harmonization-qa-wrapper-report-2026-05-14.json`.

Contrato de salida:

- `offline_mode=true`;
- `network_used=false`;
- `publication_gate=BLOCK`;
- `action_gate=APPROVE_LOCAL_ONLY` solo si los checks locales pasan;
- sin publicacion, push, deploy, Gumroad, DNS, FRED, credenciales, ordenamiento
  de paises, causalidad ni prediccion.

## Tercer fixture oficial INEGI

Estado 2026-05-14: `APPROVE_LOCAL_WITH_OFFICIAL_SOURCE`.

Fuente: INEGI / Mexico official social indicators.

Resultado:

- fuente oficial identificada en INEGI Descarga Masiva;
- archivo bruto descargado desde dominio oficial sin credenciales;
- source card, manifest y fixture offline creados;
- crosswalk actualizado solo para desempleo como `STRONG_PROXY`;
- armonizacion con World Bank + Eurostat + INEGI pasa offline;
- no se inventaron datos oficiales.

Artefactos:

- `fixtures/source_intake/inegi/INEGI_SOURCE_CARD.md`
- `fixtures/source_intake/inegi/INEGI_ENOE_SOURCE_MANIFEST_2026-05-14.json`
- `fixtures/source_intake/inegi/raw/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx`
- `fixtures/inegi_mexico_social_2018_2023_fixture.json`
- `qa_artifacts/release_validation/geodia-inegi-source-intake-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-three-fixture-harmonization-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-third-fixture-final-qa-report-2026-05-14.json`

Scaffold historico:
`fixtures/README_THIRD_OFFICIAL_FIXTURE_REVIEW.md`.

La licencia/terminos queda `REVIEW_TERMS_DOCUMENTED`; no autoriza publicacion o
redistribucion publica/comercial. `publication_gate=BLOCK`.


## Internal RC v0.1 status

- Three-fixture harmonization is available locally with World Bank, Eurostat and INEGI ENOE fixtures.
- Offline QA is available through `python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty` and the three-fixture explicit command in `release/internal_rc_v0_1/RUNBOOK_REPRODUCE_GEODIA_HARMONIZATION.md`.
- Publication remains blocked pending human/legal review: `publication_gate=BLOCK`.
- GEODIA does not make prediction, ranking or causality claims.
- Internal RC docs are in `release/internal_rc_v0_1/`; no public-safe package has been created.


## Public-Safe Candidate v0.1 status

- Local public-safe candidate package exists at `release/public_safe_candidate_v0_1/`.
- Local zip exists at `qa_artifacts/release_validation/geodia-public-safe-candidate-v0-1.zip` with SHA256 `719ca8a7ef4c7439fe8859b5894483afa062c2b88883303fd5e0628fa9de0e43`.
- The candidate excludes raw XLSX and real fixture JSON data; it includes a synthetic fixture schema example only.
- `publication_gate=BLOCK`, `external_publication=false`, `public_safe_package_created=true`.
- Legal/human review remains required before distribution.

## DUAT Smallville Simulation Lab v0.1

Local synthetic Smallville-style simulation is available through:

```powershell
python -m geodia_social_observatory.cli smallville-duat --seed duat-smallville-v0-1 --days 2 --ticks-per-day 6 --pretty --out ../../qa_artifacts/release_validation/duat-smallville-sim-lab-v0-1-ledger.json
python -m geodia_social_observatory.cli smallville-falsify --ledger ../../qa_artifacts/release_validation/duat-smallville-sim-lab-v0-1-ledger.json --pretty --out ../../qa_artifacts/release_validation/duat-smallville-sim-lab-v0-1-falsifier.json
python -m geodia_social_observatory.cli remote-compute-plan --pretty --out ../../qa_artifacts/release_validation/duat-remote-compute-plan-v0-1.json
python -m geodia_social_observatory.cli remote-notebook-template --pretty --out ../../qa_artifacts/release_validation/duat-smallville-colab-kaggle-template-v0-1.ipynb
```

The lab has 25 synthetic agents, deterministic replay, hash-chain ledger,
climate/social/geological/pressure/orbital parameters and remote compute gates
for local CPU, Colab, Kaggle and SimScale. External runtimes remain `REVIEW`;
`publication_gate=BLOCK`; bias is reported as `AUDITABLE_NOT_ABSENT`, not
absent.

Detailed runbook:
`docs/DUAT_SMALLVILLE_REMOTE_COMPUTE_v0_1.md`.
