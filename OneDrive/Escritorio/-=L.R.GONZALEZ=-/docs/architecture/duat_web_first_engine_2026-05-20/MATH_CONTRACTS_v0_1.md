# MATH_CONTRACTS v0.1

## Status

Estos contratos son operacionales, no claims de fisica validada.

## Types

```txt
WorldState(t) = {
  geography, era, climate, astronomy, culture, laws,
  resources, events, factions, map_state, active_stimuli
}
```

```txt
AgentState_i(t) = {
  body, needs, traits, lineage, sensory_profile, bias_profile,
  memory, beliefs, goals, relationships, role, skills,
  emotional_state, cognitive_load, R_i, Phi_eff_i
}
```

```txt
ObservationEnvelope_i,c(t) = {
  channel, raw_observation_proxy, missingness, noise,
  contradiction, confidence, timestamp, spatial_ref, evidence_refs
}
```

```txt
SharedReality(t) = {
  fused_observations, confidence_field,
  unresolved_contradictions, canonical_state_estimate
}
```

```txt
BiasProfile_i = {
  cultural_bias, lineage_bias, trauma_history,
  role_bias, perceptual_weighting
}
```

```txt
TaskState = { task_id, owner, utility, status, evidence, gate, progress }
PlannerState = { candidate_actions, expected_utility, cost, gate, rationale }
ActionGateDecision = { decision, reason, evidence, boundary, timestamp }
WitnessEvent = { id, tick, type, summary, evidence, R, Phi_eff, gate }
ReplayHash = { tick, prev_hash, state_hash, action_hash, event_hash }
```

## Equations

```txt
Observation_i,c = Channel_c(World) + Bias_i,c + Noise_i,c + Missingness_i,c + Contradiction_i,c
```

```txt
SharedReality = weighted_fusion(observations, trust, evidence, calibration, recency)
```

```txt
R_i = weighted(prediction_error, contradiction, missingness, instability, boundary_risk)
```

```txt
Phi_eff_i = useful_action_output / (information_cost + compute_cost + correction_cost + epsilon)
```

```txt
TaskUtility = need_score * goal_score * role_fit * feasibility * social_pressure * gate_modifier
```

## Replay

```txt
H_t = sha256(schema_version | seed | tick | prev_hash | action_hash | state_delta_hash | witness_hash)
```

Rules:
- Canonical JSON sorted keys.
- No wall-clock in hash.
- External/cloud enrichments referenced by cache hash.
- Failed gates are events too.

