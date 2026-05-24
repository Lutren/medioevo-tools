# 16 — CLAIMS REGISTER
**Estado:** R≈0.22 | Tabla de verdad epistémica | Versión 1.0 — supersede versiones anteriores

---

## Leyenda de gates

| Gate | Significado |
|---|---|
| STRONG_CLAIM_VERIFIED | Verificado algebraicamente; publicable con revisión |
| PUBLISH_AS_FORMAL_HYPOTHESIS | Formalizado, falsifiable; necesita verificación independiente |
| PUBLISH_AS_PHENOMENOLOGICAL | Modelo operativo; fenómeno medible real; sin claim físico fundamental |
| PUBLISH_ALLOWED_AS_MODEL | Modelo práctico; no claim de verdad física |
| PUBLISH_ALLOWED_WITH_SCOPE | Publicable si se explicita el alcance; sin universalización |
| RESEARCH_ONLY | Solo uso interno; sin claim público fuerte |
| REQUIRES_VALIDATION_FOR_SCIENCE | Necesita datos, baseline, preregistro, revisión externa |
| NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Física: necesita cómputo numérico + comparación observacional |
| REPHRASE_REQUIRED | Lenguaje debe cambiar antes de publicar |
| BLOCK | No implementar; no publicar; rediseñar |

---

## Sección A: Física — Sector Canónico OSIT-AG

| ID | Claim | Gate | Falsador | Fuente |
|---|---|---|---|---|
| P-01 | NEC preservada en sector canónico: T_μν k^μ k^ν = M_r²(k·∇r)² ≥ 0 | **STRONG_CLAIM_VERIFIED** | Error signo en tensor de estrés; encontrar M_r²<0 o U<0 | OSIT_AG_FORMAL_v0.2 |
| P-02 | Gradientes espaciales cancelan exactamente en Raychaudhuri: S_u = M_r² ṙ_u² − U(r) | **STRONG_CLAIM_VERIFIED** | Derivación simbólica independiente en xAct/SymPy | OSIT_AG_FORMAL_v0.2 |
| P-03 | Condición desenfoque: U(r) > M_r² ṙ_u² | **STRONG_CLAIM_VERIFIED** | Mostrar S_u < 0 falla bajo estas condiciones | OSIT_AG_FORMAL_v0.2 |
| P-04 | Sector canónico solo no soporta wormholes ni drives Alcubierre | **STRONG_CLAIM_VERIFIED** (corolario P-01) | Encontrar solución NEC-violante dentro del sector canónico | OSIT_AG_FORMAL_v0.2 |
| P-05 | J_c = 1 en sector canónico; J_c(ξ) ≠ 1 con GB activo | PUBLISH_AS_FORMAL_HYPOTHESIS | Derivar J_c(ξ) de ecuaciones GB modificadas | Pendiente |

---

## Sección B: Física — Sector Extendido (BLOQUEADOS)

| ID | Claim | Gate | Qué desbloquea |
|---|---|---|---|
| P-06 | QNM modificados por campo r | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Perturbación numérica + literatura Einstein-scalar-GB |
| P-07 | Corrección entropía Hawking (Wald) | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Cálculo Noether explícito + convención fija |
| P-08 | Velocidad GW modificada | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Satisfacer GW170817: \|c_T/c − 1\| < 5×10⁻¹⁶ |
| P-09 | Dark energy por campo r | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Fit CMB/BAO/SN Ia; comparar ΛCDM AIC |
| P-10 | Inflación por campo r | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | n_s y r_tensor; comparar Planck 2018 |
| P-11 | "Antigravedad" = propulsión/masa negativa | **BLOCK** | Redefinir siempre como desenfoque geodésico |
| P-12 | OSIT resuelve/supersede GR | **BLOCK** | Reformular como "extiende GR con sector escalar" |
| P-20 | Σ aparece en g_μν | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Acoplamiento explícito + covarianza + observable |

---

## Sección C: Medición OSIT-M

| ID | Claim | Gate | Falsador |
|---|---|---|---|
| P-21 | POVM deformado Φ_R es CPTP para todo ε∈[0,1] | PUBLISH_AS_FORMAL_HYPOTHESIS | Verificar completitud Kraus; encontrar ε donde falla |
| P-22 | "El fotón renderiza la realidad" | REPHRASE_REQUIRED | Reformular: "detección de fotón = evento POVM en interfaz observador-aparato" |

---

## Sección D: Información y Observador

| ID | Claim | Gate | Notas |
|---|---|---|---|
| I-01 | O_i(t) = L_i(C_i(G_i(∫R_i(S)dt))) | PUBLISH_AS_FORMAL_HYPOTHESIS | Formaliza pipeline sensorial |
| I-02 | R = residuo acumulado no integrado | PUBLISH_ALLOWED_WITH_SCOPE | Definir método de medición antes de uso clínico |
| I-03 | Φ_eff = eficiencia de actualización/cierre | PUBLISH_ALLOWED_WITH_SCOPE | Proxy operativo; sin medida externa validada aún |
| I-04 | J_c: más input después del umbral reduce claridad | PUBLISH_AS_FORMAL_HYPOTHESIS | EML lo formaliza; requiere calibración empírica |
| I-05 | Realidad = calibración de lenguaje entre observadores | PUBLISH_ALLOWED_WITH_SCOPE | No "dos realidades físicas diferentes" |
| I-08 | "Caminamos hacia el futuro viendo el pasado" | PUBLISH_ALLOWED_AS_MODEL | Compatible con flecha termodinámica |
| I-09 | "El tiempo y el espacio son vectores cognitivos humanos" | REPHRASE_REQUIRED | Reformular: "coordenadas espacio-temporales son representaciones relativas a la medición" |

---

## Sección E: Sigma / Cognitiva

| ID | Claim | Gate | Notas |
|---|---|---|---|
| C-01 | Diferencias individuales en Δt_min y Δ_i son medibles | PUBLISH_AS_PHENOMENOLOGICAL | Soportado por literatura (Battelli 2007, Donohue 2012) |
| C-02 | Apertura cognitiva ("diafragma") | PUBLISH_ALLOWED_AS_MODEL | Compatible con sensory gating; metáfora con proxy conductual |
| C-03 | Algunas perfiles autistas tienen mayor ganancia sensorial en canales específicos | PUBLISH_AS_PHENOMENOLOGICAL + REQUIRES_VALIDATION_FOR_SCIENCE | No universal |
| C-04 | "Todos los autistas tienen más input" | REPHRASE_REQUIRED | Dimensión de variación, no ley universal |
| C-07 | Newton case: su Sigma limitó su física | PUBLISH_ALLOWED_AS_MODEL | Heurístico, no psicoanálisis |

---

## Sección F: IA / Arquitectura

| ID | Claim | Gate | Notas |
|---|---|---|---|
| A-01 | OSO como identidad de agente serializable y portable | RESEARCH_ONLY | Requiere implementación + auditoría de seguridad |
| A-02 | Orquestador determinístico, no LLM | PUBLISH_ALLOWED_AS_MODEL | Decisión arquitectural testable |
| A-03 | Conway evolution protocol | RESEARCH_ONLY | Requiere ciclo de test controlado |
| A-04 | Wabi-Sabi gate: aceptar mejoras imperfectas con evidencia | PUBLISH_ALLOWED_AS_MODEL | Protocolo claro y auditable |
| A-05 | EML como función de costo de carga cognitiva | RESEARCH_ONLY | Propiedades matemáticas verificadas; calibración empírica pendiente |
| A-07 | AGI = proceso distribuido de componentes cognitivos | PUBLISH_ALLOWED_WITH_SCOPE | No afirmar equivalencia AGI sin benchmark |
| A-09 | danger-full-access / yolo mode | **BLOCK** | No negociable |

---

## Sección G: Seguridad

| ID | Claim | Gate | Acción |
|---|---|---|---|
| S-01 | Escaneo sigiloso de red (escaner sigiloso.txt) | **BLOCK** | Reescribir como inventario defensivo autorizado sin stealth |
| S-02 | Automatizar interfaces gratuitas de LLM | REVIEW_REQUIRED | Probable violación de ToS; no productizar |
| S-03 | Ejecutar repo DUAT-GEODIA sin auditoría | **BLOCK** | Solo análisis estático hasta revisión completa |

---

## Sección H: Narrativa / Producto

| ID | Claim | Gate | Notas |
|---|---|---|---|
| N-01 | "El Observador" como narrativa pública | PUBLISH_ALLOWED_WITH_SCOPE | Separado de physics paper y SDK |
| N-02 | "OSIT unifica todos los sistemas" | REPHRASE_REQUIRED | Reformular: "OSIT es framework de mapeo aplicable a múltiples dominios" |
| N-04 | "OSIT explica la consciencia" | REPHRASE_REQUIRED + BLOCK (claim fuerte) | Reformular: "OSIT provee variables operativas para estudiar observación" |
| N-05 | Matrix como mapa de comunicación | PUBLISH_ALLOWED_AS_MODEL | Etiquetado explícitamente como metáfora |

---

## Handoff
`CLAIMS_REGISTER_v1.0|P01-04-VERIFIED|POVM-FORMAL|AI-RESEARCH|BLOCKS-MAINTAINED|2026-05-07`


---

## Claims añadidos o reforzados por este pase

| CLAIM_ID | Claim | Categoría | Evidencia disponible | Riesgo | Falsador mínimo | Estado |
|---|---|---|---|---|---|---|
| BRAIN-01 | Brain OS es una capa cognitiva local-first sobre la máquina, no un kernel Linux | IA_TEORIA / INGENIERIA | `claudio_os_blueprint/docs/BRAIN_OS_PRINCIPLES.md`, `ARCHITECTURE.md` | Bajo si se formula así | Verificar que docs y CLI lo tratan como loop cognitivo | PUBLISH_ALLOWED_AS_MODEL |
| DSL-01 | Observacionista DSL compila intención/evidencia/estado/acción/witness a JSON | CODIGO / MODULO | `observacionismo_dsl.py` leído | Bajo | Ejecutar tests de parseo/validación | PUBLISH_AS_PHENOMENOLOGICAL |
| MODEL-01 | Un modelo reducido solo reemplaza baseline tras medición de accuracy, latencia, memoria, energía y seguridad | IA_TEORIA / MODULO | `MODEL_EFFICIENCY.md`, `model_slimmer_evidence.py` | Bajo | Candidate que falla umbrales debe bloquear | PUBLISH_ALLOWED_WITH_SCOPE |
| PROD-01 | Content Forge produce paquetes locales sin publicar automáticamente | PROYECTO | `content_forge/README.md` | Medio | Ejecutar job local y confirmar no publicación externa | PUBLISH_ALLOWED_AS_MODEL |
| SEC-04 | Automatización de browser sin manifiesto debe bloquearse | SEGURIDAD | `OBSERVACIONISMO_OS.md`, ClaudioOS README | Bajo | Acción browser sin manifest -> block | PUBLISH_ALLOWED_WITH_SCOPE |

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
- Archivo maestro: `16_CLAIMS_REGISTER.md`.
