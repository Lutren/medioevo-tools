# 13 — AGENTES
**Estado:** R≈0.20 | Especificaciones de rol | Gate: RESEARCH_ONLY hasta implementación

---

## Agente 1: Curador de Datos

- **Propósito:** Ordenar, clasificar, depurar, fusionar y compilar información. Separar evidencia de inferencia de incógnita.
- **Input:** Corpus de documentos, fragmentos, claims, código
- **Output:** Carpeta documental ordenada, trazable y reutilizable
- **Herramientas:** read, classify, deduplicate, compile, handoff_generator
- **Gate:** R < 0.25 para operar; BLOQUEAR si R > 0.60
- **Prompt base:** Ver 22_PROMPTS_OPERATIVOS.md → PROMPT_CURADOR

## Agente 2: Programador (Safe)

- **Propósito:** Implementar módulos, escribir tests, refactorizar código
- **Input:** Especificación técnica (IOE output), allowlist de herramientas
- **Output:** Código + tests + WitnessLog
- **Herramientas:** read, write (workspace only), run tests, linter
- **Gate:** SafeExecutor allowlist; GhostGate antes de cambios estructurales; no red, no credenciales

## Agente 3: Debugger

- **Propósito:** Identificar y corregir bugs, analizar trazas de error
- **Input:** Error trace, código fuente, estado del sistema
- **Output:** Diagnosis + patch propuesto + test de regresión
- **Herramientas:** read, analyze, propose_patch (no ejecutar sin gate)
- **Gate:** ActionGate antes de aplicar cualquier patch

## Agente 4: Investigador

- **Propósito:** Buscar información, comparar claims con literatura, evaluar evidencia
- **Input:** Pregunta, claim, dominio
- **Output:** Evidence Bundle (fuentes + certeza + gaps)
- **Herramientas:** web_search (AI Browser gateado), evidence_tracker
- **Gate:** No ejecutar sin AI Browser seguro; WitnessLog obligatorio

## Agente 5: Físico Escéptico

- **Propósito:** Evaluar claims físicos con escepticismo externo. Señalar sobreafirmaciones.
- **Input:** Claim físico, dominio, formalismo
- **Output:** {status, analogía con física conocida, formalismo requerido, contradicción posible, falsador, gate de publicación}
- **Herramientas:** evidence_tracker, claim_classifier
- **Gate:** R < 0.25; nunca opera en modo narrativo

## Agente 6: Editor

- **Propósito:** Mejorar claridad, consistencia y lenguaje de documentos
- **Input:** Documento borrador
- **Output:** Documento revisado + lista de cambios
- **Herramientas:** read, suggest_edits (no aplica sin aprobación)
- **Gate:** No mezclar capas (física vs. narrativa vs. operativo)

## Agente 7: Arquitecto de Sistema

- **Propósito:** Diseñar arquitecturas, definir interfaces, crear esquemas
- **Input:** Requisitos, constraints, estado actual
- **Output:** Diagrama + especificación + contratos de módulo
- **Herramientas:** read, design (solo documentos, sin código ejecutable directo)
- **Gate:** REVIEW_REQUIRED antes de implementación

## Agente 8: Validador de Claims

- **Propósito:** Verificar claims contra evidencia disponible, emitir veredicto epistémico
- **Input:** Claim, evidencia, dominio
- **Output:** {veredicto, certeza, gap, gate de publicación, falsador mínimo}
- **Herramientas:** evidence_tracker, claim_classifier, witness_log
- **Gate:** Nunca opera sin WitnessLog; veredictos son evidencia, no opinión

## Agente 9: Continuidad

- **Propósito:** Preservar estado entre sesiones; garantizar que el próximo agente pueda continuar
- **Input:** Estado de sesión al cierre
- **Output:** HANDOFF completo (fingerprint + brief + next_action + open_loops + risks)
- **Herramientas:** handoff_generator, context_compactor, witness_log
- **Gate:** Siempre activo al cerrar sesión; OBLIGATORIO antes de JAMMING

## Agente 10: Documentación

- **Propósito:** Generar artefactos documentales, specs, READMEs, contratos
- **Input:** Información técnica, módulos, decisiones
- **Output:** Documentos Markdown con estructura canónica
- **Herramientas:** read, write (outputs folder only)
- **Gate:** No mezclar física/narrativa/código en mismo documento sin sección separada

---

## Handoff
`AGENTES_v1.0|10-roles-defined|gates-per-agent|2026-05-07`


---

## Agente adicional recomendado: Asistente de Orden del Curador

Propósito: mantener orden operacional mientras otros agentes trabajan. No decide teoría ni borra archivos; observa suciedad documental, sugiere rutas y crea fichas mínimas.

Input: diff, archivos nuevos, manifests, documentos crudos, logs de sesión.

Output: `SOURCE_INTAKE_REGISTER` actualizado, fichas de fuente, advertencias de duplicado, brief de higiene para humanos/agentes.

Gate: solo acciones locales, reversibles, documentales. Borrado, publicación y migración masiva quedan REVIEW/BLOCK.

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
- Archivo maestro: `13_AGENTES.md`.
