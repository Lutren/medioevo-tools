# 12 — MÓDULOS TÉCNICOS
**Estado:** R≈0.20 | Especificaciones implementables | Gate: test antes de deploy

---

## state_estimator

**Propósito:** Estimar R, Φ_eff y régimen del procesador/agente actual.

| Campo | Valor |
|---|---|
| Input | history: List[str], pending_tasks: int, corrections: int, tasks_closed: int, tokens_consumed: int |
| Output | {R_est: float, Phi_eff: float, regime: str, action_allowed: bool} |
| Dependencias | Ninguna externa |
| Métrica de éxito | R=0 cuando pending=0, corrections=0; régimen ÓPTIMO cuando R<0.15 y Φ>0.75 |
| Prueba mínima | `estimate_R([], 0, 0) == 0.0`; `classify_regime(0.1, 0.8) == "OPTIMO"` |

---

## action_gate

**Propósito:** Compuerta que aprueba/revisa/bloquea acciones basándose en confianza, R y evidencia.

| Campo | Valor |
|---|---|
| Input | {confidence: float, R_est: float, Phi_eff: float, risk_level: str, evidence_count: int} |
| Output | {decision: APPROVE\|APPROVE_MONITORED\|REVIEW\|BLOCK, reason: str} |
| Dependencias | state_estimator |
| Métrica de éxito | Bloquea con confianza < 0.40; aprueba con confianza ≥ 0.70 AND R < 0.30 |
| Prueba mínima | risk="block" → siempre BLOCK; confidence=0.9 AND R=0.1 → APPROVE |

---

## task_decomposer

**Propósito:** Descomponer input de usuario en prompts operativos tipados para agentes.

| Campo | Valor |
|---|---|
| Input | user_input: str, oso_state: dict |
| Output | {task_type: str, target_agent: str, context: dict, action_gate: str, timeout_ms: int} |
| Dependencias | agent_registry |
| Métrica de éxito | Mismo input+estado → misma salida (determinismo); nunca usa LLM |
| Prueba mínima | Entrada vacía devuelve error válido; entrada conocida devuelve target_agent correcto |

---

## witness_log

**Propósito:** Registro inmutable de evidencia de decisiones, ejecuciones y cambios.

| Campo | Valor |
|---|---|
| Input | {agent_id, task_id, action, result, R_before, R_after, timestamp} |
| Output | log_entry con hash |
| Dependencias | ninguna externa |
| Métrica de éxito | append-only; hash verifica integridad; no permite sobrescritura |
| Prueba mínima | intentar sobrescribir entrada → error; hash(entry) == hash(re-read(entry)) |

---

## handoff_generator

**Propósito:** Producir paquete mínimo de continuidad entre sesiones.

| Campo | Valor |
|---|---|
| Input | state: dict, brief: str, next_action: str |
| Output | {fingerprint: str, brief: str, next_action: str, timestamp: str} |
| Dependencias | ninguna externa |
| Métrica de éxito | fingerprint SHA256 determinístico; mismo estado → mismo fingerprint |
| Prueba mínima | `emit_handoff(state, "", "") .fingerprint == emit_handoff(state, "", "").fingerprint` |

---

## ghost_gate

**Propósito:** Simular acción antes de ejecutarla (no modifica estado real).

| Campo | Valor |
|---|---|
| Input | proposed_action: dict, current_state: dict |
| Output | {simulated_result: dict, risk_estimate: float, proceed: bool, reason: str} |
| Dependencias | rollback_store (read-only), state_estimator |
| Métrica de éxito | ejecutar ghost_gate no modifica estado externo; proceed=false si risk>threshold |
| Prueba mínima | estado antes == estado después de ejecutar ghost_gate |

---

## context_compactor

**Propósito:** Reducir contexto cargado sin perder información crítica (combate J_c).

| Campo | Valor |
|---|---|
| Input | full_context: List[str], max_tokens: int, priority_artifacts: List[str] |
| Output | compacted_context: List[str], dropped_count: int, preserved_ids: List[str] |
| Dependencias | evidence_tracker |
| Métrica de éxito | len(compacted) ≤ max_tokens; priority_artifacts siempre incluidos |
| Prueba mínima | compactar con priority=[A,B] → A,B siempre en output |

---

## evidence_tracker

**Propósito:** Trackear evidencia disponible por claim y determinar su estado epistémico.

| Campo | Valor |
|---|---|
| Input | claim: str, evidence: List[dict], domain: str |
| Output | {claim_id, status, evidence_count, confidence, missing, falsifier} |
| Dependencias | claim_classifier |
| Métrica de éxito | claim sin evidencia → confidence = 0.0; claim con evidencia externa verificada → FORMAL_HYPOTHESIS |
| Prueba mínima | evidencia vacía → status = RESEARCH_ONLY; evidencia verificada ≥ 3 → FORMAL_HYPOTHESIS |

---

## claim_classifier

**Propósito:** Clasificar claims para publicación según nivel de evidencia y riesgo.

| Campo | Valor |
|---|---|
| Input | claim: str, domain: str, evidence_count: int, has_numeric: bool, risk_level: str |
| Output | gate: str, rationale: str |
| Dependencias | ninguna externa |
| Métrica de éxito | claim físico sin numérico → NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC; claim operativo verificado → PUBLISH_AS_MODEL |
| Prueba mínima | physics + has_numeric=False → bloqueado; operational + has_numeric=True + risk=low → permitido |

---

## rollback_store

**Propósito:** Almacenar snapshots de estado para permitir reversión.

| Campo | Valor |
|---|---|
| Input | state: dict (para save); snapshot_id: str (para restore) |
| Output | snapshot_id: str (save); state: dict (restore) |
| Dependencias | ninguna |
| Métrica de éxito | restore(save(state)) == state |
| Prueba mínima | save → restore → estado idéntico; restore de id inválido → error claro |

---

## agent_registry

**Propósito:** Registro de agentes disponibles, sus capacidades y estado.

| Campo | Valor |
|---|---|
| Input | query: {task_type, required_tools, domain} |
| Output | List[{agent_id, capabilities, status, current_load}] |
| Dependencias | state_estimator por agente |
| Métrica de éxito | devuelve agentes con herramientas requeridas; filtra agentes en JAMMING |
| Prueba mínima | query con herramienta X → solo agentes que tienen X; agente en JAMMING → no incluido |

---

## observation_envelope

**Propósito:** Encapsular una observación con metadatos trazables (fuente, R al momento, riesgo).

| Campo | Valor |
|---|---|
| Input | stimulus: Any, source: str, R_at_capture: float, evidence: str, risk: float |
| Output | ObservationEnvelope serializable |
| Dependencias | ninguna |
| Métrica de éxito | siempre incluye timestamp y R_at_capture; serializable a JSON |
| Prueba mínima | crear envelope → serializar → deserializar → datos idénticos |

---

## Handoff
`MODULOS_TECNICOS_v1.0|10-modules-specified|contracts-tests|2026-05-07`


---

## Módulos adicionales detectados en fuentes

| Módulo | Propósito | Input | Output | Prueba mínima |
|---|---|---|---|---|
| `dsl_compiler` | Compilar Observacionista DSL a JSON/gate payload | `.dsl` text | JSON contract | DSL válido genera `intent`, `actions`, `witness`; DSL sin evidencia falla |
| `model_efficiency_gate` | Medir si un modelo reducido puede reemplazar baseline | baseline + candidate metrics | allow/ask/block | `accuracy_drop > 0.02` bloquea |
| `module_manifest_validator` | Validar contrato mínimo de módulos Brain OS | manifest JSON | valid/errors | falta `witness` o `recovery` falla |
| `content_forge_job_gate` | Gatear renders locales y paquetes de publicación | job spec + assets | job state + QA | job sin assets public-safe queda `requiere_aprobacion` |
| `browser_manifest_gate` | Bloquear automatización sin manifiesto | browser action | allow/block | acción externa sin manifest bloquea |
| `curator_order_assistant` | Mantener orden y enseñar higiene documental al operador/agentes | cambios, fuentes, tareas | fichas, rutas, warnings | fuente cruda sin ficha queda REVIEW |

---

## Corte de curaduría 2026-05-07

CERTEZA:
- Este documento fue compilado desde fuentes locales de `-=PSI=-`, `-=CEREBRO=-` y `PRODUCTOS_MEDIOEVO`.
- Las fuentes originales no fueron movidas, borradas ni reescritas.

INFERENCIA:
- Si una idea aparece en varias fuentes, se conserva aquí como una entrada consolidada y se remite al manifiesto de fuentes para variaciones.

INCÓGNITA:
- PDFs, DOCX, ZIP, TAR.GZ y media quedan trazados por manifiesto; no todos fueron convertidos a texto completo en este pase.

ACCIÓN:
- Usar este archivo como capa maestra de lectura y volver a la fuente solo para auditoría, expansión o verificación puntual.

ARTEFACTO:
- Archivo maestro: `12_MODULOS_TECNICOS.md`.
