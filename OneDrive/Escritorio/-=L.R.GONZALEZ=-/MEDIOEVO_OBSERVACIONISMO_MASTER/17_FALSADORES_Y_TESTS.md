# 17 — FALSADORES Y TESTS
**Estado:** R≈0.20 | Pruebas mínimas por dominio

---

## Física: Sector Canónico OSIT-AG

### F-PHY-01: Verificación algebraica independiente
- **Herramienta:** Mathematica + xAct, o Python + SymPy + EinsteinPy
- **Prueba:** Reproducir derivaciones de P-01, P-02, P-03 en ≤ 20 líneas de código simbólico
- **Rechazo:** Si la derivación produce resultado diferente bajo mismas convenciones, P-01–P-03 fallan
- **Tiempo estimado:** 2–4 horas de trabajo técnico

### F-PHY-02: J_c(ξ) con Gauss-Bonnet
- **Acción:** Extender derivación a S = S_can + ∫ ξ(r) G_GB; computar ecuaciones modificadas
- **Resultado esperado:** J_c(ξ=0) = 1; J_c(ξ≠0) ≠ 1
- **Rechazo:** J_c = 1 independientemente de ξ → el parámetro es trivial

### F-PHY-03: Compatibilidad GW170817
- **Prueba:** Derivar c_T en el sector GB activo
- **Criterio:** |c_T/c − 1| < 5×10⁻¹⁶ debe satisfacerse
- **Rechazo:** c_T ≠ c sin margen → claim P-08 bloqueado permanentemente

---

## Física: OSIT-M (Measurement Operator)

### F-POVM-01: Experimento conductual mínimo
- **Diseño:** Tarea de detección de señal (d', β) con prevalencia conocida p_signal
- **N:** ≥ 60 observadores por grupo
- **Variables:** H_i (hit rate), FA_i (false alarm rate), R_est_i (proxy conductual)
- **Cómputo:** ε_i = (H_i + FA_i − 1) / (1 − 1/d)
- **Test:** correlación Spearman ρ(ε_i, R_est_i) > 0 con p < 0.05
- **Rechazo:** ρ ≤ 0, o ε_i predice mejor performance a mayor R

### F-POVM-02: Preregistro obligatorio
- Preregistrar en OSF antes de recopilar datos
- Especificar: hipótesis, dataset, métricas, umbrales, análisis
- Sin preregistro: cualquier resultado = RESEARCH_ONLY, no FORMAL_HYPOTHESIS

---

## Sigma / Temporal

### F-SIGMA-01: TOJ paradigma
- **Tarea:** Temporal Order Judgment (TOJ) — dos estímulos visuales/auditivos
- **Medida:** Δt_min (JND) por observador
- **Correlación:** Δt_min vs. AQ-10 (autistic traits), R_est, edad
- **N:** ≥ 60 por grupo
- **Rechazo:** Sin correlación significativa Δt_min vs. AQ-10 → claim C-03 debilitado

### F-SIGMA-02: Sensory gain diferencial
- **Tarea:** Detección de contraste visual/auditivo en umbral
- **Medida:** Umbral individual por modalidad
- **Correlación:** Umbral vs. AQ-10 vs. diagnóstico autista (si disponible)
- **Gate:** Aprobación ética; no uso diagnóstico sin revisión clínica

---

## IA / Módulos

### F-MOD-01: state_estimator calibración
- **Datos:** ≥ 50 sesiones reales con R auto-reportado y estado final
- **Test:** Correlación R_est (función de history/pending/corrections) vs. R_auto-reportado
- **Rechazo:** R calculado no correlaciona con R reportado → recalibrar factores

### F-MOD-02: action_gate determinismo
- **Prueba:** Misma entrada, misma salida en 100 corridas
- **Rechazo:** Varianza en salida → gate no es determinístico → rediseñar

### F-MOD-03: context_compactor — H_eff preservada
- **Prueba:** Evaluar si LLM downstream produce mismo resultado con contexto compactado vs. full
- **Métrica:** delta(score_task) < 5% con 50% de tokens
- **Rechazo:** Degradación > 5% → compactor pierde demasiada señal

### F-MOD-04: witness_log — integridad
- **Prueba:** Intentar sobrescribir entrada → error; hash(entry) == hash(re-read)
- **Rechazo:** Cualquier escritura que modifica entrada existente → falla de seguridad crítica

---

## Conway Evolution

### F-CONWAY-01: Ciclo controlado mínimo
- **Setup:** 1 agente, 1 tarea repetitiva, 1 método propuesto alternativo
- **Test:** Aplicar Wabi-Sabi gate; medir delta_metric antes/después
- **Criterio:** delta_metric > 0 con riesgo < threshold → aceptación válida
- **Rechazo:** Método aceptado degrada performance → gate falla → revisar threshold

---

## EML

### F-EML-01: Calibración del mínimo
- **Prueba:** Medir throughput/accuracy en agente/humano en función de carga x
- **Esperado:** Curva U: peor a x→0, óptimo en x≈0.567, peor a x→∞
- **Rechazo:** Sin forma U o mínimo diferente de 0.567 → EML necesita reparametrización

---

## Handoff
`FALSADORES_Y_TESTS_v1.0|physics-POVM-sigma-modules-conway-EML|2026-05-07`


---

## Tests técnicos añadidos

| ID | Dominio | Prueba mínima | Rechazo |
|---|---|---|---|
| F-DSL-01 | DSL | DSL válido con `intent`, `evidence`, `state`, `action`, `witness` compila a JSON | Parser acepta programa sin evidencia o witness |
| F-MODEL-01 | Model efficiency | Candidate con `accuracy_drop > 0.02` bloquea | Gate permite reemplazo sin aprobación |
| F-MANIFEST-01 | Módulos | Manifest sin `purpose`, `inputs`, `outputs`, `risk`, `gates`, `witness`, `recovery` falla | Módulo ejecutable sin contrato |
| F-CONTENT-01 | Content Forge | Job local genera carpeta runtime y QA sin autopost | Cualquier acción externa ocurre sin approval |
| F-CURADOR-01 | Curador | Fuente nueva sin ficha queda `REVIEW` | Fuente cruda entra a canon sin trazabilidad |

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
- Archivo maestro: `17_FALSADORES_Y_TESTS.md`.
