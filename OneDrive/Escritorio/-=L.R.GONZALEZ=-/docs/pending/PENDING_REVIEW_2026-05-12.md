# Pending Review - 2026-05-12

Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.

## Counts

- Active markdown raw open items: `50`.
- Active markdown deduplicated open items: `50`.
- Claudio `PENDIENTES_MASTER.md` raw open items: `0`.
- Claudio deduplicated open items: `0`.

## Active Markdown By Priority

| priority | dedup_count |
| --- | --- |
| P0 | 3 |
| P1 | 22 |
| P2 | 6 |
| P3 | 1 |
| UNCLASSIFIED | 18 |

## Active Markdown By Lane

| lane | dedup_count |
| --- | --- |
| cleanup_migration | 6 |
| general | 31 |
| research_claims | 3 |
| runtime_claudio | 9 |
| wave_fc | 1 |

## Active Markdown By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 13 |
| host_or_heavy | 7 |
| legal_or_human | 2 |
| local_candidate | 25 |
| private_boundary | 3 |

## Claudio Master By Priority

| priority | dedup_count |
| --- | --- |

## Claudio Master By Blocker

| blocker | dedup_count |
| --- | --- |

## Top Items

| priority | lane | blocker | item | first evidence | occurrences |
| --- | --- | --- | --- | --- | --- |
| P0 | cleanup_migration | private_boundary | Secret P0: confirmar rotacion/vigencia de las credenciales en `banananana.txt` antes de cualquier limpieza o uso real. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:103 | 1 |
| P0 | general | external_or_gated | Wabi P0: antes de uso real sostenido, confirmar costo/cuota de la cuenta NVIDIA y si `ultra` requiere permiso/model access adicional. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:120 | 1 |
| P0 | general | external_or_gated | Wabi P0: conseguir/registrar sólo presencia redactada de `DASHSCOPE_API_KEY` o `QWEN_API_KEY` para activar Qwen; no usar AccessKey Alibaba como bearer. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:121 | 1 |
| P1 | cleanup_migration | local_candidate | P1 Migrar `ack/resolve/block` legacy a eventos derivados append-only. | MEDIOEVO_LIVE_TREE/TASKS.md:23 | 1 |
| P1 | cleanup_migration | local_candidate | Formal P1: hacer archive-intake cuarentenado de `medioevo_info_chemistry_v0_2.zip` y `medioevo_prompt_compression_experiment_bundle.zip`. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:60 | 1 |
| P1 | general | local_candidate | P1 Crear replay test: export JSONL -> import JSONL -> `verifyLog().ok === true`. | MEDIOEVO_LIVE_TREE/TASKS.md:22 | 1 |
| P1 | general | local_candidate | P1 Crear MCP read-only local para `medioevo://messagebus/*`. | MEDIOEVO_LIVE_TREE/TASKS.md:24 | 1 |
| P1 | general | local_candidate | P1 Crear Agent Bridge / A2A local adapter sobre MCP read-only. | MEDIOEVO_LIVE_TREE/TASKS.md:43 | 1 |
| P1 | general | local_candidate | P1 Simular handoff local entre agentes sin escritura remota. | MEDIOEVO_LIVE_TREE/TASKS.md:45 | 1 |
| P1 | general | local_candidate | P1 Agregar smoke `messagebus:a2a:smoke`. | MEDIOEVO_LIVE_TREE/TASKS.md:46 | 1 |
| P1 | general | local_candidate | P1 Verificar que `messagebus:mcp:smoke`, `npm test`, `npx tsc -b` y `npm run build` siguen pasando. | MEDIOEVO_LIVE_TREE/TASKS.md:47 | 1 |
| P1 | general | local_candidate | P1 Simular aprobacion/rechazo del operador. | MEDIOEVO_LIVE_TREE/TASKS.md:59 | 1 |
| P1 | general | local_candidate | Formal P1: comparar `medioevo_agent_core.py`, `medioevo_core_v01.py`, `Completar04-07.txt` y `PR11.txt` contra contratos Wabi/Sabi antes de cualquier import. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:59 | 1 |
| P1 | general | local_candidate | Wabi P1: crear fixture de evaluacion observacionista para comparar respuesta local, dry-run y cloud mock. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:100 | 1 |
| P1 | research_claims | local_candidate | Formal P1: comparar `report.md`, `Auto.txt`, `BIBLIA_MEDIOEVO_Canon_Unificado.pdf`, `OI_P6R_paper_v0_1.md` y `paper_observacionismo_inverso.md` contra documentos 00-22 y `16_CLAIMS_REGISTER.md`. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:58 | 1 |
| P1 | research_claims | local_candidate | Formal P1: hacer QA visual solo de PDF/PNG que sustenten claims o figuras necesarias. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:61 | 1 |
| P1 | runtime_claudio | local_candidate | Claudio P1: conectar una llamada interna de lectura al gateway solo donde no duplique `model_router.py`. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:101 | 1 |
| P1 | runtime_claudio | local_candidate | Claudio P1: convertir `medioevo_agent_core.py` y `medioevo_core_v01.py` en contratos/tests pequeños antes de importar lógica. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:122 | 1 |
| P1 | cleanup_migration | host_or_heavy | P1 Crear adaptador JSONL local en disco para `appendOnlyLog`. | MEDIOEVO_LIVE_TREE/TASKS.md:21 | 1 |
| P1 | general | host_or_heavy | P1 Crear agent cards locales: Codex Agent, Publisher Agent, Canon Auditor Agent, Security Gate Agent, UI Agent. | MEDIOEVO_LIVE_TREE/TASKS.md:44 | 1 |
| P1 | general | legal_or_human | P1 Crear proposals firmadas: `append_message`, `create_task`, `update_handoff`, `publish_release`. | MEDIOEVO_LIVE_TREE/TASKS.md:58 | 1 |
| P1 | general | private_boundary | Wabi P1: decidir si existe key Qwen/DashScope real; `banananana.txt` mostro senal Aliyun AccessKey pero no una key DashScope/Qwen especifica; si existe, registrarla solo como presencia redactada, nunca como valor. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:99 | 1 |
| P1 | runtime_claudio | external_or_gated | P1 Crear ActionGate write proposal layer. | MEDIOEVO_LIVE_TREE/TASKS.md:57 | 1 |
| P1 | runtime_claudio | host_or_heavy | Wabi P1: probar tarea real sin Ollama usando `WABI_DISABLE_BASE_MODEL=1` y verificar fallback `codex/dry-run` sin escritura peligrosa. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:98 | 1 |
| P1 | wave_fc | host_or_heavy | Formal P1: comparar los dos Python de `Formal` contra `wabi_sabi/core/gate.py`, `safe_executor.py`, `rollback_store.py`, `decision_log.py` y `eml.py`. | MEDIOEVO_OBSERVACIONISMO_MASTER/PENDIENTES_DE_INPUT.md:102 | 1 |

## Kairos Fastlane

- Path: `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/observacionista/kairos_attention_hygiene/pendientes_fastlane_2026-05-01.json`.
- Generated at: `2026-05-01T00:08:52+00:00`.
- Stale against this snapshot date: `True`.
- Decision count: `478`.

| action | count |
| --- | --- |
| defer | 325 |
| hold_calibration | 103 |
| queue_next | 50 |

## Operational Rule

At the start of each run/day execute `python tools\release\pending_review.py --write --quiet`, then choose work from shortest verified local closure first. External/publication tasks stay blocked until their specific gate is clean.
