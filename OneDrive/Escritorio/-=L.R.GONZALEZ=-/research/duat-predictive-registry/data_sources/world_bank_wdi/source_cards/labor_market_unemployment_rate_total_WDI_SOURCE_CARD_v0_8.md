# labor_market.unemployment_rate.total WDI Source Card v0.8

ID: labor_market.unemployment_rate.total
Name: Unemployment, total (% of total labor force) (modeled ILO estimate)
Origin: World Bank World Development Indicators
API endpoint: https://api.worldbank.org/v2/country/MEX/indicator/SL.UEM.TOTL.ZS
Accessed at: 2026-05-15T07:47:49Z
Hash raw: 8e1266859c8d29852012fc96f688a4097c5d6436a2bd900cccb3d97b66890b23
Hash processed: c60dab757f0635ad71ce5e5b2d5ffd06a8df64bf4b4d8ddd4fffccb3474f9c64
Indicator mapping: labor_market.unemployment_rate.total -> SL.UEM.TOTL.ZS
Functional summary: annual percent_of_total_labor_force series for local readiness review.

CERTEZA:
- n_observations=35; frequency=annual.
- raw_file=data_sources/world_bank_wdi/raw/MEX_SL.UEM.TOTL.ZS_raw.json.
- processed_file=data_sources/world_bank_wdi/processed/MEX_SL.UEM.TOTL.ZS_processed.json.

INFERENCIA:
- The series can be considered for internal backtest after remaining review gates.

INCÓGNITA:
- Final terms/license interpretation and comparability details.

BLOQUEO:
- No public prediction, ranking or causality claim.
- publication_gate=BLOCK.

License: REVIEW
Comparability: REVIEW
Gaps: []
Leakage: PASS
Destination: DUAT local source pack.
Trace: world_bank_wdi_manifest_v0_8.json.
