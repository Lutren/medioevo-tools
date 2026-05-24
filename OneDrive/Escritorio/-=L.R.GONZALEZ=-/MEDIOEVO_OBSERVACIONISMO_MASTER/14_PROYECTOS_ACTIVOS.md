# 14 — PROYECTOS ACTIVOS
**Estado:** R≈0.22 | Inventario operativo | Actualizado: 2026-05-07

---

## Proyecto 1: MEDIOEVO Canon

| Campo | Valor |
|---|---|
| Estado | ACTIVO — versión v0.2 consolidada |
| Objetivo | Mantener corpus documental trazable y autorizado |
| Archivos relacionados | `MEDIOEVO_CANON_v0_2/` (8 docs), `MEDIOEVO_OBSERVACIONISMO_MASTER/` (este repo) |
| Siguiente acción | Convertir esta carpeta en repo base `medioevo-canon`; crear `schemas/` para OSO/AgentMessage/WitnessLog/ActionGate |
| Riesgo | Mezclar capas (física vs. narrativa vs. operativo) — mitigado con archivos separados |
| Dependencia | Ninguna externa |

---

## Proyecto 2: OSIT-AG Paper

| Campo | Valor |
|---|---|
| Estado | ACTIVO — resultados algebraicos P-01 a P-04 verificados |
| Objetivo | Publicar nota técnica de 4 páginas: NEC + cancelación gradientes + condición desenfoque + falsador |
| Archivos relacionados | `MEDIOEVO_OSIT_AG_FORMAL_v0_2.md`, `06_HIPOTESIS_FISICAS_OSIT_TUIP_SIGMA.md` |
| Siguiente acción | 1. Derivación simbólica en xAct/SymPy; 2. Extender a ξ≠0 para J_c(ξ); 3. Comparar con Einstein-scalar-GB literature (Bakopoulos et al.) |
| Riesgo | Sobreafirmar sin cómputo numérico — mitigado con gates explícitos |
| Dependencia | Herramienta simbólica (Mathematica/SymPy) |

---

## Proyecto 3: Duat-Geodia App

| Campo | Valor |
|---|---|
| Estado | PROTOTIPO EXISTS — READ-ONLY. No ejecutar sin auditoría |
| Objetivo | Sistema operativo-ciudad local-first con frontend + API + DB |
| Archivos relacionados | `Duat-Geodia/` (repo completo), `MEDIOEVO_DOCUMENT_INVENTORY_v0_1.md` |
| Siguiente acción | 1. SECRET_SCAN_REPORT; 2. Auditoría de código estático; 3. VISIBILITY_MATRIX; 4. Mission Control v1 read-only |
| Riesgo | Secretos en repo, código sin auditar, separación privado/público pendiente |
| Dependencia | Auditoría de seguridad antes de cualquier ejecución |

---

## Proyecto 4: obs_ai_runtime.py

| Campo | Valor |
|---|---|
| Estado | MÓDULO INICIAL — funcional como placeholder, necesita calibración |
| Objetivo | Runtime Python que implementa R, Φ_eff, régimen, DO/IOE, ActionGate, Handoff |
| Archivos relacionados | `obs_ai_runtime.py` |
| Siguiente acción | 1. Agregar tests unitarios por función; 2. Calibrar factores de estimate_R con datos reales; 3. Documentar como módulo publicable |
| Riesgo | Heurísticas no calibradas; no usar como producción hasta validación |
| Dependencia | Datos de calibración (historial de sesiones con R medido) |

---

## Proyecto 5: OSIT-M Experimental

| Campo | Valor |
|---|---|
| Estado | HIPÓTESIS FORMAL definida, experimento no iniciado |
| Objetivo | Validar correlación ε(R) vs R_est en tarea de detección de señal |
| Archivos relacionados | `MEDIOEVO_MEASUREMENT_OPERATOR_v0_1.md` |
| Siguiente acción | 1. Preregistrar experimento (EXP-1); 2. Protocolo TOJ + signal detection; 3. N=60 por grupo |
| Riesgo | Sin preregistro, cualquier resultado puede ser p-hacking |
| Dependencia | Recursos para experimento conductual; aprobación ética si hay participantes humanos |

---

## Proyecto 6: Sigma Validation

| Campo | Valor |
|---|---|
| Estado | PROTOCOLO MÍNIMO DEFINIDO |
| Objetivo | Medir Δt_min, R_est, sensory gain diferencial y correlación con AQ-10 |
| Archivos relacionados | `MEDIOEVO_SIGMA_COMPLETE_v0_2.md` |
| Siguiente acción | Preregistrar EXP-2 con hipótesis, dataset, métricas y umbrales antes de recopilar datos |
| Riesgo | Claims clínicos sin aprobación — gate activo |
| Dependencia | No usar como diagnóstico; solo como variable de investigación |

---

## Handoff
`PROYECTOS_ACTIVOS_v1.0|6-projects|canon-paper-app-runtime-exp|2026-05-07`


---

## Proyectos activos añadidos desde PRODUCTOS_MEDIOEVO

| Proyecto | Estado | Objetivo | Archivos relacionados | Siguiente acción | Riesgo |
|---|---|---|---|---|---|
| PRODUCTOS_MEDIOEVO | Activo | Ordenar frente comercial sin mover source canónico | `PRODUCTOS_MEDIOEVO/00_LEER_PRIMERO.md` | Crear `PRODUCT_MAP`, `VISIBILITY_MATRIX`, `RISK_REGISTER` si no existen en esta raíz | Mezcla comercial/canon/privado |
| Libros y Bundles | Activo | Bloque editorial 6+1 y catálogo ampliado | `01_LIBROS_Y_BUNDLES/README.md` | Mantener fuente de verdad en `libros.json` y storefront local | No publicar textos completos privados |
| Software Local | Activo | Claudio Full, Workbench, Pack Empresarial y módulos offline | `02_SOFTWARE_LOCAL/README.md` | Verificar empaques y gates comerciales | Gumroad/publicación requiere revisión |
| Open Source GitHub | Activo | Herramientas públicas: safe-exec, medioevo-tools, data-double-slit | `03_OPEN_SOURCE_GITHUB/README.md` | Mantener repos public-safe y escaneados | Licencia/secreto/publicación |
| Audiovisual y TCG | Parcial | Radiocinema, El Bardo, soundtrack, mapas, TCG | `04_AUDIOVISUAL_Y_TCG/README.md` | Separar TCG/privado de material publicable | Alto riesgo de mezcla privada |
| Betas | Pendiente | Radiocinema, COACH Pro, Creator Bundle, FlujoCRM | `05_BETAS_Y_PROXIMAMENTE/README.md` | Cerrar por evidencia local antes de venta | Producto no verificado |
| ClaudioOS Blueprint | Activo local | ISO Debian Live + Brain OS | `claudio_os_blueprint/README.md` | QEMU/Guardian/Mission Control/witness | No instalar en producción |
| Content Forge | Activo local | Render/campañas sin autopublicación | `content_forge/README.md` | QA ffprobe/visual y asset policy | Autopublicación bloqueada |

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
- Archivo maestro: `14_PROYECTOS_ACTIVOS.md`.
