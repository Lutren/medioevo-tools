# Uso de Wabi Sabi CLI

## Comandos principales

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "revisa este proyecto y dime que falla"
.\wabi.cmd "arregla los tests"
.\wabi.cmd "crea un README para este modulo"
.\wabi.cmd "ejecuta diagnostico"
.\wabi.cmd chat "hola wabi, dime que puedes hacer localmente"
.\wabi.cmd codex-status
.\wabi.cmd codex "habla conmigo desde Codex a traves de Wabi-Sabi"
.\wabi.cmd codex "prepara respuesta sin ejecutar modelo" --dry-run
.\wabi.cmd agents
.\wabi.cmd logs
.\wabi.cmd e2e-smoke
```

## Programar con parche acotado

```powershell
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas" --apply --target helpers.py --json
```

Reglas del modo `--apply`:

- `--target` debe ser un `.py` dentro de `--workspace`.
- No escribe en `.git`, `.env`, `runtime`, `node_modules`, builds, releases,
  TCG, game bridge ni rutas fuera del workspace.
- Si el archivo existia, deja backup en `runtime/backups`.
- Siempre escribe un diff en `runtime/outputs`.
- Verifica sintaxis con `py_compile`.

## Instalacion editable

```powershell
python -m pip install -e . --no-deps --no-build-isolation
wabi "ejecuta diagnostico"
```

## Modo interactivo

```powershell
.\wabi.cmd
```

Luego escribir pedidos en lenguaje natural. Salir con `/exit`.

Tambien puedes usar el alias explicito:

```powershell
.\wabi.cmd chat
```

## Usar Codex a traves de Wabi-Sabi

```powershell
.\wabi.cmd codex-status --json
.\wabi.cmd codex "responde en tres lineas que pruebas correrias" --json
```

Reglas del puente:

- Por defecto usa `codex exec` si el comando `codex` esta instalado.
- Codex se invoca con `--sandbox read-only`, `--ephemeral` y
  `--ask-for-approval never`.
- Si no hay Codex CLI y existe `OPENAI_API_KEY`, usa OpenAI Responses API.
- `WABI_OPENAI_MODEL` permite cambiar el modelo; el default es `gpt-5.5`.
- `--dry-run` no llama a ningun modelo: escribe un workpack en
  `runtime/outputs`.
- Prompts con publicacion, secretos o borrado destructivo quedan en `BLOCK`.

## Rutas de evidencia

- Artefactos: `runtime/outputs`
- Logs: `runtime/logs/wabi_events.jsonl`
- Memoria local: `runtime/memory/session_memory.jsonl`

## Fronteras

Wabi Sabi local no ejecuta acciones externas, no publica, no usa secretos y no
borra archivos. Si detecta una solicitud de riesgo, devuelve `BLOCK`.
