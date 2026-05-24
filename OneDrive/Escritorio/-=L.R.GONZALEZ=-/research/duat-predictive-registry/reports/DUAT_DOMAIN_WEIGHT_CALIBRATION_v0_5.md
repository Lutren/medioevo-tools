# DUAT Domain Weight Calibration v0.5

publication_gate: BLOCK
status: REVIEW

This diagnostic uses fold-local training values and a small grid. It remains REVIEW until a nested backtest exists.

| indicator | status | baseline MAE | best MAE | baseline RMSE | best RMSE | best window | last value weight |
|---|---|---:|---:|---:|---:|---:|---:|
| economy.real_growth_rate | NOT_IMPROVED | 3.8967183222746695 | 3.6718912147156946 | 4.585415858753202 | 4.864101978142136 | 5 | 0.25 |
| labor_market.unemployment_rate.total | REVIEW | 0.423388888888889 | 0.3933563888888889 | 0.5068877072663904 | 0.4861372550827575 | 5 | 0.5 |
| demography.life_expectancy_at_birth.total | NOT_IMPROVED | 1.1363333333333305 | 1.1993569444444436 | 1.8158352531732236 | 1.6873710416740288 | 5 | 0.75 |
