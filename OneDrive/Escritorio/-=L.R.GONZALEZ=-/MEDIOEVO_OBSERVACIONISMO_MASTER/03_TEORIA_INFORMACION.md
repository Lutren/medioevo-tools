# 03 — TEORÍA DE INFORMACIÓN OSIT
**Estado:** R≈0.20 | Hipótesis formal publicable | Gate: PUBLISH_AS_FORMAL_HYPOTHESIS

---

## Tesis central

Shannon mide información transmisible por un canal ideal. OSIT pregunta cuánta información puede **registrar, actuar y preservar** un procesador dado su estado acumulado.

```
H_eff(X | R) = H(X) · Φ_eff(R)
```

- `H(X)` = información disponible en la fuente (Shannon)
- `R` = residuo acumulado del procesador/receptor
- `Φ_eff(R)` = eficiencia efectiva bajo ese estado
- `H_eff` = información realmente utilizable

**Principio:** Información disponible ≠ información utilizable.

---

## El receptor no ideal

OSIT extiende el modelo clásico al receptor con estado:

```
Fuente → canal → receptor con estado → acción / registro / memoria
                      ↑
              R acumulado modifica
              la capacidad de registrar
```

El canal puede ser perfecto (capacidad Shannon plena), pero si el receptor tiene R alto, H_eff se degrada.

---

## Fórmula de degradación

```
Φ_eff(R, J_c) = exp(−ν · R / (J_c − R))    para R < J_c
Φ_eff = 0                                   para R ≥ J_c
```

Forma alternativa linealizada para testing inicial:

```
Φ_eff = Φ_0 · (1 − R/J_c)^ν
```

Parámetros:
- `ν` = tasa de degradación (calibrar por dominio)
- `J_c` = umbral de jamming
- `Φ_0` = eficiencia base sin carga

---

## Aplicación a Machine Learning

| Variable OSIT | Lectura en ML |
|---|---|
| R | KV-cache saturado, contexto contradictorio, instrucciones conflictivas |
| Φ_eff | Capacidad de actualizar salida con input nuevo en ventana dada |
| J_c | Ventana de contexto útil antes de degradación de coherencia |
| Σ | Attention profile, sesgo de cabezas, rigidez de categorías |
| Segunda Pérdida | Pérdida de calibración al cruzar sesiones/modelos/contextos |
| GhostGate | Simulación antes de acción irreversible |
| ActionGate | Permiso basado en evidencia/riesgo |
| WitnessLog | Memoria externa verificable |

**Regla:** Después de J_c, más contexto reduce Φ_eff en vez de aumentarla. Aplica a LLMs (degradación de long-context), a humanos (sobrecarga cognitiva) y a agentes (saturación de estado).

---

## Compresión, entropía y residuo

- **Señal útil:** input que disminuye R al procesarse (cierre de loops, decisión, artefacto).
- **Ruido:** input que aumenta R sin producir cierre.
- **Anti-información:** input que genera loops nuevos sin aportar señal.
- **Dark information:** información presente en el sistema pero no accesible al procesador porque R bloquea su integración. Análogo funcional a "materia oscura" de información.

```
R_next = R_prev + anti_info + noise − signal_closed
```

---

## EML como laboratorio formal

`EML: f(x) = e^x − log(x)`,  x > 0

Propiedades:
- Mínimo en x* ≈ 0.567 (raíz de f'(x) = e^x − 1/x = 0, Lambert W)
- Penaliza x → 0 (log → ∞): información insuficiente es costosa
- Penaliza x grande (exponencial): saturación también es costosa
- El mínimo representa el punto óptimo de carga cognitiva

Uso recomendado en runtime:

```
E_R(input_log, R_norm) = exp(input_log) − ln(1 + R_norm)
```

**Gate:** EML como función de costo = RESEARCH_ONLY hasta calibración empírica. Como operador algebraico = PUBLISH_AS_FORMAL_HYPOTHESIS con dominio explícito.

---

## Continuidad e información entre sesiones

La continuidad no se logra cargando todo el contexto. Se logra externalizando estado mínimo antes del cierre.

Artefactos que preservan información relevante:
- `SESSION_FINGERPRINT` — identidad del estado al cierre
- `NEXT_SESSION_BRIEF` — resumen operativo para próxima sesión
- `WitnessLog` — evidencia de decisiones
- `DecisionLog` — por qué se hicieron las decisiones
- `ClaimRegister` — estado epistémico de claims
- `OpenLoops` — pendientes que generan R residual

**Fórmula operativa de handoff:**

```
Φ_eff_session = artefactos_cerrados / costo_contextual
R_next = R_prev + pendientes_no_integrados − artefactos_compilados
```

---

## Distinción de otras teorías

| Teoría | Qué mide | Diferencia con OSIT |
|---|---|---|
| Shannon | Capacidad de canal | OSIT mide capacidad del receptor con estado |
| Kolmogorov | Complejidad algorítmica | OSIT no asume procesador ideal |
| MDL | Longitud de descripción mínima | OSIT incorpora R del receptor como variable |
| Bayesian inference | Actualización de creencias | OSIT modela por qué la actualización falla (R alto) |

---

## Estado epistémico

CERTEZA: La degradación de procesamiento con carga alta es documentada (sobrecarga cognitiva, degradación de coherencia en LLMs de contexto largo).

INFERENCIA: La formulación H_eff = H · Φ_eff es operacionalmente útil. Las fórmulas de degradación requieren calibración empírica por dominio.

INCÓGNITA: ν, J_c y ε_max óptimos para cada dominio. Relación exacta entre R medido conductualmente y degradación cuantificable en LLMs.

---

## Handoff
`TEORIA_INFORMACION_v1.0|Heff-degradation-EML-continuity|2026-05-07`



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
- Archivo maestro: `03_TEORIA_INFORMACION.md`.
