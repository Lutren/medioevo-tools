# DUAT ForecastGate v0.1

publication_gate: BLOCK

## Regla

```text
if no_source_card:
    REVIEW
elif no_backtest:
    REVIEW
elif data_leakage_detected:
    BLOCK
elif unsupported_causality_claim:
    BLOCK
elif forbidden_domain_claim:
    BLOCK
elif brier_score > baseline_brier:
    BLOCK_PRODUCTION
elif R_pred >= 0.60:
    BLOCK
elif R_pred >= 0.35:
    REVIEW
else:
    APPROVE
```

ForecastGate no autoriza publicacion. Solo decide si una senal o modelo puede
pasar a laboratorio, revision o bloqueo.

En `DUAT_PREDICTIVE_BENCHMARK_MATRIX_v0_3`, `LicenseTermsScan=REVIEW` mantiene
`ForecastGate=REVIEW` y `publication_gate=BLOCK` aunque R_delta sea negativo.

## DomainCalibrationGate v0.4

`ForecastGate` no interpreta por si solo si una reduccion de R es una mejora de
precision. `DomainCalibrationGate` agrega esa separacion:

- si `R_delta < 0` y MAE/RMSE mejoran, el benchmark mejora operacionalmente y
  metricamente;
- si `R_delta < 0` pero MAE/RMSE empeoran, solo hay reduccion operacional de R;
- si las metricas discrepan, el resultado queda como calibracion mixta.

Mientras `LicenseTermsScan=REVIEW`, el gate final permanece `REVIEW` y
`publication_gate=BLOCK`.

## MetricAlignedR v0.5

`MetricAlignedR` agrega una barrera posterior a `DomainCalibrationGate`:

- conserva `R_operational_before`, `R_operational_after` y
  `R_operational_delta`;
- calcula `metric_degradation_score` y `metric_penalty`;
- produce `R_after_aligned` y `R_delta_aligned`;
- aplica piso si MAE y RMSE empeoran;
- pasa por `PredictiveClaimGate`.

Regla activa: R reduction does not equal predictive validation. Si MAE y RMSE
empeoran, el resultado puede documentar reduccion operacional de R, pero no
autoriza claim predictivo. En este carril `publication_gate` permanece `BLOCK`.

## NestedBacktest v0.6

`DUAT_NESTED_DOMAIN_BACKTEST_v0_6` agrega una prueba walk-forward anidada:

- outer fold: evaluacion fuera de muestra;
- inner fold: seleccion de ventana/peso usando solo pasado;
- `BacktestLeakageGuard`: verifica que el test externo no entre al train,
  validacion interna ni seleccion de configuracion;
- `OutOfSampleGate`: clasifica metricas OOS antes de cualquier claim.

Si el nested backtest empeora MAE/RMSE, el resultado queda en `REVIEW` aunque
capas anteriores hayan reducido R operacional. `publication_gate=BLOCK`.

## Data Readiness v0.7

`DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7` se ejecuta antes de reabrir un
benchmark tras v0.6. Sus reglas principales son:

- menos de 24 observaciones: `DATA_GATE=BLOCK`;
- 24 a 29 observaciones: `DATA_GATE=REVIEW`;
- 30 o mas observaciones solo pueden aprobar backtest si licencia,
  comparabilidad, metadata, gaps y leakage pasan;
- `publication_gate=BLOCK` permanece activo.

Esto evita convertir evidencia de frontera en ajuste oportunista del modelo.

## WDI Source Pack v0.8

`DUAT_WDI_OFFICIAL_SOURCE_PACK_v0_8` no ejecuta ForecastGate predictivo ni
backtest. Solo prepara datos oficiales largos:

- raw WDI JSON con SHA256;
- processed JSON/CSV con SHA256;
- manifest y source cards;
- LicenseTermsScan, ComparabilityReview y LeakagePreflight;
- `publication_gate=BLOCK`.

Aunque las series WDI cumplan el minimo de observaciones, `ForecastGate` queda
en `REVIEW` hasta que licencia y comparabilidad pasen revision.

## WDI Governance v0.8.1

`DUAT_WDI_LICENSE_COMPARABILITY_REVIEW_v0_8_1` calcula:

- `DataGate=REVIEW`;
- `BacktestOpenGate=REVIEW_ONLY_DRY_RUN`;
- `publication_gate=BLOCK`.

El caveat de terceros en terminos World Bank y las fuentes/modelos subyacentes
de indicadores mantienen licencia y comparabilidad en `REVIEW`. Un v0.9 solo
puede ser laboratorio interno/dry-run mientras esos gates no pasen.

## Falsificadores

- Un modelo que pierde contra baseline queda bloqueado para produccion.
- Una fuente sin SourceCard no entra a aprobacion.
- Una serie con leakage temporal no entra a prediccion.
- Bloqueado: una salida que confunde inferencia con causalidad.
