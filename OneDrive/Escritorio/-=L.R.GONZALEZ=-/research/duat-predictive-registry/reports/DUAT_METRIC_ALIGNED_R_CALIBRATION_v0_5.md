# DUAT Metric-Aligned R Calibration v0.5

publication_gate: BLOCK
run_id: DUAT_METRIC_ALIGNED_R_CALIBRATION_v0_5
action_gate_local: REVIEW

R reduction does not equal predictive validation.
This report preserves operational R and adds metric-aligned R with explicit penalties.

| indicator | metric_status | R operational delta | R aligned delta | floor | predictive claim gate |
|---|---|---:|---:|---|---|
| economy.real_growth_rate | MIXED | -0.06456924788966409 | -0.025437084244559177 | False | REVIEW |
| labor_market.unemployment_rate.total | WORSE | -0.047802475183044923 | 0.0 | True | REVIEW |
| demography.life_expectancy_at_birth.total | WORSE | -0.05086429038658982 | 0.027607323287996893 | True | REVIEW |

## Boundary

- Internal local benchmark only.
- Operational R reduction is not a public predictive claim.
- Metrics that worsen force REVIEW or BLOCK behavior.
- publication_gate remains BLOCK.
