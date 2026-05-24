# World Bank WDI Source Card v0.8

ID: WORLD_BANK_WDI_v0_8
Name: World Bank World Development Indicators
Origin: World Bank API v2
API endpoint: https://api.worldbank.org/v2
Accessed at: 2026-05-15T07:47:49Z
Scope: MEX - Mexico

Functional summary: official long-history data source pack for DUAT readiness only.

CERTEZA:
- Raw JSON responses and processed series are stored locally with SHA256 hashes.
- No benchmark is executed in v0.8.

INFERENCIA:
- The series may support an internal backtest after human/license/comparability review.

INCÓGNITA:
- Final legal interpretation of terms and upstream source restrictions.
- Domain-level comparability under source revisions and methodology changes.

BLOQUEO:
- publication_gate=BLOCK.
- Not approved for public prediction, ranking, causality or electoral use.

License: REVIEW.
Comparability: REVIEW.
Leakage: PASS unless future-year records are detected.
Destination: DUAT source pack local artifact.
Trace: manifest `world_bank_wdi_manifest_v0_8.json`.
