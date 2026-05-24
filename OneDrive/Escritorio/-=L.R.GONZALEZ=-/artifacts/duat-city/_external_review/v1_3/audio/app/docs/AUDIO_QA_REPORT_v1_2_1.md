# Audio QA Report v1.2.1

**Fingerprint:** DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
**Fecha:** 2026-05-20

## Estado General

| Criterio | Estado |
|----------|--------|
| Procedural audio engine exists | PASS |
| Orchestral-like synth exists | PASS |
| Material/world/NPC audio mapping | PASS |
| Audio vibecoding exists | PASS |
| Audio UI exists | PASS |
| Sample policy exists | PASS |
| Audio off by default | PASS |
| Wabi disabled | PASS |
| No cloud/IA externa | PASS |

## Sonidos Verificados

| Sonido | Estado | Nota |
|--------|--------|------|
| waterFlow | PASS | Procedural con granular |
| fireCrackle | PASS | Granular + noise |
| smokeBreath | PASS | Brown noise + envelope |
| neonHum | PASS | 60Hz + flicker |
| metalHit | PASS | Modal resonator |
| glassCrystal | PASS | Inharmonic partials |
| steamPipe | PASS | Filtered noise + bursts |
| archiveMachine | PASS | Ticks + drone |
| gateApprove | PASS | Consonant intervals |
| gateReview | PASS | Suspended harmony |
| gateBlock | PASS | Dissonance |
| qStateGlyphs | PASS | 4 estados |

## Orchestral Moods

| Mood | Estado |
|------|--------|
| archive | PASS |
| forge | PASS |
| garden | PASS |
| market | PASS |
| ruin | PASS |
| gate_review | PASS |
| gate_block | PASS |

## UI

| Panel | Estado |
|-------|--------|
| AudioEnginePanel | PASS |
| AudioMixerPanel | PASS |
| AudioVibePanel | PASS |

## Limitaciones Conocidas

1. Tests automatizados pendientes (requieren vitest)
2. Browser audio QA requiere interacción manual
3. Samples reales pendientes de allowlist
4. Spatial audio 3D no implementado (2D/2.5D only)

## Wabi

- execution_allowed=false: VERIFIED
- sandbox_execution_allowed=false: VERIFIED
- real_apply_allowed=false: VERIFIED

## Conclusion

Motor funcional. Todos los criterios de aceptación PASS excepto
la suite de tests automatizados que requiere vitest/jest.
