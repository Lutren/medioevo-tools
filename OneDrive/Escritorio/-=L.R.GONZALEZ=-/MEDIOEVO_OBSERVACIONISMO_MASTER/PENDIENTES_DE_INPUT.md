# PENDIENTES_DE_INPUT

Estado: `NO_BLOQUEANTE`

## CERTEZA

- Existen fuentes pesadas o no-textuales: PDF, DOCX, ZIP, TAR.GZ, MP4, JPG.
- Existen fuentes conversacionales y archivos TXT largos que pueden contener variaciones útiles.
- Este pase generó una carpeta maestra trazable sin borrar ni mover fuentes.
- El pase `wabi.cerebro_line_audit.v2` extrajo `33` DOCX/PDF como texto y registró `0` errores de extracción de DOCX/PDF.
- `ReplitExport-lutren.tar.gz` fue procesado por intake cuarentenado: `215` textos indexados, `.git/cache` bloqueados, fuente original intacta.

## INFERENCIA

- El canon esencial ya está representado por los documentos 00-22.
- Las fuentes pesadas deben procesarse por prioridad y ficha, no por volcado completo.

## INCÓGNITA

| Pendiente | Motivo | Acción mínima |
|---|---|---|
| PDF/DOCX visuales | Ya fueron extraídos como texto, pero no revisados visualmente | Render/QA solo si un claim depende de diagramas, fórmulas o layout |
| ZIP/TAR.GZ/binarios restantes | Pueden contener código o docs duplicados; no todos fueron desempacados | Repetir intake cuarentenado por prioridad, sin extracción cruda ni movimiento de fuentes |
| `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md` en PRODUCTOS | Mencionados pero no encontrados en esa raíz | Crear o enlazar ruta canónica |
| Claims físicos P-06 a P-10 | Sin cómputo numérico | Mantener bloqueados hasta simulación |
| Claims cognitivos/Sigma | Sin validación/preregistro | Usar lenguaje fenomenológico |
| Publicación externa | Requiere seguridad/legal/visibilidad | Mantener REVIEW/BLOCK |

## ACCIÓN

Siguiente pase recomendado: revisar el intake de `ReplitExport-lutren.tar.gz` y convertir solo módulos propios útiles en contratos/tests antes de importarlos.

## ARTEFACTO

Lista de huecos no bloqueantes para continuar sin preguntar.

---

## Corte Formal to PSI - 2026-05-08

Estado: `NO_BLOQUEANTE_CON_GATE`

### CERTEZA

- `C:\Users\L-Tyr\OneDrive\Escritorio\Formal` fue fichado como inbox nuevo.
- Conteo actual re-verificado: `50` archivos.
- Duplicados exactos por SHA256 contra `-=PSI=-`, `MEDIOEVO_OBSERVACIONISMO_MASTER` y `runtime/cerebro_master_index`: `0`.
- Se crearon cinco artefactos en `docs/intake/`.
- No se movio, borro, renombro, importo ni ejecuto ningun archivo de `Formal`.

### INFERENCIA

- `Formal` contiene deltas potenciales para teoria formal, Observacionismo Inverso, contratos de agente y evidencia de experimentos.
- Tambien contiene patrones de ejecucion directa que deben quedar como requisitos negativos para SafeExecutor/GhostGate.

### INCOGNITA / PENDIENTES

- [x] Formal P1: comparar `report.md`, `Auto.txt`, `BIBLIA_MEDIOEVO_Canon_Unificado.pdf`, `OI_P6R_paper_v0_1.md` y `paper_observacionismo_inverso.md` contra documentos 00-22 y `16_CLAIMS_REGISTER.md`. Evidencia: `docs/intake/FORMAL_CLAIMS_EXCERPT_COMPARISON_2026-05-13.md`; no se muto claim register.
- [x] Formal P1: comparar `medioevo_agent_core.py`, `medioevo_core_v01.py`, `Completar04-07.txt` y `PR11.txt` contra contratos Wabi/Sabi antes de cualquier import. Evidencia: `docs/intake/FORMAL_WABI_CONTRACT_COMPARISON_2026-05-13.md` y `apps/local/wabi-sabi/tests/test_formal_contract_intake.py`.
- [x] Formal P1: hacer archive-intake cuarentenado de `medioevo_info_chemistry_v0_2.zip` y `medioevo_prompt_compression_experiment_bundle.zip`. Evidencia: `docs/intake/FORMAL_ARCHIVE_INTAKE_2026-05-13.md`, SHA256 registrados, sin extraccion.
- [x] Formal P1: hacer QA visual solo de PDF/PNG que sustenten claims o figuras necesarias. Resultado: `NO_REQUERIDA_EN_ESTE_PASE`; `BIBLIA_MEDIOEVO_Canon_Unificado.pdf` tiene texto extraible (`pypdf`, 16 paginas, no cifrado) y ningun delta dependio de figura/layout. Evidencia: `docs/intake/FORMAL_CLAIMS_EXCERPT_COMPARISON_2026-05-13.md`.
- [x] Formal P2: proponer parche pequeno a `16_CLAIMS_REGISTER.md` solo para deltas confirmados y no duplicados. Evidencia: `docs/intake/FORMAL_CLAIMS_EXCERPT_COMPARISON_2026-05-13.md` propone `I-10`, `I-11` y `A-10` como patch aditivo de bajo reclamo; no se muto el claim register.
- [x] Formal P3: nominar archivos a `DELETE_CANDIDATES.md` solo despues de prueba de no-insight/no-codigo/no-evidencia y gate de limpieza. Resultado: `NO_DELETE_CANDIDATES_NOMINATED`; ningun archivo cumple todas las precondiciones de limpieza. Evidencia: `docs/intake/FORMAL_DELETE_CANDIDATES_GATE_2026-05-13.md`.

### ACCION

Siguiente paso verificable: ejecutar la comparacion de excerptos de los cinco candidatos canonicos contra el master y producir un parche minimo de claims o una decision `NO_DELTA`.

### ARTEFACTO

- `docs/intake/FORMAL_TO_PSI_INTAKE_2026-05-08.md`
- `docs/intake/FORMAL_DUPLICATES_REVIEW_2026-05-08.md`
- `docs/intake/FORMAL_CODE_INSIGHTS_2026-05-08.md`
- `docs/intake/FORMAL_CLAIMS_DELTA_2026-05-08.md`
- `docs/intake/FORMAL_CLEANUP_GATE_2026-05-08.md`

---

## Corte Wabi/Sabi, Claudio y provider secrets - 2026-05-08

Estado: `LOCAL_GATEWAY_READY_CON_CLOUD_BLOQUEADO`

### CERTEZA

- `Formal\banananana.txt` fue clasificado como `PRIVATE_SECRET_CONFIG`, no como codigo, claim ni canon.
- Wabi/Sabi responde con `provider-status`, `chat` y `auto /status`.
- Ollama local esta disponible con `qwen2.5-coder:3b` y `qwen2.5:0.5b`; los modelos cloud de Ollama siguen filtrados.
- NVIDIA NIM y Qwen cloud existen como adapters mockeables en Wabi/Sabi, pero estan bloqueados por defecto.
- Claudio tiene gateway local a Wabi/Sabi en `core/wabi_gateway.py`; no concede autonomia ni imprime secretos.

### INFERENCIA

- El valor fuerte es la capa de control observacionista: redaccion de secretos, gates, provider fallback, contratos de agente y evidencia.
- La modificacion de pesos/modelos queda fuera de alcance hasta tener dataset, metricas, falsadores y host gate `APPROVE`.

### INCOGNITA / PENDIENTES

- [x] Wabi P1: probar tarea real sin Ollama usando `WABI_DISABLE_BASE_MODEL=1` y verificar fallback `codex/dry-run` sin escritura peligrosa. Evidencia: `python -m wabi_sabi.cli.main auto ... --dry-run --codex-provider dry-run --json`, `provider_order=["dry-run"]`, artifact `runtime/wabi_sabi/dryrun_no_ollama_2026-05-13/outputs/wabi_codex_workpack_20260513-024232.json`.
- [x] Wabi P1: decidir si existe key Qwen/DashScope real; `banananana.txt` mostro senal Aliyun AccessKey pero no una key DashScope/Qwen especifica; si existe, registrarla solo como presencia redactada, nunca como valor. Decision: `QWEN_MISSING_BEARER_CONFIRMED`; no `DASHSCOPE_API_KEY` ni `QWEN_API_KEY` presente por nombre, sin imprimir valores. Evidencia: `docs/ops/WABI_QWEN_REDACTED_PRESENCE_2026-05-13.md`.
- [x] Wabi P1: crear fixture de evaluacion observacionista para comparar respuesta local, dry-run y cloud mock. Evidencia: `apps/local/wabi-sabi/tests/test_observacionista_evaluation_fixture.py`.
- [x] Claudio P1: conectar una llamada interna de lectura al gateway solo donde no duplique `model_router.py`. Evidencia: `/api/providers/status` agrega `wabi_gateway` desde `core.wabi_gateway.get_wabi_gateway_status`, sin tocar `model_router.py`; `python -m pytest tests\test_wabi_gateway.py tests\test_claudio_api_server_assets.py::test_main_server_provider_status_includes_wabi_gateway_read -q` -> `7 passed`; `python -m pytest tests\test_claudio_api_server_assets.py::test_main_server_provider_contracts_route tests\test_model_router_api.py -q` -> `4 passed`.
- [x] Formal P1: comparar los dos Python de `Formal` contra `wabi_sabi/core/gate.py`, `safe_executor.py`, `rollback_store.py`, `decision_log.py` y `eml.py`. Evidencia: `docs/intake/FORMAL_WABI_CONTRACT_COMPARISON_2026-05-13.md` y prueba focal `test_formal_contract_intake.py`.
- [x] Secret P0: cerrar por owner override sin leer/imprimir valores: `banananana.txt` queda `CLOSED_KEEP_PRIVATE_REDACTED`, sin limpieza ni uso real; evidencia en `docs/pending/OWNER_OVERRIDE_PROVIDER_SECRET_CLOSEOUT_2026-05-13.md`.

### ARTEFACTO

- `docs/intake/FORMAL_TECH_VALUE_SCOPE_2026-05-08.md`
- `docs/intake/FORMAL_SECRET_PROVIDER_INTAKE_2026-05-08.md`
- `docs/ops/WABI_CLAUDIO_PROVIDER_GATE_2026-05-08.md`

### ACTUALIZACION - modelos cloud para programar

- [x] Wabi P1: registrar aliases NVIDIA NIM para `ultra`, `llama-70b`, `super`, `nano-30b` y `nano-9b` sin activar red.
- [x] Wabi P1: registrar aliases Qwen cloud para `qwen-plus` y `qwen-235b` sin activar red.
- [x] Wabi P1: exponer catalogo en `provider-status --json` con redaccion de secretos.
- [x] Wabi P1: validar resolucion de aliases con HTTP mock, no con llamadas reales.
- [x] Wabi P0: activar `WABI_ALLOW_CLOUD_PROVIDERS=1` solo en sesion gated y con prompt inocuo de smoke para NVIDIA.
- [x] Claudio P1: probar llamada real `Claudio -> Wabi -> NVIDIA NIM` con alias `super`; resultado `OK`.
- [x] Secret P0: verificar que el token NGC/Docker de `banananana.txt` no sirve como NIM bearer actual (`401`).
- [x] Wabi P0: cerrar por owner override como `CLOSED_DO_NOT_USE_ULTRA`: NVIDIA env presente, `super` tuvo smoke historico OK, `ultra` queda no usado/no sostenido por costo/cuenta; evidencia en `docs/pending/OWNER_OVERRIDE_PROVIDER_SECRET_CLOSEOUT_2026-05-13.md`.
- [x] Wabi P0: cerrar por owner override como `CLOSED_QWEN_DISABLED_NO_BEARER`: `DASHSCOPE_API_KEY` y `QWEN_API_KEY` ausentes, Qwen cloud queda desactivado; evidencia en `docs/pending/OWNER_OVERRIDE_PROVIDER_SECRET_CLOSEOUT_2026-05-13.md`.
- [x] Claudio P1: convertir `medioevo_agent_core.py` y `medioevo_core_v01.py` en contratos/tests pequenos antes de importar logica. Evidencia: contratos Wabi/Sabi en `test_formal_contract_intake.py`; no se importo logica de Formal.
