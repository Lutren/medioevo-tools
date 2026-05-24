# DUAT Nested Domain Backtest v0.6

publication_gate: BLOCK
run_id: DUAT_NESTED_DOMAIN_BACKTEST_v0_6
action_gate_local: REVIEW

nested backtest is internal technical evidence only.
R reduction does not equal predictive validation.

| indicator | observations | outer folds | OOS classification | MAE delta | RMSE delta | R aligned delta | gate |
|---|---:|---:|---|---:|---:|---:|---|
| economy.real_growth_rate | 12 | 2 | OOS_METRICS_WORSE | 0.41321448382956394 | 0.4070954727223004 | 0.13769860703984477 | REVIEW |
| labor_market.unemployment_rate.total | 18 | 3 | OOS_METRICS_WORSE | 0.32545624999999995 | 0.34242573811211957 | 0.5680389385462083 | REVIEW |
| demography.life_expectancy_at_birth.total | 12 | 2 | OOS_METRICS_WORSE | 0.6678124999999966 | 0.9248536197411587 | 0.45259772046343194 | REVIEW |

## Boundary

- Walk-forward validation uses only past data for configuration selection.
- Outer test folds are never used to select parameters.
- LicenseTermsScan and ComparabilityReview remain gates for publication.
- No external prediction, causal assertion or social ordering claim is authorized.
