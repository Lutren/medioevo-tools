# DUAT Predictive Registry v0.1

publication_gate: BLOCK

## Benchmark Matrix v0.3

`DUAT_PREDICTIVE_BENCHMARK_MATRIX_v0_3` replica el benchmark R_before/R_after
en dos indicadores reales offline:

- `economy.real_growth_rate`
- `labor_market.unemployment_rate.total`

La salida solo cuenta como evidencia tecnica interna. No habilita claims
publicos de prediccion, jerarquizacion social, causalidad o validacion
cientifica/comercial.
external_publication: false

## Domain Calibration Gate v0.4

`DUAT_DOMAIN_CALIBRATION_GATE_v0_4` extiende la matriz con un tercer indicador
real offline:

- `demography.life_expectancy_at_birth.total`

La nueva capa clasifica cada objetivo por dos ejes separados:

- R operacional: `R_before`, `R_after`, `R_delta`;
- precision directa: deltas de MAE, RMSE y MAPE_if_safe.

Regla activa: una reduccion de R no equivale a validacion predictiva. Si las
metricas empeoran, el resultado se reporta como frontera de calibracion por
dominio, no como mejora predictiva.

## Metric-Aligned R v0.5

`DUAT_METRIC_ALIGNED_R_CALIBRATION_v0_5` preserva el R operacional historico
de v0.4 y agrega `R_after_aligned` con penalizacion por degradacion de
metricas. El objetivo es impedir que una baja de R operacional sea presentada
como mejora predictiva cuando MAE/RMSE/MAPE empeoran.

Campos nuevos:

- `metric_degradation_score`
- `metric_penalty`
- `R_after_aligned`
- `R_delta_aligned`
- `alignment_classification`
- `predictive_claim_gate`

El resultado v0.5 queda en `REVIEW`; `publication_gate=BLOCK`.

## Nested Domain Backtest v0.6

`DUAT_NESTED_DOMAIN_BACKTEST_v0_6` prueba si la calibracion por dominio sobrevive
a evaluacion fuera de muestra:

- seleccion interna con folds de pasado;
- evaluacion externa en el siguiente punto temporal;
- guardia anti-leakage;
- `OutOfSampleGate` separado de `ForecastGate`.

El resultado v0.6 debe leerse como diagnostico interno. Si las metricas OOS
empeoran, no hay claim predictivo aunque haya evidencia operacional previa.

## Official Long-History Data Readiness v0.7

`DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7` agrega una etapa previa a todo
nuevo benchmark:

- manifiesto de fuente oficial;
- revision de licencia/terminos;
- auditoria de cobertura temporal;
- comparabilidad de unidad/definicion;
- leakage preflight;
- minimo de observaciones para walk-forward.

El resultado actual bloquea el re-benchmark con los fixtures cortos y mantiene
`publication_gate=BLOCK`.

## World Bank WDI Source Pack v0.8

v0.8 agrega la primera fuente oficial larga para reabrir benchmarks futuros:

- World Bank World Development Indicators API v2;
- scope `MEX`;
- tres indicadores DUAT mapeados a WDI;
- raw/processed hashes;
- source cards y reviews de licencia/comparabilidad;
- `DataGate=REVIEW` por revisiones pendientes.

No hay backtest, ajuste de modelo, claim publico, ranking ni causalidad en v0.8.

## WDI Governance v0.8.1

v0.8.1 agrega la decision de gobernanza para el source pack WDI:

- terminos World Bank verificados contra URL oficial;
- licencia queda `REVIEW` por caveat de terceros y revision humana/legal;
- comparabilidad queda `REVIEW` por estimaciones/modelado/fuentes multiples;
- leakage sigue `PASS`;
- `BacktestOpenGate=REVIEW_ONLY_DRY_RUN`.

Esto no abre publicacion ni validacion predictiva; solo permite planear un
posible v0.9 interno si el humano acepta el gate de review.

## Objetivo

Registrar fuentes, metodos y formulas para escenarios DUAT con menos ruido
operacional, sin prometer verdad, causalidad ni acierto garantizado.

## Formula base

```text
H_eff_pred = H_raw * SourceQuality * Freshness * Coverage * Phi_eff * CalibrationScore
Freshness = exp(-lambda_age * age_days)
Coverage = valid_points / expected_points
CalibrationScore = 1 - normalized_historical_error

R_pred = clamp01(
  0.25*R_source +
  0.20*R_missing +
  0.20*R_temporal +
  0.20*R_contra +
  0.15*R_model
)

SourceQuality = weighted_mean(
  provenance_score,
  license_score,
  api_stability_score,
  granularity_score,
  coverage_score,
  traceability_score,
  reproducibility_score
)

prediction_final = sum(w_i * prediction_i) / sum(w_i)
w_i = exp(-lambda_error*error_i - lambda_noise*R_pred_i - lambda_age*age_i) * SourceQuality_i
```

## Metodos

Los metodos aprobables en laboratorio son filtros, validadores, calibradores,
intervalos e infraestructura de backtest. Los metodos causales quedan en REVIEW
hasta tener grafo causal, identificacion y falsificadores.

## Fuentes

Fuentes oficiales/no-key pueden entrar a smoke local con SourceCard. Fuentes con
key quedan en REVIEW_KEY_REQUIRED. Indices como Kaggle/OpenML/awesomedata no
son verdad primaria.

## Claim boundary

DUAT genera escenarios operativos con fuente, incertidumbre, backtest y gate. No
es oraculo ni reemplaza juicio humano/legal/cientifico.
