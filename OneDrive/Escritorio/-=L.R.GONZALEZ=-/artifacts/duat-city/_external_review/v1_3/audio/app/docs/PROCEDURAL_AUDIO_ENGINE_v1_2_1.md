# Procedural Audio Engine v1.2.1

**Fingerprint:** DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
**Estado:** INTERNO_LOCAL — NO_PUBLICAR_SIN_GATE
**Wabi:** execution_allowed=false

## Arquitectura

```
evento del mundo
  -> material / luz / NPC / clima / gate / OSIT
  -> physics/pixel cell adapter
  -> agente/NPC state
  -> emocion/estado OSIT (R/Phi_eff)
  -> formula sonora procedural
  -> sintesis (osciladores, ruido, FM, granular, modal)
  -> mezcla espacial (pan, attenuation, occlusion, reverb)
  -> salida WebAudio API
```

## Stack Tecnico

- React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- WebAudio API (sin librerias externas)
- Motor 100% procedural — no depende de samples WAV
- CPU-first — optimizado para hardware limitado

## Sonidos Base (12)

1. **waterFlow** — noise filtrado + burbujeo granular
2. **fireCrackle** — pink/brown noise + impulses granulares
3. **smokeBreath** — low-pass noise + envelope lento
4. **neonHum** — 60Hz hum + armónicos + flicker
5. **metalHit** — modal resonator con parciales metálicos
6. **glassCrystal** — parciales inarmónicos + decay largo
7. **steamPipe** — filtered noise + pressure bursts
8. **archiveMachine** — ticks + servo + low drone
9. **gateApprove** — intervalo consonante / campana verde
10. **gateReview** — intervalo suspendido / tensión ámbar
11. **gateBlock** — golpe grave + disonancia roja
12. **qStateGlyphs** — 00=silence, 01=glitch, 10=tono, 11=burst

## Buses de Audio

- master, music, ambience, sfx, ui, npc, material, danger
- Cada bus con compresor y EQ opcionales
- Master compressor para prevenir clipping

## Metricas

- **R_audio**: residuo del canal (0-1)
- **Phi_audio**: eficiencia de conversión (0-1)
- activeVoices, cpuEstimate, droppedVoices

## Vibecoding Soportado

- "hazlo mas silencioso" / "mas fuerte"
- "mas orquestal" / "mas ritual" / "mas tension"
- "mas lluvia" / "mas fuego"
- "mas archivo prohibido" / "mas mercado subterraneo" / "mas jardin bioluminiscente"
- "menos musica, mas ambiente"
- "mas Vermeer silencioso" / "mas Caravaggio dramatico" / "mas van Eyck detallado"

## Reglas de Seguridad

- Audio OFF por default (requiere user gesture)
- Wabi: execution_allowed=false
- No cloud / no IA externa / no publicar sin gate
- Samples: CC0 preferred, CC-BY-NC blocked
