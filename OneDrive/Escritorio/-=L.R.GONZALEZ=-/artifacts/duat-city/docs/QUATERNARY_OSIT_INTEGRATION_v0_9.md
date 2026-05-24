# QUATERNARY OSIT INTEGRATION v0.9

## OSIT Panel

`QuaternaryPanel` appears inside OSIT mode and exposes:

- global counts for `00`, `01`, `10`, `11`;
- `R_quaternary` and `Phi_quaternary`;
- average frequency, permanence and stability;
- combined R/Phi estimate;
- top anomalies and unstable sources;
- copyable quaternary handoff JSON.

## City Metrics

The quaternary metrics are added as `state.quaternary`. The existing city `R` and `Phi_eff` remain unchanged. Combined values live in `state.quaternary.combinedR` and `state.quaternary.combinedPhi`.

## WitnessLog

Witness entries use type `quaternary_timing_gate` and are rate-limited. The engine logs only when the quaternary gate crosses REVIEW/BLOCK, significant absence grows, or instability persists.

## Agent Inspector

Selected agents show Q state, dwell, frequency and stability when the timing adapter has evaluated that agent.

