# Integración: Audio Engine v1.2.1 + Physics/Light v1.3.0

**Fingerprint:** DUAT-v1.3.0-AUDIO-INTEGRATION

## Puentes

### LightAudioBridge
- Luz Q=11 (burst) → audio eventBurst
- Luz Q=01 (anomalía) → audio missing_signal_pulse
- Luz Q=00→10 (estabilización) → audio light_stable_hum

### PhysicsAudioBridge
- Transición WATER→STEAM → audio water_boil
- Colisión sólida (v>50) → audio collision_impact
- Cambio brusco presión (ΔP>1) → audio pressure_burst

## Métricas Compartidas

| Métrica | Audio v1.2.1 | Physics/Light v1.3.0 |
|---------|--------------|----------------------|
| R | R_audio | R_physics |
| Phi_eff | Phi_audio | Phi_physics |
| J_c | clipping/silence | jammingThreshold |

## Unificación

```typescript
interface UnifiedMetrics {
  R_system: max(R_audio, R_physics, R_quest);
  Phi_system: min(Phi_audio, Phi_physics, Phi_quest);
  regime: OSIT regime;
}
```

## Event Loop

```
1. Physics.step() → dirty cells, collisions, transitions
2. LightField.propagate() → Q-states, lux
3. Bridges.process() → audio events
4. AudioEngine.render() → sonido
5. CPURenderer.render() → píxeles
6. NPC.update() → OSIT observe
7. Quest.update() → R_quest, Phi_quest
```
