# voice/ — ElevenLabs TTS Bridge para MEDIOEVO

Puente de texto-a-voz para narración de MEDIOEVO. Usa la API de ElevenLabs
con un sistema de cola JSONL y un informe de resultados.

## Uso

```bash
# Dry-run (sin llamadas reales):
python elevenlabs_voice_bridge.py --queue path/to/queue.jsonl

# Ejecutar síntesis real:
ELEVENLABS_API_KEY=tu_key python elevenlabs_voice_bridge.py --execute --limit 5
```

## Formato de la cola (JSONL)

```json
{"id": "narr_001", "speaker": "leonardo", "elevenlabs_voice_id": "VOICE_ID", "text": "Texto a narrar.", "output_res_path": "res://audio/narration/narr_001.mp3"}
```

- `voice_id` pendiente o vacío: la entrada se omite (dry-run seguro)
- `output_res_path`: ruta Godot `res://` que se convierte a ruta local

## Requerimientos

- Python 3.10+ (stdlib únicamente: urllib, json, pathlib)
- `ELEVENLABS_API_KEY` o `ELEVEN_LABS_API_KEY` en entorno
- Cuenta ElevenLabs con créditos

## Estado

| ítem | estado |
|------|--------|
| Código | CERTEZA (copiado de E:\Medioevo_RPG\tools\production\ 2026-06-14) |
| API online | BLOQUEADO_CLAVE (requiere ELEVENLABS_API_KEY en .env) |
| Prueba real | BLOQUEADO_PUBLICATIONGATE (no se prueba sin clave activa) |
