# DUAT Official Long-History Data Readiness v0.7

publication_gate: BLOCK
run_id: DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7
data_gate: BLOCK
recommendation: collect_data

This is internal boundary evidence and data readiness work. It is not approved for publication.

| indicator | source | observations | minimum review | license | comparability | leakage | gate |
|---|---|---:|---|---|---|---|---|
| economy.real_growth_rate | world_bank_indicators | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |
| economy.real_growth_rate | eurostat_sdmx | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |
| labor_market.unemployment_rate.total | world_bank_indicators | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |
| labor_market.unemployment_rate.total | eurostat_sdmx | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |
| labor_market.unemployment_rate.total | INEGI | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |
| demography.life_expectancy_at_birth.total | world_bank_indicators | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |
| demography.life_expectancy_at_birth.total | eurostat_sdmx | 6 | BLOCK | REVIEW | REVIEW | PASS | BLOCK |

## Boundary

- v0.6 remains frozen as boundary evidence.
- No model weights were changed in v0.7.
- A new benchmark requires official long-history data, source provenance, license review, comparability review and leakage preflight.
