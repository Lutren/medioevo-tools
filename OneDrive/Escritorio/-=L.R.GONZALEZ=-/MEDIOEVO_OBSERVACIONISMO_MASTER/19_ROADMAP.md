# 19 — ROADMAP
**Estado:** R≈0.22 | Planificación por fases | Actualizado: 2026-05-07

---

## Fase 0 — Ordenar documentos ✓ (esta sesión)

- DONE: Inventario de 125 fuentes
- DONE: Canon v0.2 consolidado (8 documentos vivos)
- DONE: Claims Register v1.0
- DONE: Authority Map v0.1
- DONE: Line Audit v0.1 (37.401 líneas)
- DONE: Carpeta MEDIOEVO_OBSERVACIONISMO_MASTER (23 archivos)
- PENDING: Convertir carpeta en repo `medioevo-canon`

---

## Fase 1 — Consolidar Canon

- PENDING: Crear `schemas/` JSON para OSO, AgentMessage, WitnessLog, ActionGate
- PENDING: Validar obs_ai_runtime.py con tests unitarios
- PENDING: SECRET_SCAN del repo Duat-Geodia
- PENDING: VISIBILITY_MATRIX (qué es público/privado)
- PENDING: Separar RPG/DUAT privado de open-source
- PENDING: Preregistrar EXP-1 (OSIT-M) y EXP-2 (Sigma) en OSF

---

## Fase 2 — Convertir teoría en módulos

- PENDING: Implementar state_estimator con tests calibrados
- PENDING: Implementar action_gate determinístico
- PENDING: Implementar witness_log append-only con hash
- PENDING: Implementar handoff_generator
- PENDING: Implementar context_compactor
- PENDING: Implementar ghost_gate (simulación sin ejecución)
- PENDING: Derivación simbólica J_c(ξ) en xAct/SymPy
- PENDING: Ciclo Conway test: 1 agente, 1 mejora, 1 decisión Wabi-Sabi

---

## Fase 3 — Prototipo local

- PENDING: Mission Control v1 read-only (muestra estado agentes, WitnessLog, gates)
- PENDING: OSO JSON schema versionado + serialización/deserialización
- PENDING: Orquestador determinístico mínimo (router + decomposer)
- PENDING: AI Browser seguro (URL → snapshot → evidence bundle)
- PENDING: Safe Programmer con allowlist + GhostGate + RollbackStore
- PENDING: Integration test: flujo completo WabiSabi → Agent → WitnessLog → Handoff

---

## Fase 4 — Validar claims

- PENDING: Ejecutar EXP-1 (OSIT-M): N=60, TOJ + signal detection + R proxy
- PENDING: Ejecutar EXP-2 (Sigma): N=60, Δt_min vs AQ-10
- PENDING: Cómputo numérico P-06 (QNM) con EinsteinPy/Mathematica
- PENDING: Comparación J_c(ξ) derivado vs. datos de literatura Einstein-scalar-GB
- PENDING: Calibración ν, J_c, ε_max en obs_ai_runtime con datos reales

---

## Fase 5 — Preparar publicación / release

- PENDING: Paper técnico OSIT-AG: NEC + gradientes + desenfoque (P-01–P-04) + falsador
- PENDING: Nota formal OSIT-M: POVM deformado + experimento + resultados
- PENDING: SDK observacionismo v0.1: ActionGate + WitnessLog + handoff templates
- PENDING: "El Observador" narrativa pública v1
- PENDING: Demo local Duat-Geodia (después de auditoría y phase 3 completa)

---

## Handoff
`ROADMAP_v1.0|5-phases|phase0-complete|2026-05-07`


---

## Ajuste de roadmap por este pase

Fase 0 cerrada en esta carpeta: inventario, compilación master, manifiesto y handoff.

Fase 1 prioritaria:
- Crear o localizar `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md` para `PRODUCTOS_MEDIOEVO`.
- Ejecutar tests unitarios sobre `observacionismo_dsl.py` y `model_slimmer_evidence.py`.
- Crear JSON schemas para OSO, AgentMessage, WitnessLog, ActionGate y ModuleManifest.
- Separar publicable/comercial/privado antes de cualquier publicación.

Fase 2 técnica:
- Convertir `curator_order_assistant` en módulo/CLI.
- Conectar `dsl_compiler`, `model_efficiency_gate`, `module_manifest_validator` con Brain OS/Guardian.
- Mission Control read-only para visualizar gates, witness y pendientes.

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
- Archivo maestro: `19_ROADMAP.md`.
