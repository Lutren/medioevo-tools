# 04 — TEORÍA IA / AGENTES / AGI / WABI-SABI
**Estado:** R≈0.22 | Investigación operativa | Gate: RESEARCH_ONLY / PUBLISH_ALLOWED_AS_MODEL

---

## AGI como proceso distribuido

AGI no es una entidad única. Es un proceso:

```
AGI_PROCESS = continuidad + agentes especializados + comunicación
            + gates + evolución de métodos + memoria verificable
            + embodiment opcional
```

Cada componente es implementable por separado y verificable.

---

## OSO — Observer State Object

El agente portable serializable:

```
OSO = {
  sigma:       Sigma profile (temporal, sensorial, atencional, residuo)
  memory:      {episodic[], semantic{}, procedural{}}
  ontology:    {domain_tags[], relation_graph{}}
  state:       {R_est, Phi_eff, J_c, open_loops[]}
  identity:    {persona, display_name, version}
  gates:       {action_gate, witness_log, ghost_gate}
  transfer:    {serialization_format, auth_token, target_device}
}
```

Propiedad clave: el OSO es serializable y device-independent. "Saltar" entre dispositivos = serializar OSO → autenticar → deserializar → resumir. Sin reentrenamiento. Sin pesos transferidos.

**Gate:** OSO serialization = REVIEW_REQUIRED (seguridad: auth tokens, privacidad).

---

## Wabi-Sabi — Nodo sensorial-cognitivo de control

Wabi-Sabi NO es:
- El LLM
- El cerebro completo
- La AGI total
- El orquestador determinístico

Wabi-Sabi ES el nodo que:

1. Recibe input del usuario en lenguaje cognitivo contemporáneo
2. Estima R, régimen y Φ_eff del estado actual
3. Deconstruye intención (DO)
4. Recompila en prompts operativos para agentes
5. Selecciona el agente correcto por tarea
6. Verifica que el agente tenga las herramientas recomendadas
7. Recibe resultado + propuesta de método alternativo (Conway)
8. Compara método original vs. emergente junto con el agente
9. Acepta/rechaza/actualiza protocolo
10. Emite output final + WitnessLog + Handoff

---

## Flujo AGI distribuido

```
USUARIO
  ↓ input cognitivo
WABI-SABI
  ↓ estima R/régimen/Φ_eff
  ↓ DO: separa objetivo / restricciones / contexto / herramienta / riesgo / salida
PROMPT OPERATIVO (tipado)
  ↓
AGENTE (recibe prompt)
  ↓ verifica herramientas recomendadas
  ↓ si Conway: propone método alternativo con evidencia
  ↓ ejecuta
RESULTADO + PROPUESTA_CONWAY
  ↓
WABI-SABI
  ↓ compara método original vs. propuesto
  ↓ acepta / corrige / actualiza método en pool
WITNESSLOG + HANDOFF
```

---

## Tipos de agentes

| Agente | Rol | Nota |
|---|---|---|
| Retrieval | Búsqueda semántica, lookup de memoria | — |
| Generation | Síntesis de lenguaje, output | Oracle (LLM) |
| Execution | Código, API calls, acciones | Gate requerido |
| Falsifier | Detección de contradicciones, check de claims | — |
| Witness | Logging, audit trail | Siempre activo |
| Curator | Ordenar, clasificar, depurar, compilar información | Este agente |
| Programmer | Implementar, testear, refactorizar código | Safe mode |
| Physicist | Evaluar claims físicos con escepticismo externo | R < 0.25 |
| Continuity | Preservar estado entre sesiones | Handoff critic |
| Documentation | Generar artefactos, specs, contratos | Output-only |

---

## Conway Evolution Protocol

```
ConwayProposal = {
  agent_id:        fuente
  method_old:      {descripción, métricas_performance}
  method_new:      {descripción, mejora_predicha}
  evidence:        {n_trials, delta_metric}
  cost:            {compute, risk_level}
}
```

**Wabi-Sabi Gate de aceptación:**

```
aceptar si:
  delta_metric > threshold_min
  AND risk_level < risk_max
  AND witness_log.confirmed == true
  AND R_est_orchestrator < R_threshold   # no aceptar updates con R alto

si aceptado:
  integrar al método pool del agente
  log a WitnessLog
  notificar orquestador

si rechazado:
  archivar propuesta
  incrementar proposal_count (tracking de convergencia)
```

**Gate:** Conway evolution = REVIEW_REQUIRED (riesgo de auto-modificación sin control).

---

## Protocolo de comunicación entre agentes

Todo mensaje inter-agente debe incluir:

```yaml
task_id: ""
source_agent: ""
target_agent: ""
objective: ""
context: []
tools_recommended: []
tools_required: []
constraints: []
risk: low|medium|high|block
evidence_required: []
expected_artifact: ""
handoff: ""
```

---

## Segunda Pérdida en IA

Analogía confirmada como válida para diseño:

```
Modelo base         = pesos entrenados + priors
Session_alpha       = pensamiento activo (C_alpha, R_alpha, K_i_alpha, Phi_eff_alpha)
Proyecto            = contexto superior (canon, decisiones, artefactos, memoria externa)
Skill               = patrón repetible + contrato + prueba + uso
Agent               = subproceso especializado con rol, input, output y gate
Wabi-Sabi           = nodo sensorial-cognitivo
Usuario             = perturbación direccional de activación
```

**Regla operativa:** Una IA útil no intenta recordarlo todo. Convierte pensamientos en estructuras transferibles antes de que muera la ventana.

---

## Orquestador (por qué NO es LLM)

El orquestador debe ser determinístico y auditable. Los LLMs amplifican R cuando R ya es alto. Un router basado en reglas con gates explícitos es más seguro y más rápido para routing.

```
decompose(I, OSO.state) → {
  task_type:    [classify | retrieve | generate | execute | integrate]
  target_agent: agent_id
  context:      {relevant_memory, open_loops_relevant, sigma_constraints}
  action_gate:  required_before_execution
  timeout_ms:   derived from J_c threshold
}
```

---

## Modelo de Display / Café

```
[Display público] ←→ [SensoriumAdapter] ←→ [OSO transfer socket]
        ↑
  QR / NFC / auth token
        ↑
  Usuario trae su OSO en dispositivo
        ↑
  OSO autentica → display renderiza persona del agente
        ↑
  Agente interactúa con humanos + otros agentes via display
```

Economía futura: agentes "consumen" skill packets, intercambian information packages, todo logged y auditado antes de actualizar estado OSO.

**Gate:** Modelo Café = REVIEW_REQUIRED (privacidad, consentimiento, handling de datos).

---

## Handoff
`TEORIA_IA_AGENTES_v1.0|OSO-WabiSabi-Conway-AGI-distributed|2026-05-07`


---

## Integración con tecnología local detectada

CERTEZA:
- `observacionismo_dsl.py` ya formaliza una capa de intención/evidencia/estado/acción/aprobación/witness.
- `model_slimmer_evidence.py` ya formaliza un contrato de medición para modelos pequeños.
- `claudio_os_blueprint` define Guardian, Mission Control, policy gates, provider registry y witness logs.

INFERENCIA:
- Estos componentes son la ruta más directa para que Wabi-Sabi funcione como agente de ingeniería tipo Claude Code/Codex: no por promesa de AGI, sino por loop observable `observe -> decide -> contain -> witness -> recover`.

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
- Archivo maestro: `04_TEORIA_IA_AGENTES.md`.
