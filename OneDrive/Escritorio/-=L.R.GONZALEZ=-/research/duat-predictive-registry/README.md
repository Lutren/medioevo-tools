# DUAT Predictive Registry

Estado: local research / publication_gate=BLOCK.

Este carril registra filtros multidimensionales, metodos predictivos, fuentes
gratuitas y gates para mejorar escenarios DUAT. No convierte el sistema en
oraculo, no es predictor electoral, no ordena personas o territorios y no es
motor causal.

## Regla central

Mas informacion no aumenta R automaticamente. Mas informacion crea mas
dimensiones de R. DUAT debe responder con filtros especializados, SourceCards,
SourceQuality, ForecastGate, backtest y falsificadores.

## Componentes

- `DUAT_MULTIDIMENSIONAL_FILTER_ECOLOGY_v0_1.md`
- `DUAT_DUAL_LANE_COGNITIVE_FILTER_v0_1.md`
- `DUAT_PREDICTIVE_REGISTRY_v0_1.md`
- `DUAT_FORECASTGATE_v0_1.md`
- `fixtures/duat_first_predictive_objective_v0_1.json`
- `reports/duat-r-before-after-benchmark-v0-1.json`
- `DUAT_FREE_SIGNAL_SOURCES_CATALOG_v0_1.json`
- `DUAT_PREDICTIVE_METHODS_CATALOG_v0_1.json`
- `duat_predictive_registry/`
- `tests/`

## Benchmark v0.2

Primer objetivo ejecutable:
`DUAT_GEODIA_HARMONIZED_INDICATOR_ONE_STEP_FORECAST_v0_1`.

Comando local desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli benchmark --objective fixtures/duat_first_predictive_objective_v0_1.json --out reports/duat-r-before-after-benchmark-v0-1.json --markdown-out reports/DUAT_R_BEFORE_AFTER_BENCHMARK_v0_1.md --pretty
```

Este benchmark usa fixtures offline GEODIA para `economy.real_growth_rate`.
La comparabilidad y licencias siguen en `REVIEW`; `publication_gate=BLOCK`.
No autoriza publicacion, jerarquizacion social, causalidad ni prediccion publica.

## Benchmark Matrix v0.3

Comando local desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli benchmark-matrix --objectives fixtures/duat_first_predictive_objective_v0_1.json fixtures/duat_labor_market_unemployment_objective_v0_1.json --out reports/duat-benchmark-matrix-v0-3.json --markdown-out reports/DUAT_BENCHMARK_MATRIX_v0_3.md --review-out reports/DUAT_LICENSE_AND_COMPARABILITY_REVIEW_v0_1.md --pretty
```

La matriz compara `economy.real_growth_rate` y
`labor_market.unemployment_rate.total` con fixtures reales offline. El resultado
es evidencia tecnica interna solamente; `publication_gate=BLOCK` y
`LicenseTermsScan=REVIEW`.

## Domain Calibration Gate v0.4

Comandos locales desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli benchmark-matrix --objectives fixtures/duat_first_predictive_objective_v0_1.json fixtures/duat_labor_market_unemployment_objective_v0_1.json fixtures/duat_non_economic_third_indicator_objective_v0_1.json --out reports/duat-benchmark-matrix-v0-4.json --markdown-out reports/DUAT_BENCHMARK_MATRIX_v0_4.md --review-out reports/DUAT_LICENSE_AND_COMPARABILITY_REVIEW_v0_1.md --pretty

python -m duat_predictive_registry.cli calibrate-domains --matrix reports/duat-benchmark-matrix-v0-4.json --out reports/duat-domain-calibration-gate-v0-4.json --markdown-out reports/DUAT_DOMAIN_CALIBRATION_GATE_v0_4.md --pretty
```

`DomainCalibrationGate` separa dos resultados que no son equivalentes:

- reduccion operacional de R;
- mejora directa de metricas predictivas como MAE, RMSE y MAPE_if_safe.

`R_delta < 0` por si solo no autoriza claim predictivo. La matriz v0.4 agrega
`demography.life_expectancy_at_birth.total` como tercer indicador real offline,
mantiene `publication_gate=BLOCK` y conserva `LicenseTermsScan=REVIEW`.

## Metric-Aligned R Calibration v0.5

Comandos locales desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli metric-align-r --calibration reports/duat-domain-calibration-gate-v0-4.json --matrix reports/duat-benchmark-matrix-v0-4.json --out reports/duat-metric-aligned-r-calibration-v0-5.json --markdown-out reports/DUAT_METRIC_ALIGNED_R_CALIBRATION_v0_5.md --pretty

python -m duat_predictive_registry.cli calibrate-domain-weights --matrix reports/duat-benchmark-matrix-v0-4.json --out reports/duat-domain-weight-calibration-v0-5.json --markdown-out reports/DUAT_DOMAIN_WEIGHT_CALIBRATION_v0_5.md --pretty
```

`MetricAlignedR` preserva `R_operational_before`, `R_operational_after` y
`R_operational_delta`, y agrega una capa penalizada por degradacion de MAE,
RMSE y MAPE_if_safe. Si MAE y RMSE empeoran, se aplica piso de alineacion:
`R_after_aligned` no puede presentarse como mejora predictiva.

`PredictiveClaimGate` conserva todos los indicadores de v0.5 en `REVIEW`.
`publication_gate=BLOCK`; el resultado sigue siendo benchmark local interno,
no validacion predictiva publica.

## Nested Domain Backtest v0.6

Comando local desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli nested-backtest --matrix reports/duat-benchmark-matrix-v0-4.json --metric-aligned reports/duat-metric-aligned-r-calibration-v0-5.json --out reports/duat-nested-domain-backtest-v0-6.json --markdown-out reports/DUAT_NESTED_DOMAIN_BACKTEST_v0_6.md --pretty
```

`NestedBacktest` ejecuta walk-forward con seleccion interna de configuracion y
evaluacion externa fuera de muestra. El test externo no participa en la
seleccion de ventanas/pesos. En v0.6 los tres indicadores reales quedan
`OOS_METRICS_WORSE`; esto es evidencia de frontera de calibracion, no
validacion predictiva. `publication_gate=BLOCK`.

## Official Long-History Data Readiness v0.7

Comando local desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli data-readiness --manifest data_sources/duat_official_long_history_manifest_v0_7.json --schema schemas/duat_data_readiness_report_v0_7.schema.json --pretty --out reports/duat-official-long-history-data-readiness-v0-7.json --markdown-out reports/DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7.md
```

v0.7 congela v0.6 como evidencia de frontera y revisa si las series oficiales
locales tienen historia suficientemente larga para volver a correr backtest. La
salida actual conserva `DataGate=BLOCK` porque los fixtures existentes tienen
6 observaciones por fuente, menos que el minimo de 24. La recomendacion es
`collect_data`, no ajustar pesos sobre el mismo historial corto.

## World Bank WDI Source Pack v0.8

Comando local desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli wdi-source-pack --country MEX --indicators NY.GDP.MKTP.KD.ZG SL.UEM.TOTL.ZS SP.DYN.LE00.IN --out reports/duat-world-bank-wdi-source-pack-v0-8.json --pretty
```

`DUAT_WDI_OFFICIAL_SOURCE_PACK_v0_8` crea el primer paquete oficial de historia
larga para DUAT usando World Bank World Development Indicators. Mapeo:

- `economy.real_growth_rate` -> `NY.GDP.MKTP.KD.ZG`
- `labor_market.unemployment_rate.total` -> `SL.UEM.TOTL.ZS`
- `demography.life_expectancy_at_birth.total` -> `SP.DYN.LE00.IN`

El scope actual es `MEX`, detectado en los fixtures/manifests previos y pasado
explícitamente al CLI. v0.8 descarga raw JSON, genera processed JSON/CSV,
source cards, manifest y reporte; no ejecuta backtest. `DataGate=REVIEW`
porque las series tienen historia suficiente pero `LicenseTermsScan` y
`ComparabilityReview` siguen en `REVIEW`. `publication_gate=BLOCK`.

## WDI License/Comparability Governance v0.8.1

Comando local desde esta carpeta:

```powershell
python -m duat_predictive_registry.cli wdi-governance-review --manifest data_sources/world_bank_wdi/world_bank_wdi_manifest_v0_8.json --out reports/duat-world-bank-wdi-governance-review-v0-8-1.json --pretty
```

`DUAT_WDI_LICENSE_COMPARABILITY_REVIEW_v0_8_1` revisa los dos gates pendientes
de v0.8. Resultado actual:

- `LicenseTermsScan=REVIEW`
- `ComparabilityReview=REVIEW`
- `LeakagePreflight=PASS`
- `DataGate=REVIEW`
- `BacktestOpenGate=REVIEW_ONLY_DRY_RUN`

v0.9, si se abre, solo puede ser dry-run interno. No hay aprobacion de
prediccion publica, ranking, causalidad, inferencia electoral ni claim de
modelo.

## QA

```powershell
python -m pytest research/duat-predictive-registry/tests
```

No publicar, no push, no deploy, no credenciales, no claims fuertes.
