# Qwen Blueprint Local Index - 2026-05-06

## ESTADO

- Carril: Wabi-Sabi / Qwen observacionista.
- Gate: `REVIEW`.
- Host: `JAMMING/BLOCK`.
- Navegacion externa: bloqueada en este ciclo.
- Modelo base local: `qwen2.5-coder:3b`.
- Fallback local: `qwen2.5:0.5b`.
- Pesos/adapters/aliases: bloqueados.

## CERTEZA

Archivos locales que funcionan como blueprints operativos:

| archivo | SHA256 | uso |
|---|---|---|
| `runtime/model_router/Modelfile.qwen_observador_candidate` | `FDE8815550F8A60000F7DA5522544963C3EAE9CEF09040870FF6D34C9C47D7FA` | System prompt y parametros candidatos |
| `runtime/model_router/qwen_observacion_contract.json` | `F1FFC023972585C61699D05BCF946195658611D6CFF938228ADFE35A4FD3B4B3` | Contrato de observacion Qwen |
| `runtime/model_router/qwen_observacion_gate_report.json` | `A72BE78944A4909A906B1DD9B66A50267CF519115FC4D1F35BDB880E9EC8023F` | Gate actual Qwen |
| `runtime/model_router/qwen_health.json` | `DE2D10DDCE19EA3C1BF4EA202AD540BBF97AE7C5C4A6D314F37D2B9C9ADE3EB4` | Health de `qwen2.5-coder:3b` |
| `runtime/model_router/qwen_triage_health.json` | `2C63C689942C3609585892F007A50EC2FCE0684DF66F552F136B62B322720661` | Health de `qwen2.5:0.5b` |

## LECTURA TECNICA

- `core/model_router.py` define `QWEN_OBSERVACION_MODEL = "qwen2.5-coder:3b"`.
- La ruta `qwen_observador` usa primero `qwen2.5-coder:3b` y luego `qwen2.5:0.5b`.
- `core/qwen_observacion_engine.py` define `BASE_MODEL = "qwen2.5-coder:3b"` y `TRIAGE_MODEL = "qwen2.5:0.5b"`.
- El motor ya fuerza `think=false`, `truncate=true`, `keep_alive=0`.
- El contrato actual declara `weights_modified=false` y `adapter_training_started=false`.
- El dataset semilla marca `accepted_for_training=false` y `human_review_required=true`.

## MODFILE CANDIDATO

Parametros actuales:

- `temperature=0.1`
- `top_p=0.7`
- `top_k=32`
- `repeat_penalty=1.08`
- `num_ctx=1024`
- `num_predict=192`

Reglas de sistema ya presentes:

- No revelar pensamiento interno ni `<think>`.
- Responder con `CERTEZA`, `INFERENCIA`, `INCOGNITA`, `ACCION`.
- No inventar cierre sin evidencia.
- Bloquear externo, borrado, publicacion, finanzas, credenciales, deploy y pesos/adapters sin ActionGate.
- Reducir alcance si host o ruta estan en `REVIEW/BLOCK`.
- Aplicar metodo directo e inverso.
- Usar ObservaScript minimo: observar, documentar, verificar, actuar, handoff.

## HIPOTESIS DE MODIFICACION SEGURA

1. Crear `QwenBlueprintIndex` como solo lectura.
2. Expandir dataset semilla a 20+ pares `chosen/rejected`, sin accepted_for_training.
3. Agregar eval de formato: `CERTEZA/INFERENCIA/INCOGNITA/ACCION`.
4. Agregar eval de frontera: externo, privado, destructivo, pesos, claims fuertes.
5. Agregar eval de salida: sin `<think>`, sin absolutos, con evidencia.
6. Mantener `qwen2.5:0.5b` para triage y reset cuando host este saturado.

## BLOQUEOS

- No correr `qwen_3b_suite` con host `BLOCK`.
- No crear alias Ollama.
- No descargar ni usar modelos cloud.
- No entrenar adapters.
- No modificar pesos.
- No navegar a HuggingFace/Qwen docs hasta tener ActionGate externo o una ventana de investigacion aprobada.

## SIGUIENTE ACCION

Cuando host baje a `REVIEW` estable: crear indice automatico de hashes y contratos desde estos archivos, con test local de parseo.
