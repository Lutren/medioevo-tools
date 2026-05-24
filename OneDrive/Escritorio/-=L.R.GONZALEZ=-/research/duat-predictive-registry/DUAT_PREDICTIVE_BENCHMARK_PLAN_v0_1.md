# DUAT Predictive Benchmark Plan v0.1

publication_gate: BLOCK

## Benchmark v0.2 Ejecutado

Objetivo: `DUAT_GEODIA_HARMONIZED_INDICATOR_ONE_STEP_FORECAST_v0_1`.

Modo: fixture real offline desde GEODIA, sin red y sin credenciales.

Indicador: `economy.real_growth_rate`.

Resultado: el benchmark mide `R_before/R_after` con baseline retrospectivo y
ensemble ponderado. La salida queda en `REVIEW` porque los terminos/licencias y
la comparabilidad economica siguen en revision. `publication_gate=BLOCK`.

## Objetivo

Medir si una fuente o metodo reduce `R_pred` y mejora error/calibracion contra
baseline antes de integrarlo en DUAT.

## Baseline minimo

- naive last value;
- seasonal naive si hay estacionalidad;
- moving average robusto;
- no external source.

## Validacion temporal

- usar TimeSeriesSplit o cortes temporales equivalentes;
- prohibir data leakage;
- separar train, validation y test por fecha;
- registrar fecha de captura y hash de fixture.

## Metricas

- MAE/RMSE para continuo;
- Brier/log-loss/calibration curve para probabilistico;
- interval coverage para conformal;
- `R_before`, `R_after`, `Phi_eff_before`, `Phi_eff_after`;
- falsificador de fuente y de modelo.

## Siguiente benchmark

Elegir un objetivo concreto de DUAT y correr backtest historico o ventana de N
dias. Hasta entonces, toda mejora queda en INFERENCIA.
