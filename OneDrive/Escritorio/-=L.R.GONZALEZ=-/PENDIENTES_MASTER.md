# PENDIENTES_MASTER

## 2026-05-31 - Consolidación Wabi + mejoras sistémicas

Status: Wabi-Sabi consolidado a un solo tronco. Mejoras múltiples ejecutadas.

| item | estado | evidencia |
|---|---|---|
| Wabi-Sabi consolidation | CERRADO | `apps/local/wabi-sabi` → `_archive/legacy/wabi-sabi-legacy-2026-05-31/`; canónico en BRAIN_OS `02_CLAUDIO/wabi_sabi` |
| FlujoCRM checks | CERRADO_VERIFICADO | `npm run check` 5/5 PASS (2026-05-31) |
| CI/CD pre-commit hooks | CREADO | `.githooks/pre-commit` con secret scan + python syntax + node check; `git config core.hooksPath .githooks` |
| REPO_MANIFEST.json | CREADO | consolidación de VISIBILITY_MATRIX + PRODUCT_MAP + RISK_REGISTER en un solo JSON |
| obsai-core README | MEJORADO | quick start, capabilities table, CLI docs más estratégicos |
| duat-genesis README | MEJORADO | claims boundary más visible |
| Cross-product integration | DOCUMENTADO | `docs/architecture/CROSS_PRODUCT_INTEGRATION_2026-05-31.md` |
| obsai-core tests | VERIFICADO | `72 passed in 4.23s` |
| Decisiones registradas | DECISIONS.md | Wabi consolidation añadida |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Fragmentos cover asset & Gumroad | REVIEW_ASSET_PRODUCTION | requiere portada + revisión humana |
| FlujoCRM clean-machine QA | REVIEW_CLEAN_VM | requiere máquina limpia Windows |
| FlujoCRM legal/support review | REVIEW_LEGAL | requiere humano |
| FlujoCRM code signing | REVIEW_SIGNING | requiere certificado o decisión unsigned |
| Fragmentos publicación | BLOCK_PUBLICATION | hasta cover + QA + legal + humano |
| Publicación GitHub obsai-core | REVIEW_PUBLICATION | requiere ActionGate + secret scan + PRIVATE_EXCLUSIONS |

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi `/api/chat/message`

Status: sincronizado. La cola principal sigue en
`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-`.

| item | estado | evidencia |
|---|---|---|
| Wabi UI chat modelo/hora | CERRADO_EN_BRAIN_OS | `/api/chat/message` -> `online_ai_called=True`, modelo real, reloj clause |
| Suite Wabi relevante | CERRADO_TESTS | `281 passed` |
| Suite Claudio full | CERRADO_TESTS | `836 passed` |
| Consolidar dos árboles Wabi | REVIEW_REQUIRED | requiere decisión de tronco canónico |
| Router por costo / early-exit | REVIEW_REQUIRED | requiere RFC/tests local-first |

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi chat cloud identity

Status: sincronizado. La cola principal sigue en
`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-`.

| item | estado | evidencia |
|---|---|---|
| Wabi chat identidad de modelo | CERRADO_EN_BRAIN_OS | Helper/prompt/fallback/flag actualizados; full tests `836 passed` |
| Smoke CLI vivo | CERRADO_PROVIDER_LLM | `wabi ask "que modelo eres y que hora es"` -> `nvidia/nvidia/nemotron-3-super-120b-a12b`, sin reloj |
| Smoke UI vivo | CERRADO_PROVIDER_LLM | `/api/conversation/turn` -> `cloud=True`, modelo presente, reloj clause presente, `forbidden_mentions=[]` |
| Snapshot tecnico LRG final | CERRADO_SIN_PENDIENTES_ACTIVOS | `pending_review.py --write --quiet` -> `active_dedup=0`, `claudio_open=0` |

No reabrir en este root sin target concreto. Publicacion/push/deploy/apply y
borrado destructivo siguen bloqueados.

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi Programmer delegation

Status: sincronizado. La cola principal sigue en
`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-`.

| item | estado | evidencia |
|---|---|---|
| Snapshot tecnico LRG | CERRADO_SIN_PENDIENTES_ACTIVOS | `pending_review.py --write --quiet` -> `active_dedup=0`, `claudio_open=0` |
| Wabi Programmer CLI SafeExecutor delegation | CERRADO_EN_BRAIN_OS | `-= BRAIN_OS =-\02_CLAUDIO\docs\RFC_WABI_PROGRAMMER_CLI_SAFEEXECUTOR_DELEGATION_v0_1.md`; full tests `822 passed` |

No reabrir en este root sin target concreto. Publicacion/push/deploy/provider live siguen bloqueados.

## 2026-05-22 - Espejo tecnico de BRAIN_OS principal

Status: sincronizado. La cola principal de pendientes/handoffs queda en
`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-`.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Snapshot tecnico | CERRADO_SIN_PENDIENTES_ACTIVOS | `python tools\release\pending_review.py --write --quiet` -> `active_dedup=0`, `claudio_open=0` |
| Ruta principal | CERRADO_SYNC | `-= BRAIN_OS =-\RUTA_PRINCIPAL_BRAIN_OS_2026-05-22.md` |
| Wabi alias drift | CERRADO_TESTS | `nemotron-nvidia` -> `nvidia/nemotron-3-super-120b-a12b`; Wabi suite `439 passed` |

### Regla

Este archivo queda como espejo tecnico. No reabrir pendientes cerrados en
BRAIN_OS sin evidencia nueva o target concreto.

## 2026-05-22 - Fragmentos Cover Asset Gate

Status: cerrado localmente como gate de revision. No se creo asset, no se
selecciono imagen y no se ejecuto publicacion.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Validador local de cover asset | CERRADO_TOOLING | `tools\release\validate_cover_asset_gate.py`; `python -m py_compile` PASS |
| Pruebas focales del gate | CERRADO_TESTS | `tests\release\test_validate_cover_asset_gate.py` -> `3 passed` |
| Manifest/reporte Fragmentos sin asset | CERRADO_REVIEW_GATE | `qa_artifacts\editorial_cover_gate\FRAGMENTOS_COVER_GATE_20260522`; `overall_status=REVIEW_ASSET_MISSING`, findings `LICENSE_STATUS_REVIEW_REQUIRED`, `REVIEW_ASSET_MISSING` |
| Secret scan focal sobre artefactos del gate | CERRADO_SCAN | `scan_secrets.py --artifact ...` -> `count_reported=0` |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Generar o seleccionar portada real | REVIEW_ASSET_PRODUCTION | Requiere decision humana, asset concreto, procedencia/licencia y plataforma destino. |
| Licencia/procedencia del asset | REVIEW_LICENSE_PROVENANCE | Hasta que `license_status` sea `owned`, `licensed` o `owned_or_cleared_for_internal_review`. |
| KDP/Gumroad/web/redes/push/deploy/public ZIP | BLOCK_PUBLICATION | El gate solo prepara revision local; no autoriza acciones externas. |

## 2026-05-22 - Human gate packet y cover brief Fragmentos

Status: cerrado localmente como preparacion de revision humana. No se creo
asset ni se ejecuto publicacion.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Packet humano Fragmentos/Calibracion | CERRADO_REVIEW_PACKET | `docs\publishing\FRAGMENTOS_CALIBRACION_HUMAN_PUBLICATION_GATE_PACKET_2026-05-22.md`, JSON parse OK, secret scan `count_reported=0` |
| Brief portada public-safe Fragmentos | CERRADO_COVER_BRIEF | `docs\publishing\FRAGMENTOS_PUBLIC_SAFE_COVER_BRIEF_2026-05-22.md`, JSON parse OK, secret scan `count_reported=0` |
| Boundary de publicacion | CERRADO_GATE_DOCS | `PublicationGate=BLOCK`, `ActionGate=REVIEW_HUMAN_EDITORIAL`, `REVIEW_ASSET_PRODUCTION` |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Generar o seleccionar portada real | REVIEW_ASSET_PRODUCTION | Requiere revision humana de direccion visual, procedencia/licencia y plataforma destino. |
| Staging publico local allowlisted | REVIEW_PUBLIC_STAGING | Solo despues de elegir un libro, asset y copy aprobado. |
| KDP/Gumroad/web/redes/push/deploy/public ZIP | BLOCK_PUBLICATION | No ejecutar sin gate explicito por target. |

## 2026-05-22 - QA Word/PDF full-page Fragmentos y Calibracion

Status: cerrado como cobertura visual automatizada completa. No autoriza
publicacion.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Convertir DOCX Fragmentos con Word local y renderizar todas las paginas | CERRADO_AUTOMATED_FULL_COVERAGE | `qa_artifacts\editorial_docx_word_visual_qa\EDITORIAL_DOCX_WORD_FULL_QA_20260522`, Word pages `688`, rendered pages `688`, blank `0`, edge `0` |
| Convertir DOCX Calibracion con Word local y renderizar todas las paginas | CERRADO_AUTOMATED_FULL_COVERAGE | `qa_artifacts\editorial_docx_word_visual_qa\EDITORIAL_DOCX_WORD_FULL_QA_20260522`, Word pages `477`, rendered pages `477`, blank `0`, edge `0` |
| Contact sheets internos | CERRADO_AUTOMATED_REVIEW_AID | Fragmentos `35` contact sheets; Calibracion `24` contact sheets |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Revision humana final para venta/tienda/impresion | REVIEW_HUMAN_EDITORIAL | La cobertura automatizada no sustituye criterio editorial humano antes de KDP/Gumroad/store. |
| Publicacion, upload, push, deploy o ZIP publico | BLOCK_PUBLICATION | Los DOCX, PDFs, PNGs y contact sheets contienen material privado completo. |

## 2026-05-22 - QA split DOCX Fragmentos y Calibracion

Status: smoke interno ejecutado con limites. No se declara aprobacion visual
completa.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Smoke render DOCX Fragmentos | CERRADO_PARCIAL_REVIEW | `qa_artifacts\editorial_docx_visual_qa\FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`, `53` paginas PNG parciales; render completo `artifact-tool` no termino en ventana controlada |
| Smoke render DOCX Calibracion | CERRADO_PARCIAL_REVIEW | `qa_artifacts\editorial_docx_visual_qa\CALIBRACION_INTERNAL_EXPORT_2026-05-22`, `19` paginas PNG parciales; render completo `artifact-tool` no termino en ventana controlada |
| QA representativa desde PDF integrado | CERRADO_SMOKE_REPRESENTATIVO | `qa_artifacts\editorial_docx_visual_qa\EDITORIAL_INTERNAL_EXPORTS_SPLIT_QA_20260522\EDITORIAL_DOCX_SPLIT_QA_REPORT_2026-05-22.md`; paginas PDF representativas sin candidatos blanco/borde |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Aprobacion visual DOCX pagina por pagina | REVIEW_VISUAL_FULL | Requiere renderer por rangos o revision manual Word/LibreOffice; no se cerro en esta sesion. |
| Publicacion o assets store-ready derivados | BLOCK_PUBLICATION | Los exports y QA contienen material privado; no publicar ni subir. |

## 2026-05-22 - Export interno Fragmentos y Calibracion

Status: cerrado localmente con evidencia. El snapshot canonico de pendientes
se refresco y queda en `active_dedup=0`, `claudio_open=0`.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Export interno equivalente para Fragmentos | CERRADO_EXPORT_INTERNO | `books\editorial\internal_exports\FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`, `INTERNAL_EXPORT_MANIFEST.json`, hash check `hash_ok=True` |
| Export interno equivalente para Calibracion | CERRADO_EXPORT_INTERNO | `books\editorial\internal_exports\CALIBRACION_INTERNAL_EXPORT_2026-05-22`, `INTERNAL_EXPORT_MANIFEST.json`, hash check `hash_ok=True` |
| Snapshot canonico de pendientes | CERRADO_SIN_PENDIENTES_ACTIVOS | `docs\pending\PENDING_REVIEW_2026-05-22.md`, `qa_artifacts\pending\pending_review_2026-05-22.json` |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Uso publico de `books\editorial\internal_exports` | BLOCK_PUBLICATION | No copiar a GitHub, Gumroad, KDP, web, redes, ZIP publico, staging publico ni release externo sin gate nuevo. |
| Revision editorial/portadas/listings/store assets | REVIEW_ASSET_PRODUCTION | Requiere revision humana/editorial; los exports son material privado de lectura/revision local. |
| Legal/licencia/comercializacion | REVIEW_LEGAL_COMMERCIAL | All rights reserved; no cambia licencia ni autoriza venta/publicacion. |

## Siguiente accion verificable

Si el proximo `pending_review.py` sigue en cero, trabajar solo un gate
REVIEW explicito: QA visual DOCX split para Fragmentos/Calibracion, brief de
portada interno, o revision humana/editorial. No hacer upload, KDP, Gumroad,
web, redes, push, deploy ni ZIP publico.

## 2026-05-17 - Reconciliacion de Local Queue Closeout

Status: reconciliado contra evidencia local. Este archivo ya no usa checkboxes
para gates permanentes porque `pending_review` los interpreta como trabajo local
ejecutable.

### Cierres con evidencia

| item | estado | evidencia |
|---|---|---|
| Review metodologica WDI antes de interpretar comparabilidad o resultados predictivos | CERRADO_LOCAL_REVIEW | `research/duat-predictive-registry/reports/duat-world-bank-wdi-governance-review-v0-8-1.json`, `TEST_REPORT.md`, `docs/ops/MEDIOEVO_LOCAL_QUEUE_CLOSEOUT_2026-05-15.md` |
| Mantener los otros 31 libros como backlog etiquetado por asset/status | CERRADO_INVENTARIO | `docs/publishing/BOOK_PUBLICATION_CONTROL_BOARD_2026-05-15.md`, `docs/publishing/BOOK_PUBLICATION_MISSING_ASSETS_2026-05-15.md` |
| Aislar arbol git sucio antes de cualquier commit path-scoped | CERRADO_AISLAMIENTO_LOCAL | `docs/ops/GIT_WORKTREE_ISOLATION_2026-05-17.md`; no se hizo commit ni staging |
| MTS solo con preregistro previo, sin modificar modelo, labels ni holdout | CERRADO_LOCAL_SINTETICO | `docs/ops/MEDIOEVO_LOCAL_QUEUE_CLOSEOUT_2026-05-15.md`, `TEST_REPORT.md`, `ACTION_GATES.md` |
| Paquete local de revision para Deriva, Fragmentos y Calibracion | CERRADO_PAQUETE_INTERNO | `docs/publishing/BOOK_RELEASE_REVIEW_PACKET_DERIVA_FRAGMENTOS_CALIBRACION_2026-05-17.md` |

### Gates que permanecen abiertos

| item | gate | regla |
|---|---|---|
| Review legal/humana de World Bank/WDI antes de redistribucion o claim externo | REVIEW_EXTERNAL | No se puede cerrar localmente. Mantener `PublicationGate=BLOCK` para redistribucion o claim externo. |
| Exports, portada KDP/public-ready y checklist de tienda para Deriva, Fragmentos y Calibracion | REVIEW_ASSET_PRODUCTION | El paquete interno queda listo, pero los assets finales requieren revision humana/editorial y no autorizan upload. |
| Publicacion, upload, deploy, git push, Gumroad, KDP, redes o ZIP publico | BLOCK_PUBLICATION | Requiere gate nuevo y explicito por target. |
| Exposicion de manuscritos privados, canon privado, secretos, tokens o rutas sensibles | BLOCK_PRIVACY | No publicar ni copiar contenido privado a paquetes publicos. |
| Uso de sensores reales, datos personales, telemetria, camara, microfono, ubicacion o biometria en MTS | BLOCK_MTS_REAL_DATA | Solo se permite evidencia sintetica/local ya preregistrada. |

## Cierre adicional ejecutado

Deriva ya tiene export interno local en `books\editorial\internal_exports\DERIVA_INTERNAL_EXPORT_2026-05-17` con MD/HTML/DOCX/PDF/EPUB, manifiesto hash y `PublicationGate=BLOCK`.

## Siguiente accion verificable

Crear export interno equivalente para Fragmentos o Calibracion, o preparar brief de portada interno para Deriva; no hacer upload, KDP, Gumroad, web, redes, push ni ZIP publico.
