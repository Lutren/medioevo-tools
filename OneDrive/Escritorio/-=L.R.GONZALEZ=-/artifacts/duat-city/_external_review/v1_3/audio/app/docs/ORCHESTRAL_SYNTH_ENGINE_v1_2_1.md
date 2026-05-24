# Orchestral Synth Engine v1.2.1

**Fingerprint:** DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC

## Instrumentos Sinteticos

### Cuerdas (SyntheticStrings)
- **lowDrone**: Cuerdas graves con vibrato (5Hz) y bow noise
- **highShimmer**: Cuerdas brillantes con detune múltiple

### Bronces (SyntheticBrass)
- **swell**: Creciente dramático con formant filters (300, 850, 2500Hz)
- **staccatoHit**: Golpe corto con saw/triangle softened
- **ritualHorn**: Cuerno ceremonial con ratios φ

### Coro (SyntheticChoir)
- **pad**: Coro sostenido con formantes vocálicas (A, E, I, O, U)
- **drone**: Coro con vocal 'o'
- **breath**: Suspiro coral con ruido filtrado

### Percusion (SyntheticPercussion)
- **timpaniHit**: Cuerpo con pitch envelope descendente
- **bell**: Parciales inarmónicos (1, 1.17, 1.33, 1.53, 2.0, 2.67)
- **bowedMetal**: Metal frotado con vibrato irregular
- **lowPercussion**: Golpe grave de tambor

## Mood Mapping

| Mood | Instrumentos |
|------|-------------|
| archive | choir + glass + low strings |
| forge | brass + low percussion + fire |
| garden | high strings + water + bioluminescent bells |
| market | pulses + chatter-like granular + neon |
| ruin | drone + reversed bell + missing signal |
| gate_review | suspended harmony |
| gate_block | dissonant hit |

## MotifGenerator

- Genera motivos desde seeds con RNG determinista
- **MoodScales**: escalas por mood (menor, pentatónica, lidia, frigia, etc.)
- **RoleMotifs**: guard, merchant, scholar, mystic, rogue, elder
- **EmotionalMotifs**: calm, alert, agitated, fearful, curious, hostile, mystical
- **FibMotif**: usa φ para generar intervalos

## HarmonyEngine

- Progresiones por mood desde círculo de quintas
- **Calm**: quintas, octavas, cuartas abiertas
- **Tension**: menores, tritonos, clusters
- Resolución de tensión a acordes estables

## TensionEngine

- Tensión derivada de R (residuo) y Phi_eff
- Interpolación suave con damping
- Config de intervalos seguros por nivel de tensión
