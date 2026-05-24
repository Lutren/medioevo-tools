# MATH_AND_MODELING_GAPS

## Gaps principales

1. No existe todavia un contrato formal unico para `WorldState(t)` compartido entre GEODIA, DUAT City y Wabi.
2. `ObservationEnvelope` no esta normalizado como tipo compartido.
3. `SharedReality` existe como idea, pero no como fusion ponderada con confianza, evidencia, calibracion y recencia.
4. `BiasProfile` aparece en discurso/canon, pero falta contrato operativo.
5. `TaskUtility` existe de forma parcial en tareas/necesidades; falta ecuacion unica.
6. Replay aun no es completo: sim/RPG core ya puede ser determinista, pero quaternary/witness conservan estado global.
7. GLOMO unisensorial no tiene benchmark contra late-fusion multimodal tradicional.

## Matematica operacional minima

No se declara como fisica validada. Es matematica pragmatica de sistema.

```txt
Observation_i,c(t) =
  Channel_c(WorldState(t), AgentPose_i(t))
  + Bias_i,c(t)
  + Noise_i,c(t)
  + Missingness_i,c(t)
  + Contradiction_i,c(t)
```

```txt
w_i,c(t) =
  trust_i,c
  * evidence_i,c
  * calibration_i,c
  * recency_i,c
  * (1 - boundary_risk_i,c)
```

```txt
SharedReality_k(t) =
  sum_i,c(w_i,c(t) * observation_i,c,k(t))
  / max(epsilon, sum_i,c(w_i,c(t)))
```

```txt
R_i(t) =
  clamp01(
    w_pe * prediction_error_i
    + w_contra * contradiction_i
    + w_missing * missingness_i
    + w_instability * instability_i
    + w_boundary * boundary_risk_i
    + w_load * cognitive_load_i
  )
```

```txt
Phi_eff_i(t) =
  useful_action_output_i
  / (information_cost_i + compute_cost_i + correction_cost_i + epsilon)
```

```txt
TaskUtility_i,a(t) =
  need_score_i,a
  * goal_score_i,a
  * role_fit_i,a
  * feasibility_i,a
  * social_pressure_i,a
  * gate_modifier_i,a
  - R_penalty_i,a
  - opportunity_cost_i,a
```

## Gaps de modelo por prioridad

- P0: contratos `WorldState`, `AgentState`, `ObservationEnvelope`, `ReplayHash`.
- P0: replay hash canonical JSON con seed/tick/action/state_delta/prev_hash.
- P1: SharedReality fusion field.
- P1: benchmark GLOMO.
- P2: lineage/theatre genealogico y cultura/leyes por epoca.

