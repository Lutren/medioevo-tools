## 2026-05-15 - DUAT Dual-Lane Predictive Registry v0.1
- Fecha UTC: 2026-05-15T03:02:47Z
- Estado: DUAT Multidimensional Filter Ecology + Predictive Registry v0.1 implementado localmente.
- Fuentes catalogadas: 29; metodos: 17; filtros: 10.
- Tests: DUAT registry 20 passed; GEODIA regression 53 passed.
- Scans: FAIL.
- Gate: publication_gate=BLOCK; external_publication=false; no keys used or printed.
- Nota: pending_review active_dedup=1 queda en REVIEW tracker, no en bloqueo de implementacion local.
- Proxima accion verificable: escoger un objetivo predictivo concreto y correr benchmark R_before/R_after.

## 2026-05-15 - GEODIA Public-Safe Candidate v0.1
- Fecha UTC: 2026-05-15T01:34:07Z
- Estado: GEODIA Public-Safe Package Candidate v0.1 creado como artefacto local de revision.
- Zip local: `qa_artifacts/release_validation/geodia-public-safe-candidate-v0-1.zip`.
- SHA256: `719ca8a7ef4c7439fe8859b5894483afa062c2b88883303fd5e0628fa9de0e43`.
- Excluye: raw XLSX, fixtures reales, rutas privadas, source vaults, privados/RPG/TCG y runtime privado.
- Incluye: README public-safe, claims boundary, attribution/terms review, source card INEGI sanitizada, QA summary, manifest, ejemplo sintetico de fixture.
- Gate: publication_gate=BLOCK; external_publication=false; human/legal review REQUIRED.
- Proxima accion verificable: revision humana/legal y decision A/B/C/D del candidate.

## 2026-05-14 - GEODIA Internal RC v0.1
- Fecha: 2026-05-14T22:17:54Z
- Estado: GEODIA internal RC v0.1 documentado para revision humana/legal.
- Evidencia: tres fixtures oficiales, wrapper QA offline, source card INEGI, hashes y human review packet.
- Gate: publication_gate=BLOCK; public_safe_package_created=false; external_publication=false.
- Proxima accion verificable: revision humana del packet y decision entre paquete public-safe, modulo interno o cuarto fixture oficial.

# Estado De Proyectos, Apps Y Herramientas - 2026-05-14

Estado generado desde documentos locales vigentes, pending review, product map,
release readiness, test reports y handoffs. No autoriza publicacion, push,
deploy, borrado ni uso de credenciales.

## Resumen Ejecutivo

- Backlog local operativo: `0` pendientes deduplicados; Claudio: `0`.
- Estado global: cierre local por carriles validado; targets externos nuevos
  siguen en `REVIEW/BLOCK` hasta ActionGate especifico.
- Riesgo global: workspace sucio y scan global legacy no apto para publicacion
  directa; solo usar allowlists por producto.
- Nueva fuente DUAT: `awesomedata/awesome-public-datasets` queda registrada como
  indice de descubrimiento, no como dataset ejecutable ni licencia downstream.
- GEODIA ya tiene dos fixtures oficiales offline: World Bank Mexico 2018-2023 y
  Eurostat Germany 2018-2023; la comparacion multi-source queda en
  `INFERENCIA` con `publication_gate=BLOCK`.
- GEODIA Harmonization v0.1 ya existe: schema, crosswalk, modulo, tests y
  reporte local; no genera rankings ni claims sociales.
- GEODIA Harmonization CLI v0.1 ya regenera el reporte local desde fixtures
  offline + crosswalk + schema, sin red y con `publication_gate=BLOCK`.
- GEODIA Harmonization QA Wrapper v0.1 ya cierra el flujo en un comando local:
  harmonize offline, JSON validation, scans focales, pending review y reporte
  final QA.
- Tercer fixture oficial: INEGI ENOE queda `APPROVE_LOCAL_WITH_OFFICIAL_SOURCE`; fixture real creado desde fuente oficial sin credenciales; publicacion sigue `BLOCK`.

## Proyectos Y Paquetes Open/Public-Safe

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `packages/open-dev/duat-genesis` | `OPEN_PUBLIC_REPO_LIVE`; sandbox sintetico MIT; tests y scans previos limpios. Ahora incluye source cards public-safe para catalogos/fuentes. | Crear fixtures offline con hash para datasets elegidos, empezando por fuentes oficiales con licencia clara. | No usar datos reales sin source card, licencia, hash y claim boundary; calibracion sigue `DEMO_ONLY`. |
| `packages/open-dev/obsai-core` | `OPEN_PUBLIC_REPO_LIVE`; nucleo operacional public-safe. | Mantener APIs minimas y cerrar solo consumidores reales. | No absorber canon privado ni claims fuertes. |
| `packages/open-dev/residueos` | `OPEN_PUBLIC_REPO_LIVE`; action gate local con umbrales demo. | Calibrar con datasets reales o fixtures auditados antes de elevar claims. | Thresholds/calibracion `DEMO_ONLY`. |
| `packages/open-dev/observacionismo-gate` | `OPEN_PUBLIC_REPO_LIVE`; SDK aislado. | Mantener dependencia cero y contratos estables. | No mezclar runtime Claudio privado. |
| `packages/open-dev/claudio-os-blueprint` | `OPEN_PUBLIC_REPO_LIVE`; blueprint/handoff, no ISO final. | Verificar ISO/QEMU antes de cualquier claim de OS ejecutable. | ISO terminado no verificado. |
| `packages/open-dev/gemma-observacionismo-cleanup` | `OPEN_PUBLIC_REPO_LIVE`; fixtures sinteticos. | Mantenerlo como metodo de limpieza/observacion. | No pesos/modelos ni claims cientificos. |
| `packages/open-dev/obs-safe-integration-kit` | `OPEN_PUBLIC_REPO_LIVE`; wrappers dry-run, ActionGate y EvidenceStore. | Integrar solo adaptadores read-only o dry-run por defecto. | Riesgo si terceros lo conectan como autonomia garantizada. |

## DUAT, GEODIA Y Simulaciones

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `research/geodia-social-observatory` | `INTERNAL_RESEARCH`; MVP offline con allowlist, backtest local, tres fixtures oficiales (World Bank, Eurostat, INEGI), armonizacion v0.1, CLI reproducible y wrapper QA offline. | Preparar documentacion de release interna con licencia INEGI todavia en REVIEW. | Publicacion externa `BLOCK`; datos reales requieren licencia, hash y claim bajo; ordenamiento de paises bloqueado. |
| Awesomedata catalog | `PUBLIC_DATASET_CATALOG_INDEX`; registrado en ficha local y como policy/card. | Crear una source card por dataset elegido, no por catalogo. | Catalogo MIT no limpia licencias de datasets enlazados. |
| Fuentes oficiales seed | World Bank, Eurostat e INEGI ya tienen fixtures offline; IMF, OECD, OWID, GDELT y FRED siguen como candidatas documentadas. | Preparar release interno y revisar licencias antes de publicar. | FRED requiere API key; GDELT solo media signal; OWID requiere licencia original; INEGI requiere revision de terminos antes de redistribucion. |
| `publish_staging/medioevo-duat-public-release` | Public site/store/assets desplegados y verificados en `medioevo.space`; repo/staging sucio. | Separar mantenimiento web de cambios experimentales; no broad-stage. | Nuevo deploy/Gumroad/social requiere gate fresco. |

## Apps Comerciales

| app | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `apps/commercial/asistente-negocio` | `COMMERCIAL`; installer/current-user QA historico, scans focales limpios. | Clean VM QA, decision de firma/unsigned y legal final. | No venta/release final sin checklist comercial. |
| `apps/commercial/flujocrm` | `COMMERCIAL`; smoke, audit, installer QA, SQLite E2E y copy piloto verificados. | Rebuild/hash final del instalador activo y clean VM QA. | Legal final, firma/unsigned y publicacion externa gateada. |
| `apps/commercial/mini-office` | `COMMERCIAL`; tests locales y ZIP fuente verificados. | Clean-machine install, soporte/privacy/refund y checkout. | Legal final y paquete final. |
| `apps/commercial/argus-desktop` | `COMMERCIAL_OR_INTERNAL`; build/typecheck historico OK en temp. | Revalidar dependencias locales y UX antes de empaquetar. | Paquete final no generado; posible telemetria interna/assets privados. |
| `docs/product/wave-collapse.md` | `LOCAL_DEMO_READY`; evidence pack local y capturas. | QA visual DOCX y paquete instalable/listing. | Legal/EULA e instalacion/listing public-safe pendientes. |

## Productos Publicados / Tienda

| producto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `packages/paid/duat-templates` | `COMMERCIAL_PUBLISHED`; Gumroad vivo y metadata actualizada sin upload de archivos. | Subir media/cover en dashboard solo con gate autenticado separado. | No incluir DUAT Geodia privado ni datasets reales. |
| `packages/paid/medioevo-agent-ops-pack` | `COMMERCIAL_PUBLISHED`; Gumroad vivo y metadata actualizada sin upload de archivos. | Preparar assets sociales/manuales sin automatizar posts. | Dashboard/media/social siguen gateados. |
| `DESPERTAR Preview` | `COMMERCIAL_BOOKS_PUBLIC_SAFE_PREVIEW`; `medioevo.space/despertar-preview` y Gumroad `dmqgzi` verificados. | Resolver product id/dashboard de Gumroad si se requiere update de metadata/media. | No publicar libro completo ni claims bestseller. |
| `medioevo.space/store` | Live con tres productos y assets publicos. | Mantener QA de rutas y sitemap tras cambios. | Deploy futuro requiere ActionGate; DNS destructivo no autorizado. |

## Claudio, Wabi-Sabi Y Herramientas Locales

| herramienta | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| Claudio runtime `-=MEDIOEVO=-/-=LIBROS/claudio` | Rama ahead y worktree sucio; pending local `0`. | Solo cambios focales con pruebas; no normalizar todo el arbol. | Secrets locales, vendors, TCG/game bridge y cambios concurrentes. |
| Wabi-Sabi local agents | Suite historica `107 passed`; auto/router/background jobs documentados. | Mantener Ollama/cloud opt-in y provider status read-only. | Cloud/providers bloqueados por defecto; no imprimir secretos. |
| Curador SETO / release tools | Loop de curador hidden fix aplicado; pending review vigente `0`. | Usar curador preflight antes de nuevas fuentes/ZIPs. | Limpieza destructiva requiere gate exacto y migration map. |
| `tools/release` | Scripts de scan, manifests, tests, product assets y cleanup focal activos. | Usar scans por producto y manifests, no globs amplios. | Scan global legacy sigue no apto para release directo. |
| BRAIN_OS / Desktop live continuity | Root humano limpio y launchpad verificado; bulletin local instalado. | Mantener root limpio; enviar nuevos handoffs/reportes a su lane. | Borrado de duplicados exactos bloqueado sin gate destructivo. |

## Research Interno

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `research/obs-info-kernel` | Interno; tests historicos `22 passed`; scans focales limpios. | Validar fuentes primarias y claims antes de extraer open-dev. | No publicar claims de fisica/conciencia/topologia como verdad. |
| `research/observacionismo-lab` | Interno; tests historicos `34 passed`; scans focales limpios. | Usar como laboratorio de falsadores/fixtures, no como producto. | No prueba ciencia ni autoriza publicacion. |
| `MEDIOEVO_OBSERVACIONISMO_MASTER` | Canon/control operativo en evolucion. | Consolidar por fuente unica y handoff verificable. | Evitar duplicar verdad en carpetas paralelas. |

## Privado / No Publicar

| area | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `metaevo-tcg`, `claudio/tcg`, `runtime/game_bridge` | `PRIVATE`; fuera de releases publicos. | Mantener frontera y no mezclar con open/commercial. | No tocar ni publicar salvo instruccion privada explicita. |
| MEDIOEVO GM Lite | Repo GitHub privado vivo; build/secret scan/boundary check verificados. | Mantener privado; definir si habra deploy privado separado. | Public repo/public deploy bloqueados. |
| Libros/canon completo | `BOOKS_EDITORIAL`; preview publico selectivo existe. | Continuar con samples/preview aprobados. | No regalar libros completos ni vaults canonicos. |

## Proxima Accion Recomendada

World Bank Mexico, Eurostat Germany e INEGI ENOE ya tienen fixtures oficiales
offline; la armonizacion CLI y el wrapper QA pasan con tres fuentes. El
siguiente paso verificable para DUAT/GEODIA es preparar documentacion de
release interna sin publicacion externa, manteniendo licencia/terminos en
REVIEW y `publication_gate=BLOCK`.

## Evidencia Usada

- `docs/pending/PENDING_REVIEW_2026-05-14.md`
- `docs/release/RELEASE_READINESS_SCORE.md`
- `PRODUCT_MAP.md`
- `VISIBILITY_MATRIX.md`
- `RISK_REGISTER.md`
- `TEST_REPORT.md`
- `NEXT_SESSION_BRIEF.md`
- `docs/intake/AWESOMEDATA_PUBLIC_DATASETS_SOURCE_FICHA_2026-05-14.md`
- `docs/intake/EUROSTAT_SOCIAL_EPOCH_SOURCE_CARD_2026-05-14.md`
- `qa_artifacts/release_validation/geodia-eurostat-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-multisource-comparison-2026-05-14.json`
- `research/geodia-social-observatory/docs/GEODIA_INDICATOR_HARMONIZATION_v0_1.md`
- `qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-harmonization-cli-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-harmonization-qa-wrapper-report-2026-05-14.json`
- `qa_artifacts/release_validation/geodia-third-fixture-readiness-report-2026-05-14.json`

## DUAT Predictive Registry v0.1

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `research/duat-predictive-registry` | `LOCAL_RESEARCH`; Dual-Lane Filter + R vector + Filter Bank + SourceQuality + ForecastGate + 29 fuentes + 17 metodos + tests PASS. | Elegir objetivo predictivo concreto y medir R_before/R_after. | Publicacion externa BLOCK; claims de oraculo/ranking/causalidad/prediccion electoral BLOCK; fuentes con key en REVIEW. |

## DUAT Predictive Benchmark v0.2

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `research/duat-predictive-registry` | `LOCAL_RESEARCH_BENCHMARK`; primer benchmark R_before/R_after con fixtures GEODIA reales, DUAT tests 30 passed y GEODIA 53 passed. | Decidir mejora del benchmark o repetir sobre indicador con STRONG_PROXY. | ForecastGate REVIEW; publication_gate BLOCK; LicenseTermsScan REVIEW; no claims publicos. |

## DUAT Benchmark Matrix v0.3

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `research/duat-predictive-registry` | `LOCAL_RESEARCH_MATRIX`; benchmark matrix v0.3 con economy + labor real_fixture, replication `REPLICATED_LOCAL` para R_delta, DUAT tests 41 passed, GEODIA 53 passed. | Elegir tercer indicador o calibracion por dominio, porque labor MAE enhanced empeora. | ActionGate REVIEW; publication_gate BLOCK; LicenseTermsScan REVIEW; no claims publicos. |

## DUAT Domain Calibration Gate v0.4

| proyecto | estado actual | siguiente paso | bloqueo |
|---|---|---|---|
| `research/duat-predictive-registry` | `LOCAL_RESEARCH_DOMAIN_CALIBRATION`; matrix v0.4 con economy + labor + demography real_fixture; R_delta mejora en 3/3, pero metricas quedan economy=MIXED, labor=WORSE, demography=WORSE. DUAT tests 56 passed; GEODIA tests 53 passed. | Calibrar pesos/ventanas por dominio para que mejora operacional de R no se confunda con accuracy. | ActionGate REVIEW; publication_gate BLOCK; LicenseTermsScan REVIEW; ComparabilityReview REVIEW; no claims publicos. |

## 2026-05-14 - DUAT Metric-Aligned R Calibration v0.5

- Status: v0.5 implemented local-only.
- Tests: DUAT 70 passed; GEODIA 53 passed.
- Gate: ActionGate local REVIEW; publication_gate BLOCK.
- Next: nested domain calibration or freeze v0.5 as internal lab artifact.

## 2026-05-14 - DUAT Nested Domain Backtest v0.6

- Status: v0.6 implemented local-only.
- Tests: DUAT 87 passed; GEODIA 53 passed.
- Nested backtest: OOS_METRICS_WORSE in 3/3 indicators; ActionGate local REVIEW; publication_gate BLOCK.
- Next: freeze as boundary evidence or add longer official fixture before another predictive benchmark.

## 2026-05-15 - DUAT Official Long-History Data Readiness v0.7

- Status: v0.6 frozen as boundary evidence; v0.7 readiness layer implemented local-only.
- Tests: DUAT 96 passed; GEODIA 53 passed.
- DataGate: BLOCK because current offline source series have 6 observations, below MIN_OBSERVATIONS_WARN=24.
- Scans: SecretScan PASS; BoundaryCheck PASS; LicenseTermsScan REVIEW; PrivatePathScan PASS; ClaimsScan PASS; PublicationGateScan PASS; LeakagePreflight PASS; SchemaValidation PASS; ComparabilityReview REVIEW; ReconstructionTest PASS.
- Report: `research/duat-predictive-registry/reports/duat-official-long-history-data-readiness-v0-7.json`.
- SHA256 report: `ce0be663e545c47b6cbfcaf6e8a3311e33e383e4a71d3e72d08f834351e51a0e`.
- Next: collect official long-history data with source card, license terms review and comparability review before another backtest.

## 2026-05-15 - DUAT World Bank WDI Source Pack v0.8

- Status: first official long-history source pack created for DUAT using World Bank WDI.
- Scope: MEX.
- Series: economy n=64, labor n=35, demography n=65.
- DataGate: REVIEW; publication_gate BLOCK; no backtest executed.
- Tests: DUAT 103 passed; GEODIA 53 passed.
- Scans: SecretScan PASS; BoundaryCheck PASS; LicenseTermsScan REVIEW; PrivatePathScan PASS; ClaimsScan PASS; PublicationGateScan PASS; LeakagePreflight PASS; SchemaValidation PASS; ComparabilityReview REVIEW; ReconstructionTest PASS.
- Report: `research/duat-predictive-registry/reports/duat-world-bank-wdi-source-pack-v0-8.json`.
- SHA256 report: `4f4aea9d294baf221c50571a916c013bfd8449a16ff08c934a86ef8e1e23ba47`.
- Next: human/legal license review and comparability review before `DUAT_WDI_BACKTEST_v0_9`.

## 2026-05-15 - DUAT WDI License/Comparability Governance v0.8.1

- Status: governance review created for WDI source pack.
- DataGate: REVIEW.
- BacktestOpenGate: REVIEW_ONLY_DRY_RUN.
- LicenseTermsScan: REVIEW; ComparabilityReview: REVIEW; LeakagePreflight: PASS.
- Tests: DUAT 110 passed; GEODIA 53 passed.
- Report: `research/duat-predictive-registry/reports/duat-world-bank-wdi-governance-review-v0-8-1.json`.
- SHA256 report: `17b4548d2803984a27ef482c7fa2c828156dc9d7fc15831e962211d528365464`.
- Next: v0.9 can only be internal dry-run unless gates move to PASS.
