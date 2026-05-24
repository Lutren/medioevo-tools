# DUAT Domain Calibration Gate v0.4

publication_gate: BLOCK
run_id: DUAT_DOMAIN_CALIBRATION_GATE_v0_4
action_gate_local: REVIEW

## Boundary

This is an internal local benchmark. R reduction does not equal predictive validation.
The report separates operational residue reduction from direct forecast error metrics.

## Matrix

| indicator | domain | data_mode | R_delta | MAE delta | RMSE delta | classification | gate |
|---|---|---|---:|---:|---:|---|---|
| economy.real_growth_rate | economy | real_fixture | -0.06456924788966409 | -0.018274044256341604 | 1.025355678660512 | OPERATIONAL_R_IMPROVED_METRICS_MIXED | REVIEW |
| labor_market.unemployment_rate.total | labor_market | real_fixture | -0.047802475183044923 | 0.03051300904088816 | 0.049099864075189736 | OPERATIONAL_R_IMPROVED_METRICS_WORSE | REVIEW |
| demography.life_expectancy_at_birth.total | demography | real_fixture | -0.05086429038658982 | 0.3371498800775281 | 0.12891789174921664 | OPERATIONAL_R_IMPROVED_METRICS_WORSE | REVIEW |

## Claim Boundary

- Internal technical evidence only.
- No public predictive claim.
- No ranking, causal claim or external release.
- LicenseTermsScan remains REVIEW pending human/legal review.

## Next Action

Calibrate per-domain model weights before treating operational R reduction as direct accuracy improvement.
