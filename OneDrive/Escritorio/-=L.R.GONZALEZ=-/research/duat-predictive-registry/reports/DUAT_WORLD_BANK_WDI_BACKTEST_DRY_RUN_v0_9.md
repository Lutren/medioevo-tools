# DUAT WDI Backtest Dry Run v0.9

run_id: `DUAT_WDI_BACKTEST_DRY_RUN_v0_9`
status: `REVIEW_INTERNAL_ONLY`
DataGate: `REVIEW`
BacktestOpenGate: `REVIEW_ONLY_DRY_RUN`
publication_gate: `BLOCK`

Internal dry-run only. No public prediction, ranking, causal claim, electoral prediction or benchmark claim is allowed.

| indicator | observations | folds | naive MAE | ma3 MAE | comparability | license |
|---|---:|---:|---:|---:|---|---|
| economy.real_growth_rate | 64 | 54 | 3.10185 | 3.142176 | REVIEW | REVIEW |
| labor_market.unemployment_rate.total | 35 | 25 | 0.34308 | 0.547267 | REVIEW | REVIEW |
| demography.life_expectancy_at_birth.total | 65 | 55 | 0.492491 | 0.884091 | REVIEW | REVIEW |

## Gates

- LeakagePreflight: PASS
- ClaimsScan: PASS_LOW_CLAIM_INTERNAL_ONLY
- PublicationGate: BLOCK
- Final: REVIEW_INTERNAL_ONLY while license/comparability remain REVIEW.
