# Codex Changelog v1.2.1

**Fingerprint:** DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC

## Cambios Realizados

### Fase 0 — Baseline
- [x] Inicializado proyecto React + TypeScript + Vite + Tailwind
- [x] Estructura de directorios creada

### Fase 1 — Audio Core
- [x] audioTypes.ts — Tipos fundamentales
- [x] audioEngine.ts — Motor principal con voice pool
- [x] audioGraph.ts — Grafo de nodos WebAudio
- [x] audioClock.ts — Reloj con Quaternary Timing
- [x] audioMixer.ts — Mezclador multi-bus
- [x] audioBus.ts — Buses con compresor
- [x] audioMetrics.ts — R_audio, Phi_audio

### Fase 2 — Procedural Synthesis
- [x] oscillators.ts — Osciladores con Fib detuning
- [x] envelopes.ts — ADSR con presets
- [x] filters.ts — Biquad + formantes vocálicas
- [x] noise.ts — White/pink/brown/blue/violet
- [x] modalResonator.ts — Resonancia por material
- [x] granular.ts — Grains, crackle, bubbles, steam
- [x] fm.ts — FM synthesis para bronces/campanas
- [x] additive.ts — Cuerdas, coro, drones
- [x] reverb.ts — Schroeder-like multi-tap
- [x] spatial.ts — Audio 2D/2.5D
- [x] 12 sonidos base del mundo DUAT

### Fase 3 — Orchestral Engine
- [x] syntheticStrings.ts — Low drone + high shimmer
- [x] syntheticBrass.ts — Swell + staccato + ritual horn
- [x] syntheticChoir.ts — Pad + drone + breath
- [x] syntheticPercussion.ts — Timpani + bell + bowed metal
- [x] motifGenerator.ts — Motivos procedurales
- [x] harmonyEngine.ts — Progresiones armónicas
- [x] tensionEngine.ts — Motor de tensión

### Fase 4 — World State Adapters
- [x] worldAudioAdapter.ts — Adapter principal
- [x] materialAudio.ts — Mapeo materiales
- [x] lightAudio.ts — Mapeo luz
- [x] npcAudio.ts — Audio para NPCs
- [x] eventAudio.ts — Eventos del mundo
- [x] ositAudio.ts — Métricas OSIT

### Fase 5 — Spatial Audio
- [x] spatialAudio.ts — Posicionalización 2D
- [x] Reverb profiles por ubicación

### Fase 6 — Audio Vibecoding
- [x] audioVibeParser.ts — Parser determinista

### Fase 7 — Sample Library
- [x] sampleTypes.ts — Tipos
- [x] sampleRegistry.ts — Registro con allowlist
- [x] sampleManifest.ts — Manifest
- [x] sampleLoader.ts — Cargador

### Fase 8 — UI
- [x] AudioEnginePanel.tsx — Panel principal
- [x] AudioMixerPanel.tsx — Mixer multi-bus
- [x] AudioVibePanel.tsx — Vibecoding

### Fase 9 — RPG Export
- [x] audioTypes.ts — RPGAudioProfile

### Fase 13 — Docs
- [x] PROCEDURAL_AUDIO_ENGINE_v1_2_1.md
- [x] ORCHESTRAL_SYNTH_ENGINE_v1_2_1.md
- [x] AUDIO_VIBECODING_v1_2_1.md
- [x] AUDIO_LIBRARY_POLICY_v1_2_1.md
- [x] CODEX_CHANGELOG_v1_2_1.md

## No Implementado (Fase 10-12)
- Tests automatizados (requieren vitest/jest setup)
- QA report final (requiere validación manual)

## Wabi Status
- execution_allowed=false
- sandbox_execution_allowed=false
- real_apply_allowed=false
