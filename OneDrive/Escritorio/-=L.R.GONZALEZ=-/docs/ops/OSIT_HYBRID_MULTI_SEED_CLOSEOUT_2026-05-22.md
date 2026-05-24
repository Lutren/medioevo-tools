# OSIT-HYBRID MULTI-SEED CLOSEOUT 2026-05-22

## Estado

OSIT-HYBRID multi-seed queda cerrado como harness sintetico local. No se
recupero el simulador fuente original; por tanto, esta evidencia no debe
presentarse como repeticion historica exacta ni validacion externa.

## Evidencia

- Harness creado:
  `-= BRAIN_OS =-/-=LR WORKING BENCH=-/Descubrimientos/osit_hybrid_multiseed.py`.
- Tests creados:
  `-= BRAIN_OS =-/-=LR WORKING BENCH=-/Descubrimientos/test_osit_hybrid_multiseed.py`.
- Focal:
  `python -B -m pytest test_osit_hybrid_multiseed.py -q -p no:cacheprovider`
  -> `3 passed in 30.48s`.
- Full Workbench Descubrimientos:
  `python -B -m pytest -q -p no:cacheprovider`
  -> `37 passed in 26.75s`.
- py_compile:
  `python -B -m py_compile osit_hybrid_multiseed.py test_osit_hybrid_multiseed.py`
  -> PASS.
- Paquete:
  `qa_artifacts/osit_hybrid/OSIT_HYBRID_MULTI_SEED_20260522`.

## Resultado

- `seed_count=100`.
- `audit_seed=20260522`.
- `winner_by_mean_score=GS raw` en el harness sintetico local.
- `R_mu_comparable` existe para escenarios raw y OSIT.
- Source Cards: `4800` tarjetas, seis escenarios cubiertos,
  `publication_gate=BLOCK`.
- Manifest:
  `qa_artifacts/osit_hybrid/OSIT_HYBRID_MULTI_SEED_20260522/manifest.json`.

## ActionGate

- Harness sintetico local: APPROVE.
- Claims externos, NRMP real, datos historicos, publicacion o compute remoto:
  BLOCK/REVIEW.

## Decision

El pendiente "Repetir OSIT-HYBRID con multi-seed, R_mu comparable y Source
Cards para los seis escenarios" queda cerrado en alcance local sintetico. El
resultado cambia la conclusion operativa: no afirmar que `GS OSIT` gana
universalmente; bajo este harness comparable gana `GS raw` por media de Score,
mientras `GS OSIT` queda cerca y con menor `R_mu`.
