# DUAT Official Long-History Data Readiness v0.7

publication_gate: BLOCK
run_id: DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7

## Purpose

v0.7 prepares DUAT for a future benchmark by checking whether official long-history data is ready before any new modeling work. It does not tune weights, add complex models or reinterpret v0.6 as a public claim.

## Criteria

- MIN_OBSERVATIONS_WARN = 24
- MIN_OBSERVATIONS_REVIEW = 30
- PREFERRED_OBSERVATIONS = 40
- MIN_OUTER_FOLDS_TARGET = 5
- MIN_TRAIN_WINDOW_TARGET = 15
- FORECAST_HORIZON_DEFAULT = 1

## Gates

- n_observations < 24: DATA_GATE=BLOCK.
- 24 <= n_observations < 30: DATA_GATE=REVIEW.
- n_observations >= 30: approve for backtest only if license, gaps, comparability and leakage also pass.
- Unknown terms keep LicenseTermsScan=REVIEW.
- Definition or unit changes without crosswalk keep ComparabilityReview=REVIEW.
- Future values in features trigger LeakagePreflight=BLOCK.
- Missing source metadata keeps SourceCardGate=REVIEW.
- Imputation must be documented and keeps ImputationReview=REVIEW.

## CLI

```bash
python -m duat_predictive_registry.cli data-readiness --manifest data_sources/duat_official_long_history_manifest_v0_7.json --schema schemas/duat_data_readiness_report_v0_7.schema.json --pretty --out reports/duat-official-long-history-data-readiness-v0-7.json --markdown-out reports/DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7.md
```

## Boundary

This is data readiness work only. It is not approved for publication, ranking, causal claims, electoral prediction or public forecasting claims.
