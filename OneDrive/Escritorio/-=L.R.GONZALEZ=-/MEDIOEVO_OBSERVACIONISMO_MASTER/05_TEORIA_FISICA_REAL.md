# 05 — TEORÍA FÍSICA ESTÁNDAR COMPATIBLE
**Estado:** R≈0.22 | Solo física estándar o analogías explícitamente compatibles

---

## Propósito

Este documento contiene SOLO física estándar o analogías que son explícitamente compatibles con física establecida. Los claims propios de OSIT-QG van en el archivo 06.

---

## Relatividad General — base de OSIT-AG

**Acción de Einstein-Hilbert:**
```
S_EH = ∫ d⁴x √(−g) R_E/(2κ²)
```

**Ecuaciones de Einstein:** G_μν = 8πG T_μν

**Condición de Energía Nula (NEC):** Para cualquier vector nulo k^μ: T_μν k^μ k^ν ≥ 0.

**Interpretación:** Materia con NEC positiva enfoca geodésicas nulas (teoremas de Penrose-Hawking). Para soportar agujeros de gusano o drives tipo Alcubierre se requiere violación de NEC.

**OSIT-AG en este contexto:** El sector canónico de OSIT-AG (campo escalar con M_r²>0, U(r)≥0) preserva NEC. Resultado algebraicamente verificado.

---

## Ecuación de Raychaudhuri

Para congruencia de geodésicas timelike con vector tangente u^μ:

```
dθ/dτ = −(1/3)θ² − σ_μν σ^μν + ω_μν ω^μν − R_μν u^μ u^ν
```

La fuente de focalización/desenfoque es R_μν u^μ u^ν. Vía ecuaciones de Einstein: R_μν u^μ u^ν = 8πG S_u.

**Desenfoque** requiere S_u < 0. En sector canónico OSIT-AG: S_u = M_r² ṙ_u² − U(r). Desenfoque ocurre cuando U(r) > M_r² ṙ_u².

---

## Termodinámica y entropía

**Entropía de Bekenstein-Hawking:** S_BH = A/(4G), donde A es el área del horizonte.

**Corrección de Wald:** Para teorías de gravedad modificada f(R) o con acoplamiento escalar, la entropía se calcula desde la carga de Noether. Requiere derivación explícita con convención fija.

**Aplicación en OSIT-QG:** La corrección de entropía de Wald para el sector Gauss-Bonnet acoplado requiere cálculo numérico explícito. Estado: NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC.

---

## Teoría de campo cuántico — compatibilidad declarada

**OSIT-AG como EFT:** El sector OSIT-AG/QG se enmarca como teoría de campo efectiva (EFT) de baja energía, no como teoría fundamental de gravedad cuántica. Compatible con el enfoque de Donoghue (GR como EFT).

**POVM — Medición cuántica estándar:**
```
p(i | ρ) = Tr(Π_i ρ),  Σ_i Π_i = I
```

**OSIT-M:** Extiende esto al canal real de detección incluyendo el estado R del observador como parámetro de deformación depolarizante. El canal deformado Φ_R es CPTP para todo ε ∈ [0,1]. No modifica la función de onda; modifica el canal detector-registro. Compatible con quantum optics estándar (eficiencia del detector, back-action, POVM).

---

## Velocidad de ondas gravitacionales

**Constraintia GW170817:** |c_T/c − 1| < 5×10⁻¹⁶

Cualquier modificación de la métrica debe satisfacer este constraint. Para OSIT-QG con acoplamiento Gauss-Bonnet: requiere verificación numérica explícita. Estado: BLOQUEADO hasta cómputo.

---

## Parámetros post-newtonianos (PPN)

Para compatibilidad solar:
- γ_PPN = 1 (GR exacto)
- β_PPN = 1 (GR exacto)

Toda EFT que modifique el sector escalar debe demostrar que recupera estos valores en el límite de campo débil.

---

## Cosmología observacional — baseline

- CMB: Planck 2018. n_s = 0.9649 ± 0.0042, A_s = 2.1×10⁻⁹.
- BAO: SDSS/BOSS constraints en la ecuación de estado de dark energy.
- SN Ia: Pantheon. w = −1.028 ± 0.032.
- Estándar cosmológico: ΛCDM.

Cualquier claim de OSIT-QG sobre dark energy o inflación debe compararse contra estos datos con criterio AIC/BIC.

---

## Sensoriomotor y neurofísica (compatible con SIGMA)

**Temporal Order Judgment (TOJ):** Paradigma estándar para medir Δt_min (resolución temporal mínima discriminable). Battelli et al. 2007; Donohue et al. 2012.

**Sensory gating:** Freedman et al. 1987. Documentado en psicofísica. Compatible con metáfora del "diafragma cognitivo" en OSIT-Sigma.

**Sensory gain diferencial en autismo:** Marco et al. 2011; Tavassoli et al. 2014. Documentado en algunas modalidades. NO universal.

---

## Principio de Arrow of Time (compatible con OSIT)

El claim "caminamos por la línea del tiempo de espaldas, viendo el pasado" es compatible con la flecha termodinámica del tiempo: la entropía aumenta hacia el futuro; nuestra memoria registra el pasado porque es la dirección de menor entropía.

Formulación publicable (I-08): "compatible con la flecha termodinámica del tiempo; no es un nuevo claim físico."

---

## Handoff
`TEORIA_FISICA_REAL_v1.0|GR-POVM-EFT-PPN-CMB-TOJ|standard-only|2026-05-07`



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
- Archivo maestro: `05_TEORIA_FISICA_REAL.md`.
