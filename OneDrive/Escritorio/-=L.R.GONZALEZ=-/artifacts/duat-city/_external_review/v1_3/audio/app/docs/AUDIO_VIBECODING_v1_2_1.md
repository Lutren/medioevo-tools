# Audio Vibecoding v1.2.1

**Fingerprint:** DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC

## Parser Determinista

El vibecoding de audio usa un parser determinista basado en reglas.
No usa IA externa ni cloud.

## Frases Soportadas

### Volumen
- "hazlo mas silencioso" / "menos volumen" / "bajar"
- "mas fuerte" / "mas volumen" / "subir"

### Estilo
- "mas orquestal" / "orquesta" / "sinfonico"
- "mas ritual" / "ritual" / "sagrado" / "ceremonial"
- "mas tension" / "tenso" / "suspenso" / "dramatico"

### Elementos
- "mas lluvia" / "lluvia" / "agua"
- "mas fuego" / "fuego" / "calor"
- "mas archivo prohibido" / "archivo" / "biblioteca"
- "mas mercado subterraneo" / "mercado" / "bazaar"
- "mas jardin bioluminiscente" / "jardin" / "bioluminiscente"

### Balance
- "menos musica, mas ambiente"
- "mas musica, menos ambiente"

### Estilos Artisticos
- "mas Vermeer silencioso" / "Vermeer"
- "mas Caravaggio dramatico" / "Caravaggio"
- "mas van Eyck detallado" / "van Eyck"

## Output

El parser genera un `AudioSceneConfig`:
- instruments[]
- ambience[]
- sfxDensity (0-1)
- musicTension (0-1)
- reverbProfile
- mixLevels por bus
- proceduralSeed
- mood
