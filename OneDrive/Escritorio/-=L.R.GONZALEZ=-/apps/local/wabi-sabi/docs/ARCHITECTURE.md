# Arquitectura Wabi Sabi Local

## Responsabilidades

```text
wabi_sabi/
  cli/
    main.py      # entrypoint, salida humana/json, modo interactivo
    parser.py    # intencion por reglas locales
    router.py    # registro y seleccion de agentes
  agents/
    base_agent.py
    programmer_agent.py
    debug_agent.py
    research_agent.py
    file_agent.py
  core/
    bridge.py   # puente OSIT: envelope, R, routing, ActionGate, WitnessLog
    codex_bridge.py # puente opcional hacia Codex CLI / OpenAI Responses
    config.py
    gate.py
    memory.py
    observation.py
    programming.py # parche Python acotado: target, backup, diff, py_compile
    tools.py
  config/
    agents.json
```

## Flujo

1. El CLI recibe texto en lenguaje natural.
2. `parser.py` clasifica intencion.
3. `gate.py` evalua riesgo local.
4. `router.py` selecciona agente desde `config/agents.json`.
5. El agente ejecuta una accion segura.
6. `memory.py` registra JSONL append-only.
7. La respuesta sale con CERTEZA / INFERENCIA / INCOGNITA.

## Puente OSIT

`core/bridge.py` es la capa bridge-first absorbida desde `ESTADO.txt`. No llama
modelos por defecto y no depende de Ollama como arquitectura. El flujo minimo es:

```text
TaskEnvelope -> ResidueMeter -> ActionGate -> ModelRegistry
             -> RuntimeAdapter -> WitnessLog
```

Modo programador con escritura:

```text
prompt -> parser -> ActionGate -> ProgrammerAgent --apply
       -> ScopedPatch -> backup/diff -> py_compile -> ObservationEnvelope
```

La escritura esta limitada a archivos `.py` dentro del workspace. Las rutas de
runtime, secretos, vendors, builds, releases, TCG/game bridge y rutas externas
se rechazan antes de escribir.

## Puente Codex

`core/codex_bridge.py` permite hablar con Codex desde Wabi-Sabi sin convertir
el CLI local en un agente externo sin control:

```text
prompt -> ActionGate -> provider auto
       -> codex-cli read-only | openai-responses | dry-run workpack
       -> runtime/logs/wabi_events.jsonl
```

Proveedor `auto`:

1. `codex-cli` si `codex` esta instalado.
2. `openai-responses` si existe `OPENAI_API_KEY`.
3. `dry-run` si no hay proveedor ejecutable.

El adaptador `codex-cli` ejecuta:

```text
codex --ask-for-approval never exec --sandbox read-only --skip-git-repo-check --ephemeral
```

Esto permite conversar o pedir analisis desde Wabi-Sabi, pero no aplica cambios
por si solo. Los cambios locales siguen pasando por `--apply` o por un gate
humano/ActionGate posterior.

Reglas actuales:

- tareas deterministicas usan `deterministic_no_llm`;
- triage bajo riesgo puede rutearse a `qwen2.5:0.5b`;
- tareas tecnicas/codigo pueden rutearse a `qwen2.5-coder:3b`;
- publicacion, secretos, acciones externas, borrado destructivo, aliases,
  descargas, LoRA o fine-tuning quedan en `BLOCK`;
- `WitnessLog` usa SQLite con hash-chain y `verify_chain()`.

## Contrato de agente

Cada agente declara:

- nombre
- descripcion
- capacidades
- limites
- entrypoint
- `safe_mode`

Entrada: `AgentInput(prompt, parsed, options)`.

Salida: `AgentResult` con `ok`, `action`, `output`, `artifacts`, `evidence`,
`certainty`, `inference`, `unknown` y `error`.

## Extension

1. Crear un nuevo archivo en `wabi_sabi/agents`.
2. Heredar de `BaseAgent`.
3. Agregar entrypoint y capacidades en `wabi_sabi/config/agents.json`.
4. Agregar ruta de intencion si corresponde.
5. Crear test focal en `tests/`.
