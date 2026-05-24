# AUDIO GAME-FEEL ADAPTER v1.3.1

Fingerprint: DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY

## Estado

Implementado adaptador local determinista para audio y game-feel. El sistema no usa muestras externas, no llama a IA, no usa nube y permanece apagado hasta gesto local del usuario.

## Componentes

- `src/audio/audioTypes.ts`: contratos de cues, snapshot, benchmark y manifest.
- `src/audio/audioEventMapper.ts`: mapea materiales, luces, agentes, lenguaje, gates y cosmologia interna a cues.
- `src/audio/proceduralSynth.ts`: genera planes WebAudio deterministas y los ejecuta solo tras `Enable`.
- `src/audio/gameFeelAdapter.ts`: snapshot con `R_audio`, `Phi_audio`, pulse, shake y frontera.
- `src/audio/worldAudioAdapter.ts`: adaptador UI/runtime off-by-default.
- `src/audio/audioBenchmark.ts`: benchmark puro de mapping, sin AudioContext.
- `src/components/AudioGameFeelPanel.tsx`: panel operativo con Enable, Preview, gain y cues.

## Frontera

- Audio procedural local, no samples.
- No cloud, no API externa, no IA.
- `publicationAllowed=false`.
- `externalSamplesCopied=false`.
- Wabi execution sigue false.
- La cosmologia se usa solo como `IN_WORLD_COSMOLOGY`, no como claim cientifico.

## Integraciones

- GameState: `audioGameFeel`.
- Brain Runtime: sistema `audioGameFeel`.
- Handoff: bloque `audio_gamefeel`.
- RPG export v3: `audio_gamefeel_profile`.
- Pixel/Light: cues desde materiales, luces, reflectancia, fuego, humo y neon.
