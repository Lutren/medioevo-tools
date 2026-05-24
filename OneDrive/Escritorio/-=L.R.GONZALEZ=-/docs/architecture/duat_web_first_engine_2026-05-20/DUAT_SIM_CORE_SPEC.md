# DUAT_SIM_CORE_SPEC v0.1

## Objetivo

DUAT sim-core es la verdad del mundo, no el renderer ni el creador de apps. Debe correr localmente con CPU y poca RAM, producir replay determinista y alimentar distintos modos de experiencia.

## Contratos principales

### WorldState(t)

- `geography`: region, bioma, elevacion, cuerpos de agua, rutas.
- `era`: periodo historico/futuro, tecnologia disponible, calendario.
- `climate`: temperatura, humedad, lluvia, viento, estaciones.
- `astronomy`: sol/luna/ciclos, hora, eventos celestes.
- `culture`: normas, idioma, simbolos, tabues, rituales.
- `laws`: reglas sociales, politicas, comercio, castigos.
- `resources`: comida, energia, materiales, conocimiento, confianza.
- `events`: cola de eventos canon-safe.
- `factions`: grupos, poder, objetivos, relaciones.
- `map_state`: tiles/chunks/objetos/ocupacion.
- `active_stimuli`: sonidos, luces, clima, riesgos, rumores.

### AgentState_i(t)

- `body`, `needs`, `traits`, `lineage`, `sensory_profile`.
- `bias_profile`, `memory`, `beliefs`, `goals`, `relationships`.
- `role`, `skills`, `emotional_state`, `cognitive_load`.
- `R_i`, `Phi_eff_i`, `current_task`, `pose`, `inventory`.

### ObservationEnvelope_i,c(t)

- `agent_id`, `channel`, `timestamp`, `raw_observation_proxy`.
- `missingness`, `noise`, `contradiction`, `confidence`.
- `spatial_ref`, `evidence_refs`, `raw_ref_hash`.

### SharedReality(t)

- `fused_observations`
- `confidence_field`
- `unresolved_contradictions`
- `canonical_state_estimate`

### Runtime records

- `TaskState`: owner, utility, evidence, progress, gate, closure.
- `PlannerState`: candidate actions, cost, expected utility, blocked causes.
- `ActionGateDecision`: approve/review/block with evidence.
- `WitnessEvent`: local event with source, summary, evidence.
- `ReplayHash`: deterministic hash chain.

## Determinism rule

- No direct `Math.random`/global random in sim.
- Random source is injected or derived from canonical seed and state.
- Time uses tick, not wall clock, inside sim.
- External enrichment is cached and replayed by hash.

## Experience modes over same WorldState

- Sims mode: camera follows one agent; same state, narrow lens.
- SimCity mode: macro controls; same state, aggregated controls.
- RPG mode: user inhabits one actor; same state, input becomes agent action.
- Director mode: injects events through ActionGate; same state, event log.

