# Wabi Sabi Local Agents

CLI local-first para hablar con Wabi Sabi y enrutar tareas simples hacia
agentes verificables. No requiere nube ni claves. Si no hay modelo local, usa
fallback determinista basado en reglas, artefactos y logs.

## Uso rapido

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "ejecuta diagnostico"
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas" --apply --target helpers.py
.\wabi.cmd
.\wabi.cmd chat "hola wabi, resume el estado local"
.\wabi.cmd codex-status
.\wabi.cmd codex "responde como Codex desde Wabi-Sabi: que pruebas debo correr?"
.\wabi.cmd codex "genera workpack sin llamar modelo" --dry-run
.\wabi.cmd bridge-plan "clasifica pendientes y genera resumen"
.\wabi.cmd agents
.\wabi.cmd e2e-smoke
```

## Instalacion editable opcional

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
python -m pip install -e . --no-deps --no-build-isolation
wabi "crea un README para este modulo"
```

## Seguridad

- No hace push, deploy, publicacion, compras, borrados destructivos ni uso de
  secretos.
- Las escrituras automaticas van a `runtime/outputs` y los logs a
  `runtime/logs`.
- `wabi codex` ejecuta Codex CLI en modo `read-only` cuando esta instalado. Si
  no existe CLI, puede usar OpenAI Responses API con `OPENAI_API_KEY`; sin
  proveedor disponible genera un workpack local con `--dry-run`.
- El modo `--apply --target <archivo.py>` puede escribir codigo Python dentro
  del workspace con diff, backup si habia contenido previo y `py_compile`.
- Las acciones riesgosas quedan en `BLOCK` o `REVIEW` con explicacion.
- El puente OSIT registra decisiones en SQLite con hash-chain y no llama modelos
  para tareas deterministicas.

Ver tambien:

- `docs/USAGE.md`
- `docs/ARCHITECTURE.md`
- `REPORT_WABI_SABI_LOCAL_AGENTS.md`
