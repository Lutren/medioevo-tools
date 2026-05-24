# SMALLVILLE-DUAT LOCAL EVIDENCE CLOSEOUT 2026-05-22

## Estado

Smallville-DUAT local reproducible queda cerrado como evidencia local sintetica.
No se abrio compute remoto, red, datos reales, sensores, publicacion ni deploy.

## Evidencia

- Focal Smallville:
  `python -B -m pytest tests/test_smallville_duat_lab.py tests/test_smallville_duat_v02.py -q -p no:cacheprovider`
  -> `21 passed in 3.02s`.
- GEODIA full:
  `python -B -m pytest tests -q -p no:cacheprovider`
  -> `74 passed in 51.53s`.
- Artefactos nuevos:
  `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522`.
- Manifest v0.2:
  `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522/manifest.json`.
- Metricas v0.2:
  `schema=duat.smallville.metrics.v0_2`, `seed=20260522`, `agents=25`,
  `hash_chain_valid=true`, `falsifiers_passed=true`,
  `publication_gate=BLOCK`, `failed=[]`.
- Falsificador v0.1:
  `schema=duat.smallville.falsifier_report.v0_1`, `passed=true`,
  `checks=7`.

## ActionGate

- Local synthetic execution: APPROVE.
- Remote compute Colab/Kaggle/SimScale: REVIEW.
- Real data, sensors, publication, deploy, push: BLOCK/REVIEW segun target.

## Decision

El pendiente "Crear simulacion Smallville-DUAT local con SignalSourcePack,
replay, intervencion, metricas y falsadores" se cierra por implementacion y
evidencia ya existente, revalidada en este ciclo con artefactos frescos.

## Siguiente accion

Repetir OSIT-HYBRID con multi-seed, `R_mu` comparable y Source Cards para los
seis scenarios, manteniendo `PublicationGate=BLOCK`.
