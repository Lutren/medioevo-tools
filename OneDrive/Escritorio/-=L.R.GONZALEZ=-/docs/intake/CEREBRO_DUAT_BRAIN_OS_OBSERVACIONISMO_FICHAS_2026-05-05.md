# Fichas CEREBRO / DUAT / Brain OS / Observacionismo

Fecha: `2026-05-05`

Estado: `CURADURIA_OPERATIVA / NO_PUBLICACION_DIRECTA`

Estas fichas consolidan tecnologia y teoria util sin mover fuentes crudas ni duplicar runtime. Cada item queda con sistema, origen, estado epistemico, riesgo, evidencia, falsadores y proxima accion.

## Ficha 1 - CEREBRO / PSI Canon Humano

| campo | valor |
|---|---|
| sistema | Sistema Cognitivo; Memoria/Hipocampo |
| origen | `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-`, `-=PSI=-`, `00_LEER_PRIMERO_HUMANO.md` |
| estado epistemico | `CERTEZA`: ruta e indice existen; `REVIEW`: publicacion completa bloqueada |
| riesgo | mezcla canon, libro, teoria formal, PDFs/DOCX, ZIPs, prototipos y fuentes crudas |
| evidencia | indice humano leido; `00_FICHA_TECNICA_PSI_2026-05-05.md`; extensiones formales 15-18 |
| falsadores | fuente cruda tratada como canon; libro completo en carril abierto; claim fuerte sin estado |
| proxima accion | usar `01_MAPA_SISTEMAS_CEREBRO_DUAT_BRAIN_OS_2026-05-05.md` como entrada por sistemas |

## Ficha 2 - Brain OS / Kernel Cognitivo Local

| campo | valor |
|---|---|
| sistema | Sistema Cognitivo; Sistema Nervioso |
| origen | `claudio\core\brain_os_bridge.py`, `claudio\core\brain_os_kernel.py`, `claudio\tools\brain_os_cli.py` |
| estado epistemico | `CERTEZA_OPERATIVA` |
| riesgo | confundir runtime vivo con ISO final o permiso de acciones externas |
| evidencia | `python tools\brain_os_cli.py status` -> `ok=true`; `kernel-boot-audit` -> `event_id=107`, `decision=allow`, `state=listo`, `missing_required=[]` |
| falsadores | required component missing; API/kernel down; watchdog no vivo; boot audit `hold` |
| proxima accion | mantener `docs\BRAIN_OS_MASTER_PLAN_STATUS.md` y separar siempre kernel local de PC2/ISO humano-gated |

## Ficha 3 - DUAT GEODIA OS Propio

| campo | valor |
|---|---|
| sistema | Sistema Musculoesqueletico; Sistema Nervioso |
| origen | `claudio\os\duat_geodia_kernel`, `tools\duat_geodia_os_orchestrator.py`, `tools\duat_geodia_iso_builder.py` |
| estado epistemico | `CERTEZA_OPERATIVA_LOCAL` |
| riesgo | sobreclaim comercial/publico; confundir con DUAT Genesis publico o DUAT Living Matrix v0.6 |
| evidencia | `runtime\duat_geodia_os\latest_report.md`: `full_os_bootable=True`, `publication_allowed=False`; `runtime\duat_geodia_iso\latest_report.md`: QEMU CD-ROM boot `True`, SHA256 `e51a7b89dad1b643a3f96d21334acd191b705feb66311c7f8e5fcf62b0141425` |
| falsadores | QEMU sin marcadores; ISO sin firma/boot catalog; `observacion_engineering_gate` no `APPROVE`; hash cambia sin razon |
| proxima accion | siguiente rebanada tecnica: teclado IRQ1 real, memoria fisica/allocator, syscalls/scheduler |

## Ficha 4 - Observacion Engineering / Regulacion

| campo | valor |
|---|---|
| sistema | Sistema Endocrino/Regulacion; Sistema Inmunologico |
| origen | `claudio\core\observacion_engineering.py`, `tests\test_observacion_engineering.py` |
| estado epistemico | `CERTEZA_OPERATIVA` para gates; `PROXY` para formulas no calibradas |
| riesgo | promover proxies como ciencia, seguridad garantizada o autonomia sin evidencia |
| evidencia | suite focal `12 passed`; formulas documentadas en `18_MATRIZ_MATEMATICA_OPERATIVA_2026-05-05.md` |
| falsadores | gate aprueba sin evidencia; GhostGate no bloquea residuo futuro; `lambda_sat` no degrada riesgo |
| proxima accion | alimentar calibracion con outcomes reales antes de relajar autonomia local |

## Ficha 5 - DUAT Living Matrix v0.6

| campo | valor |
|---|---|
| sistema | Sistema Digestivo/Metabolico; GEODIA research |
| origen | `Downloads\duat_living_matrix_v06 (1).zip`, ficha `claudio\docs\DUAT_LIVING_MATRIX_GEODIA_INTAKE_2026-05-03.md` |
| estado epistemico | `CERTEZA` como fuente preferente; `REVIEW` como producto |
| riesgo | v0.5 trae SQLite/bloqueos; v0.6 no autoriza publicacion por si sola; posible confusion con DUAT GEODIA OS |
| evidencia | hash `A87F0905EEE1D09FD89414D135036E0EEACA9B88C33AA08B133D977FDCBCE51E`; prueba temporal v0.6 `7 passed`; v0.5 falla por SQLite lock |
| falsadores | smoke visual falla; dependencias sin ficha; claims de prediccion o ciencia aparecen en copy |
| proxima accion | smoke visual UI v0.6 y decidir beta privada/comercial/lab, manteniendo `SYNTHETIC_ONLY` |

## Ficha 6 - Observacionismo L0/L1 Language

| campo | valor |
|---|---|
| sistema | Sistema Nervioso; Sistema Circulatorio |
| origen | `research\observacionismo-lab`, `docs\developer\OBSERVACIONISMO_MINIMAL_MACHINE_LANGUAGE_2026-05-05.md` |
| estado epistemico | `CERTEZA_OPERATIVA_LOCAL` |
| riesgo | tratar lenguaje como verdad ejecutable fuera de tests o absorber trabajo concurrente |
| evidencia | orquestador DUAT corrio tests del lab: `7 passed`; contrato SETO marca lane concurrente |
| falsadores | parser/VM no reproducen transiciones; agente usa lenguaje para write/publicacion sin ActionGate |
| proxima accion | dejar a lane owner continuar parser L1; otros agentes solo leen por handoff |

## Ficha 7 - Wabi-Sabi / Sentido Comun / Stewardship Local

| campo | valor |
|---|---|
| sistema | Sistema Endocrino/Regulacion; Sistema Circulatorio |
| origen | Claudio runtime Wabi-Sabi, Sentido Comun y scheduler benchmark |
| estado epistemico | `CERTEZA_OPERATIVA_LOCAL` para coordinacion; `REVIEW` para autonomia |
| riesgo | usar politica local para pesos, alias Ollama, borrado, publicacion o decisiones legales |
| evidencia | orquestador DUAT corrio `tools\wabi_sabi_scheduler_benchmark.py` con retorno `0`; docs Claudio del 2026-05-05 registran policy-only |
| falsadores | ledger hash-chain roto; casos sin fuente/hash/falsadores; ActionGate ignorado |
| proxima accion | registrar outcomes reales y mantener `LOCAL_REVIEW_ONLY` hasta evidencia limpia |

## Ficha 8 - Publicacion Externa

| campo | valor |
|---|---|
| sistema | Sistema Inmunologico |
| origen | `RISK_REGISTER.md`, `VISIBILITY_MATRIX.md`, `runtime\duat_geodia_os\latest_report.md` |
| estado epistemico | `BLOCK` |
| riesgo | push, Gumroad, deploy, redes, GitHub o packaging por glob amplio con secretos/private IP/claims |
| evidencia | `external_publication` en orquestador: `BLOCK`; workspace global secret scan legacy sigue bloqueando glob amplio |
| falsadores | target allowlist especifico con secret scan 0, path scrub, claims scan, license boundary y ActionGate `APPROVE` |
| proxima accion | no publicar desde esta rebanada; preparar solo copy low-claim si se pide luego |

## Resumen De Bloqueos

- `BLOCK`: publicacion externa; claims cientificos fuertes; RPG/TCG/libros completos; secretos; borrado sin ficha.
- `REVIEW`: DUAT Living Matrix como producto; programador-agente con write automation; autonomia Wabi-Sabi; fuentes crudas.
- `READY_LOCAL`: Brain OS boot contract, DUAT kernel/ISO local, Observacion Engineering gates, GEODIA offline fixtures.
