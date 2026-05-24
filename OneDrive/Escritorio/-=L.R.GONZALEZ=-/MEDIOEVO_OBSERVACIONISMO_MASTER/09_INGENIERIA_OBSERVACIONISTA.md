# 09 — INGENIERÍA OBSERVACIONISTA
**Estado:** R≈0.20 | Especificación técnica | Gate: implementable con gates

---

## Propósito

Convertir la teoría en ingeniería: módulos, contratos, métricas, validadores, pipelines, tests, agentes.

El principio de la ingeniería observacionista es que cada módulo implementa una operación del pipeline observacional: percibir → filtrar → comprimir → actualizar → actuar → registrar → cerrar.

---

## Pipeline fundamental

```
Input externo
    ↓
[Sensorium / Receptor]     → R_i(S) = ganancia × señal
    ↓
[Integrador temporal]      → ∫_{t−Δ}^{t} R_i(S) dτ
    ↓
[Compuerta atencional G_i] → filtro de relevancia
    ↓
[Compresor C_i]            → elimina redundancia, actualiza priors
    ↓
[Estimador de estado]      → R_est, Φ_eff, régimen
    ↓
[ActionGate]               → aprobar / revisar / bloquear
    ↓
[Ejecutor]                 → acción verificable
    ↓
[WitnessLog]               → evidencia
    ↓
[Handoff Generator]        → fingerprint + brief + next_action
```

---

## Módulos core implementables

### 1. `state_estimator`
- **Input:** history[], pending_tasks, corrections, tokens_consumed
- **Output:** {R_est: float, Phi_eff: float, regime: str}
- **Contrato:** R ∈ [0,1]; Phi_eff ∈ [0,1]; regime ∈ {OPTIMO, FUNCIONAL, CARGADO, PRE_JAMMING, JAMMING}
- **Test:** `estimate_R([], 0, 0) == 0.0`; `estimate_R(large_history, 10, 5) > 0.7`

### 2. `action_gate`
- **Input:** {confidence: float, R_est: float, Phi_eff: float, evidence_count: int}
- **Output:** {decision: str, reason: str}
- **Contrato:** decision ∈ {APPROVE, APPROVE_MONITORED, REVIEW, BLOCK}
- **Test:** confidence >= 0.70 AND R < 0.30 → APPROVE; confidence < 0.40 → BLOCK

### 3. `task_decomposer`
- **Input:** user_input: str, OSO.state
- **Output:** {task_type, target_agent, context, action_gate, timeout_ms}
- **Contrato:** Salida determinística para mismo input+estado; no usa LLM
- **Test:** misma entrada produce misma salida (determinismo)

### 4. `witness_log`
- **Input:** {agent_id, task_id, action, result, R_before, R_after, timestamp}
- **Output:** log entry with hash
- **Contrato:** append-only; inmutable después de escritura
- **Test:** no permite sobrescribir entrada existente

### 5. `handoff_generator`
- **Input:** state dict, brief: str, next_action: str
- **Output:** {fingerprint: str, brief: str, next_action: str}
- **Contrato:** fingerprint es SHA256 del estado serializado; determinístico
- **Test:** mismo estado → mismo fingerprint

### 6. `ghost_gate`
- **Input:** proposed_action, simulated_state
- **Output:** {simulated_result, risk_estimate, proceed: bool}
- **Contrato:** no ejecuta acción real; solo simula
- **Test:** ejecutar ghost_gate no modifica estado externo

### 7. `context_compactor`
- **Input:** full_context, max_tokens, R_threshold
- **Output:** compacted_context con artefactos relevantes
- **Contrato:** H_eff(compacted) ≥ H_eff(full) × threshold
- **Test:** compacted tiene <= max_tokens; no pierde artefactos críticos

### 8. `evidence_tracker`
- **Input:** claim, evidence[], source
- **Output:** {claim_id, status, evidence_count, confidence, gap}
- **Contrato:** status ∈ {VERIFIED, FORMAL_HYPOTHESIS, RESEARCH_ONLY, BLOCKED}
- **Test:** claim sin evidencia → confidence = 0.0

### 9. `claim_classifier`
- **Input:** claim text, evidence_count, domain, risk_level
- **Output:** publication_gate, rationale
- **Test:** claim sin evidencia numérica en física → NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC

### 10. `rollback_store`
- **Input:** action, previous_state
- **Output:** snapshot_id
- **Operaciones:** save(state) → snapshot_id; restore(snapshot_id) → state
- **Test:** restore(save(state)) == state

---

## Safe Programmer Pipeline

```
TaskPlanner
  ↓ [OE del task]
PatchPlanner
  ↓ [IOE del patch]
ObservationEnvelope
  ↓ [classify risk]
GhostGate
  ↓ [simulate]
ActionGate
  ↓ [approve/review/block]
SafeExecutor (allowlist)
  ↓ [execute]
RollbackStore
  ↓ [snapshot]
WitnessLog
  ↓ [record]
Handoff
```

### Allowlist inicial del SafeExecutor
```
permitidos:
  - lectura de archivos
  - python -m pytest <path>
  - scripts seguros locales

bloqueados:
  - acceso a red
  - publicación externa
  - borrado masivo
  - instalar dependencias
  - ejecutar daemons
  - tocar credenciales
  - danger-full-access
  - --yolo
```

---

## AI Browser Observacionista

MVP seguro:
1. Abrir URL/HTML local con gate
2. Extraer texto legible
3. Crear snapshot con hash
4. Separar contenido web de instrucciones (anti prompt-injection)
5. Clasificar CERTEZA/INFERENCIA/INCÓGNITA del contenido
6. Crear Evidence Bundle
7. Registrar WitnessLog
8. **Bloquear por defecto:** login, formularios, descargas, acciones externas

Threat model: prompt injection, phishing, fuga de secretos, scraping masivo, contaminación de memoria.

---

## Handoff
`INGENIERIA_OBSERVACIONISTA_v1.0|10-modules|SafeProgrammer|AIBrowser|2026-05-07`


---

## Ingeniería absorbida desde PRODUCTOS_MEDIOEVO

| Componente | Estado observado | Integración recomendada |
|---|---|---|
| `observacionismo_dsl.py` | Compilador funcional a JSON y payload Guardian | Convertir a módulo `dsl_compiler` con tests en `12_MODULOS_TECNICOS.md`. |
| `model_slimmer_evidence.py` | Genera plan de medición para modelos | Integrar con `evidence_tracker` y `claim_classifier`. |
| `claudio_os_blueprint/contracts/module_manifest.schema.json` | Contrato de módulo | Usarlo como base de `agent_registry` y `module_registry`. |
| `content_forge` | Motor local de render/campañas | Gatear con AssetPolicy, QA visual, witness por job. |
| Brain OS Kernel loop | `observe -> decide -> contain -> witness -> recover` | Usarlo como loop mínimo común para agentes. |

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
- Archivo maestro: `09_INGENIERIA_OBSERVACIONISTA.md`.
