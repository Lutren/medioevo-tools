# economy.real_growth_rate WDI Source Card v0.8

ID: economy.real_growth_rate
Name: GDP growth (annual %)
Origin: World Bank World Development Indicators
API endpoint: https://api.worldbank.org/v2/country/MEX/indicator/NY.GDP.MKTP.KD.ZG
Accessed at: 2026-05-15T07:47:49Z
Hash raw: 0277d9db0a5954e5a922c0249ee80e09d88863e44f7d8aa413a504f05703efd5
Hash processed: 3a7eed8f168f9bf3d45cf7a4af55043263083e3e83c7beb094b4c4923722a46d
Indicator mapping: economy.real_growth_rate -> NY.GDP.MKTP.KD.ZG
Functional summary: annual annual_percent_growth series for local readiness review.

CERTEZA:
- n_observations=64; frequency=annual.
- raw_file=data_sources/world_bank_wdi/raw/MEX_NY.GDP.MKTP.KD.ZG_raw.json.
- processed_file=data_sources/world_bank_wdi/processed/MEX_NY.GDP.MKTP.KD.ZG_processed.json.

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
