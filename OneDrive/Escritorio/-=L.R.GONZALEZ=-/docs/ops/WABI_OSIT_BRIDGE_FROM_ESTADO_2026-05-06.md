# Wabi OSIT Bridge From ESTADO - 2026-05-06

## Fuente

- Ruta: `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria\ESTADO.txt`
- Archivo Frio: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06\369DCD91A9BB70DC_estado.txt`
- SHA256: `369DCD91A9BB70DC6D5509F02C2FD9D481CA2893C504435C5ADBAB17BB0882DE`
- Tamano: `253472` bytes
- Intake: `docs/intake/lobby_alejandria_estado_2026-05-06_FICHAS.md`
- Estado PSI: `INFERENCIA`
- Decision: absorber patrones operativos; no importar texto bruto al runtime.

## Lectura operativa

`ESTADO.txt` refuerza una arquitectura bridge-first para Wabi-Sabi:

```text
RuntimeAdapter -> ModelRegistry -> TaskRouter -> ActionGate
              -> ToolBroker/MemoryBroker -> WitnessLog -> Evaluator -> HandoffManager
```

La aplicacion inmediata no es entrenar pesos ni crear aliases Ollama. La
aplicacion segura es convertir el puente en contratos locales pequenos,
verificables y reemplazables.

## CERTEZA

- Ollama queda como backend opcional, no como arquitectura.
- Tareas deterministicas deben resolverse sin LLM.
- `qwen2.5:0.5b` sirve como candidato de triage barato, no como juez final.
- `qwen2.5-coder:3b` sirve como candidato tecnico para codigo/arquitectura.
- ActionGate debe bloquear publicacion, secretos, acciones externas, borrado
  destructivo, entrenamiento, LoRA, aliases y descargas de modelos.
- WitnessLog debe ser append-only con hash-chain local.
- R/Residuo debe ser computable y falsable, aunque sea proxy inicial.

## INFERENCIA

- El puente OSIT puede integrarse en `apps/local/wabi-sabi` sin crear otro
  silo.
- `ResidueMeter` debe empezar como proxy simple y despues calibrarse contra
  errores reales: retries, contradicciones, REVIEW/BLOCK y fallos de tests.
- `RuntimeAdapter` debe poder cambiar de `deterministic_no_llm` a `ollama`,
  `llama.cpp` u otro backend sin cambiar ActionGate ni WitnessLog.

## INCOGNITA

- Benchmarks reales de qwen local contra tareas del sistema.
- Calidad real de GGUF/llama.cpp en esta maquina.
- Umbrales definitivos de R y Phi_eff.
- Dataset limpio para cualquier ajuste futuro.

## BLOQUEADO

- Fine-tuning, LoRA, pruning, distillation o cambio de pesos.
- Alias Ollama nuevos.
- Descarga de modelos.
- Escalacion externa con material privado.
- Publicacion de claims fuertes o arquitectura privada completa.

## Implementacion aplicada

- `apps/local/wabi-sabi/wabi_sabi/core/bridge.py`
  - `TaskEnvelope`
  - `RouteDecision`
  - `BridgeResult`
  - `ResidueMeter`
  - `BridgeActionGate`
  - `ModelRegistry`
  - `RuntimeAdapter`
  - `NoLLMAdapter`
  - `WitnessLog`
  - `BridgeExecutor`
- `apps/local/wabi-sabi/wabi_sabi/cli/main.py`
  - Subcomandos: `bridge`, `bridge-plan`, `osit`
- `apps/local/wabi-sabi/tests/test_bridge.py`
  - Routing deterministico sin LLM.
  - Bloqueo de mutacion externa/modelos.
  - Ruta qwen coder para tareas tecnicas.
  - Ruta qwen pequena para triage.
  - Evidencia requerida cuando falta fuente.
  - Deteccion de tampering en WitnessLog.

## Falsadores

- `ResidueMeter` no predice errores/retries/reviews en logs reales.
- Una tarea bloqueada llama al runtime.
- Una accion externa queda en `APPROVE`.
- Un evento WitnessLog modificado pasa `verify_chain`.
- El adapter depende de Ollama para tareas deterministicas.
- El CLI filtra rutas privadas, secretos o texto bruto del source.

## Handoff

Fingerprint: `WABI_OSIT_BRIDGE_ESTADO_2026_05_06_369DCD91`

Brief:

- ESTADO fue registrado como fuente de Lobby.
- La parte aplicable se implemento como puente local, no como entrenamiento.
- El siguiente paso tecnico es conectar este `BridgeExecutor` con COMMS /
  Mission Control y calibrar R con eventos reales de fallo o revision.
