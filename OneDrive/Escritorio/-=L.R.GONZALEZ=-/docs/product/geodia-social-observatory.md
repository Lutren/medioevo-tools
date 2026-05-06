# GEODIA Social Observatory

Estado: `PRIVATE_INTERNAL_RESEARCH / LOCAL_PRIVATE_MVP / NO_PUBLIC_ENGINEERING`.

GEODIA Social Observatory es un simulador local privado de epocas/cambios
sociales con DUAT, especialistas Conway y Observacionismo como gate epistemico.
No es una herramienta de prediccion garantizada y no autoriza publicacion
externa de ingenieria, codigo, fixtures internos ni bridges.

El carril publico relacionado es DUAT Genesis:
`packages\open-dev\duat-genesis`, un sandbox sintetico separado.

## Contratos v1

- `claudio.social_source_snapshot.v1`
- `claudio.social_epoch_model.v1`
- `claudio.social_scenario_report.v1`

## Flujo

```txt
fuente allowlist
  -> snapshot con hash, licencia, fecha y rol
  -> normalizacion de indicadores/eventos
  -> modelo de epoca DUAT + Conway
  -> reporte con CERTEZA / INFERENCIA / INCOGNITA
  -> gate de publicacion BLOCK hasta legal + backtests + ActionGate
```

## Fuente de verdad local

`research/geodia-social-observatory`

Comandos:

```powershell
python -m pytest tests -q
python -m geodia_social_observatory.cli intake --pretty
python -m geodia_social_observatory.cli signature --text "Observo evidencia porque quizas conviene pedir otra prueba?" --pretty
python -m geodia_social_observatory.cli route --features-json "{\"uncertainty\":0.7,\"impact\":0.8}" --pretty
python -m geodia_social_observatory.cli simulate-duat --seed 7 --size 12 --steps 5 --pretty
python -m geodia_social_observatory.cli run --offline --fixture fixtures\social_epoch_fixture.json --pretty
python tools\release\scan_secrets.py --product geodia-social-observatory --json --fail-on-findings
python tools\release\product_manifest.py --product geodia-social-observatory --hash --write
```

## Intake DUAT / GEODIA 2026-05-02

Nuevas fuentes revisadas:

- `duat_geodia_v0_2.zip`: motor DUAT Geodia, API, UI, falsadores y data-source registry.
- `duat_for_integration_v0_1.zip`: FOR kernel, bridges Genesis/GEODIA y local AI.
- `duat_omnis_v1.py`: simulador social sintetico standalone.
- textos largos de EML, MCR, ciudad.matrix, procesamiento de datos, MCP y fisica especulativa.

Evidencia local:

- `duat_geodia_v0_2`: `python -m pytest tests -q` en temporal -> `1 passed`.
- `duat_for_integration_v0_1`: `python -m pytest tests -q` en temporal -> `3 passed`.

Decision: estos paquetes son material ejecutable de laboratorio, no fuente
publicable directa. El observatorio puede absorber ideas por hand-port selectivo:
falsadores, fixtures sinteticos, source registry, EML seguro y reportes de
residuo. No copiar `.pyc`, `__pycache__`, rutas locales ni claims fuertes.

## Separacion funcional/laboratorio

Funcional ahora:

- intake local de `Downloads` con SHA256 sin copiar archivos brutos;
- event store JSONL, artifact graph y replay;
- firma conductual como riesgo continuo, no identidad absoluta;
- router `cache/small/strong/sim/human`;
- salud DUAT y simulacion DUAT/Conway deterministicos.

Laboratorio:

- Gemma 4, LoRA/QLoRA, vLLM, world models entrenados y cirugia MoE;
- ADEPT/CLaSp/MoR/SWIFT/MTP;
- claims cientificos, papers y predicciones sociales.
- DUAT Geodia v0.2, DUAT + FOR v0.1, DUAT-OMNIS y MCP DUAT hasta que pasen
  hand-port, tests, claims scan y ActionGate.

## Reglas de fuente

- GDELT DOC 2.0 solo se usa como senal mediatico-narrativa.
- FRED requiere API key y aviso de no-endoso; no guardar keys en fixtures ni manifests.
- OWID requiere revisar la licencia del proveedor original por dataset.
- El MVP v1 solo acepta `--offline`; no hay fetch de red.

## Criterio de salida futuro

El producto no sale de `PRIVATE_INTERNAL_RESEARCH` como ingenieria abierta. Si
se necesita material publico, se extrae un patron sintetico hacia DUAT Genesis o
un whitepaper low-claim, con snapshots licenciados si aplica, backtests
historicos con holdout, secret scan del artefacto limpio, claims bajos, legal
review y aprobacion humana por ActionGate.
