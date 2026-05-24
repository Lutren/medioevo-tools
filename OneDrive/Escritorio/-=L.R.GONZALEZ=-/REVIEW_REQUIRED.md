## 2026-05-22 - Fragmentos Cover Asset Production

Estado: REVIEW_REQUIRED / no ejecutado en esta sesion.

Evidencia local preparada:

- Human publication gate packet:
  `docs\publishing\FRAGMENTOS_CALIBRACION_HUMAN_PUBLICATION_GATE_PACKET_2026-05-22.md`.
- Fragmentos cover brief:
  `docs\publishing\FRAGMENTOS_PUBLIC_SAFE_COVER_BRIEF_2026-05-22.md`.
- Cover asset gate:
  `qa_artifacts\editorial_cover_gate\FRAGMENTOS_COVER_GATE_20260522`.
- Validador:
  `tools\release\validate_cover_asset_gate.py`.
- Estado actual del gate: `REVIEW_ASSET_MISSING` con licencia/procedencia
  pendiente.
- Secret scans focales: `count_reported=0`.

Accion requerida:

- Revision humana de direccion visual antes de generar o seleccionar portada.
- Registrar procedencia/licencia del asset si se genera o selecciona imagen.
- Mantener bloqueado KDP/Gumroad/web/redes/push/deploy/public ZIP.

---

## 2026-05-22 - Editorial Human Publication Review

Estado: REVIEW_REQUIRED / no ejecutado en esta sesion.

Evidencia local ya cerrada:

- Word/PDF automated full-page QA paso para Fragmentos y Calibracion:
  `PASS_AUTOMATED_FULL_PAGE_COVERAGE`.
- Fragmentos: `688` paginas renderizadas, `blank=0`, `edge=0`.
- Calibracion: `477` paginas renderizadas, `blank=0`, `edge=0`.

Accion requerida:

- Antes de KDP/Gumroad/store/print/public ZIP, realizar revision humana
  editorial/comercial de portada, listing, precio, metadata, muestra publica y
  paginas finales.
- Mantener `PublicationGate=BLOCK` hasta gate explicito por destino.

---

## 2026-05-22 - Editorial DOCX Full Visual Approval

Estado: AUTOMATED_LOCAL_COVERAGE_CLOSED / human publication review remains
separate.

Evidencia:

- Fragmentos `artifact-tool` DOCX render no termino en ventana controlada; se
  conservaron `53` paginas PNG parciales.
- Calibracion `artifact-tool` DOCX render no termino en ventana controlada; se
  conservaron `19` paginas PNG parciales.
- QA split representativo creado en
  `qa_artifacts\editorial_docx_visual_qa\EDITORIAL_INTERNAL_EXPORTS_SPLIT_QA_20260522`.
- Resultado: `PARTIAL_QA_REVIEW_WITH_LIMITS`.
- Fallback Word/PDF completo ejecutado despues:
  `qa_artifacts\editorial_docx_word_visual_qa\EDITORIAL_DOCX_WORD_FULL_QA_20260522`
  con `PASS_AUTOMATED_FULL_PAGE_COVERAGE`.

Accion requerida:

- No se requiere otro render automatizado para blank/edge smoke. La revision
  humana queda solo si se pretende venta/publicacion/impresion.
- Mantener `PublicationGate=BLOCK`; los renders contienen material editorial
  privado.

---

## 2026-05-17 - Obsidian global vault registry

Estado: APPROVE_EXECUTED

- La configuracion local del vault canonico se creo en
  `-=MEDIOEVO=-\-=LIBROS\vault_medioevo\.obsidian`.
- Estado inicial observado del registro global Obsidian: apuntaba a
  `C:\Users\L-Tyr\OneDrive\Documentos\Obsidian Vault` y
  `C:\Users\L-Tyr\OneDrive\Escritorio\Medioevo`; no incluia el vault
  canonico `-=MEDIOEVO=-\-=LIBROS\vault_medioevo`.
- Con aprobacion explicita del operador (`apruebo todo`), se registro el vault
  canonico en `C:\Users\L-Tyr\AppData\Roaming\obsidian\obsidian.json`.
- Backup previo:
  `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\obsidian_appdata_backups\obsidian.json.backup-20260516-204011`.
- Verificacion posterior: `registered_id=c212f9cdec74c3a9`,
  `registered_path=C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\vault_medioevo`,
  `open=true`.
- `Get-Process *Obsidian*` no encontro proceso activo durante la modificacion.

---

## 2026-05-16/17 - MEDIOEVO DUAT + corpus teorico publico: push/deploy externo

Estado: BLOCK por host gate 2026-05-17

Evidencia local:

- `python tools\release\pending_review.py --write --quiet` reporto `active_dedup=18`, `claudio_open=0`.
- DUAT Lab corregido localmente y en staging deploy-ready; smoke visual local termino `ok=True`, `action_gate=REVIEW`.
- Corpus teorico publico generado desde fuentes limpias allowlisted en `publish_staging\medioevo-theory-public-release`.
- `python -m pytest tests\test_duat_lab_visual_smoke.py tests\test_public_theory_release.py -q` termino `10 passed`.
- Auditoria SEO del sitio activo y staging deploy-ready termino sin findings mayores.
- Escaneo enfocado de secretos para `publish_staging\medioevo-theory-public-release` y `publish_staging\medioevo-site-deploy-ready-2026-05-16` reporto `count_reported=0`.
- Host gate fresco devolvio `gate=REVIEW`, `status=CONTAMINADO`, `R=0.634`, `Phi_eff=0.388`, razones `cpu_alta`, `disco_precaucion`, `residuo_alto`.
- Reintento 2026-05-17 devolvio `gate=BLOCK`, `status=JAMMING`, `R=0.651`, `Phi_eff=0.378`, razones `memoria_alta`, `disco_precaucion`, `proceso_dominante_cpu`, `residuo_alto`.
- Autorizacion humana amplia registrada 2026-05-17: `autorizo todo , termina con todo`.
- ActionGate target-specific con `external_authorized=true` nego ambos targets porque exige host `APPROVE`:
  - `medioevo-site-deploy`: decision `b0ce1f74-77f6-47cb-8d01-50a96ad2a1d0`.
  - `github-medioevo-theory-public-release`: decision `c5ebd293-fa80-4e89-b19e-58f0fc3995ce`.
- Repo local `publish_staging\medioevo-theory-public-release` quedo commiteado en `main`, commit `6bdddb9`.

Accion requerida:

- No hacer `git push`, `gh repo create`, Cloudflare deploy ni publicacion externa desde este ciclo.
- Reintentar solo cuando el host gate vuelva a `APPROVE`; no ejecutar bajo `BLOCK`.
- Si se reabre, publicar solo los targets verificados: `publish_staging\medioevo-theory-public-release` y `publish_staging\medioevo-site-deploy-ready-2026-05-16`.

Paquete:

- `docs/publishing/MEDIOEVO_DUAT_THEORY_SEO_IMPLEMENTATION_2026-05-16.md`

---

## 2026-05-13 - Desktop setup external/provider gates

Estado: REVIEW

- `banananana.txt`: classify/hash only; do not read, rotate, move or delete without owner review.
- NVIDIA ultra: cost/quota/access review required before sustained use.
- DashScope/Qwen: env presence may be checked redacted; no cloud activation without key/account gate.
- External publication is not executed by this local desktop setup block.

---

## 2026-05-13 - BRAIN_OS exact duplicate deletion

Estado: REVIEW

- La limpieza visible de BRAIN_OS movio archivos fuera de la raiz humana, pero
  no borro paquetes ni documentos.
- Borrar duplicados exactos requiere frase explicita de limpieza final,
  SHA256/path canonico por grupo, evidencia de rollback o regenerabilidad, y
  confirmacion de que el archivo no es unico.
- Hasta entonces, los duplicados o versiones anteriores quedan en archivo o
  revision, no eliminados.

---

## 2026-05-13 - Owner Override Provider/Secret Closeout

Estado: SUPERSEDED_AS_LOCAL_BACKLOG

Los tres P0 provider/secret fueron cerrados por override del owner como
decision operativa local:

- `banananana.txt`: `CLOSED_KEEP_PRIVATE_REDACTED`.
- NVIDIA `ultra`: `CLOSED_DO_NOT_USE_ULTRA`.
- DashScope/Qwen: `CLOSED_QWEN_DISABLED_NO_BEARER`.

No se imprimieron valores, no se rotaron credenciales, no se hicieron llamadas
pagadas nuevas y no se publico nada. Cualquier uso futuro de cloud/provider es
scope nuevo con ActionGate propio.

Paquete: `docs/pending/OWNER_OVERRIDE_PROVIDER_SECRET_CLOSEOUT_2026-05-13.md`

---

# 2026-05-14 - Product assets/publicity external action gate

Estado: PARTIAL_RESOLVED / REVIEW_RESIDUAL

- Scope resolved: deploy updated product covers/store pages to Cloudflare Pages.
- Scope still in REVIEW: Gumroad dashboard media/cover upload, DESPERTAR
  `dmqgzi` product-id/dashboard correction, social content and paid advertising.
- Local status: products, covers, site source, publicity kit, tests, build and focused secret scans completed.
- Gate update: `website_deploy` target-specific ActionGate returned `allowed=true`, `status=pass`, decision `50940487-f93c-40ae-8725-c0fad3d4c2c3`.
- Deploy result: `npx wrangler pages deploy dist --project-name=medioevo-site --branch=main` completed; preview `https://eab034f5.medioevo-site.pages.dev`.
- Live verification: `https://medioevo.space/store?qa=product-assets-20260514-final` HTTP `200` with the three products and public assets.
- Gumroad update result: DUAT Templates and MEDIOEVO Agent Ops Pack metadata
  were updated by API with `with_file_requested=false`.
- DESPERTAR update result: `dmqgzi` API update did not apply; Gumroad returned
  `Custom permalink has already been taken`. Public URL remains HTTP `200`.
- Residual decision: no Gumroad media/cover upload, no social post, no paid ads
  and no DNS change from this run.
- Safe next action: run a separate authenticated ActionGate for Gumroad media
  upload or `dmqgzi` product-id repair if those are still desired.

# REVIEW_REQUIRED

## 2026-05-21 - Pending System Execution Residual Gates

Estado: REVIEW_REQUIRED / retirado de pendientes ejecutables locales.

Evidencia:

- El barrido canonico inicial de pendientes reporto `active_dedup=33` y
  `claudio_open=0`.
- Despues de cerrar los items locales y trasladar los gates no ejecutables,
  `python tools\release\pending_review.py --write --quiet` reporto
  `active_dedup=0` y `claudio_open=0`.
- Paquete de cierre:
  `docs\ops\PENDING_SYSTEM_EXECUTION_CLOSEOUT_2026-05-21.md`.

Acciones que permanecen en review:

- Host next-login check: requiere el proximo inicio real de Windows; no puede
  verificarse desde esta sesion.
- Host clearance: requiere `disk_pct < 85` y revision RPC `135` con
  PowerShell/admin/firewall antes de declarar host `APPROVE`.
- DUAT-city audio app: `npm run build` y `npm run lint` se intentaron; fallan
  por dependencias/test runner faltantes o incompatibles. No instalar
  dependencias por red sin review.
- Owner asset provenance/licencia/public-safe, staging publico y NVIDIA live
  smoke siguen fuera del cierre local sin owner review/doble opt-in.

Decision:

- No ejecutar publicacion, deploy, push, cloud live, instalacion por red,
  cleanup destructivo ni cambios de host/admin desde este cierre.

## 2026-05-21 - FlujoCRM GitHub Post-Publication Gates

Estado: REVIEW_REQUIRED / preflight local ejecutado.

Evidencia:

- `python tools\release\audit_flujocrm_free_license_readiness.py --write --json`
  devolvio `publication_ready=true`, `blockers=[]`.
- `python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json`
  devolvio `count_reported=0`.
- `npm run check` en `publish_staging\github\flujocrm-free-review` paso los
  smokes `main`, `preload` y `renderer`.
- Staging local esta en HEAD `a16c019`; no se observo remote configurado.
- Reporte:
  `docs\publishing\FLUJOCRM_GITHUB_LOCAL_PREFLIGHT_2026-05-21.md`.

Acciones que permanecen en review:

- Crear repo GitHub, hacer `git push`, editar metadata GitHub o confirmar URL
  final en website.
- Re-run secret scan despues de publicacion real.
- Verificar archivos live GitHub contra manifest final.
- Agregar screenshots solo despues de public-safe visual QA.
- Regenerar o confirmar manifest final si los cinco docs de control quedan
  incluidos en el repo publico.

## 2026-05-13 - Remaining P0 Provider And Secret Gates

Estado: REVIEW

Evidencia:

- `python tools\release\pending_review.py --write --quiet` reporta
  `active_dedup=3`, `claudio_open=0`.
- Los 3 pendientes restantes son P0:
  - rotacion/vigencia de credenciales en `banananana.txt`;
  - costo/cuota y access NVIDIA para `ultra`;
  - obtencion/registro de presencia redactada de `DASHSCOPE_API_KEY` o
    `QWEN_API_KEY`.
- `docs/ops/WABI_QWEN_REDACTED_PRESENCE_2026-05-13.md` confirma ausencia de
  bearer Qwen por nombre sin imprimir valores.

Accion requerida:

- No leer ni imprimir valores de secretos.
- No borrar, normalizar ni mover `banananana.txt` hasta owner review.
- No hacer llamadas pagadas/sostenidas a proveedores ni abrir billing desde
  este cierre local.
- Registrar solo presencia/ausencia, fecha, cuenta/proveedor y gate.

Paquete:

- `docs/pending/REMAINING_P0_GATED_WORKPACK_2026-05-13.md`

## 2026-05-07 - Secondary Terminal Popup Candidates

These were identified while fixing the recurrent `CuradorSETO-Downloads-Intake`
terminal popup. They were not changed in this cycle because the recurrent
scheduled task had the strongest evidence and was fixed first.

| target | evidence | review action |
|---|---|---|
| `Startup\OpenClaw Gateway.cmd` | contains `start "" /min cmd.exe /d /c C:\Users\L-Tyr\.openclaw\gateway.cmd` | only convert to hidden wrapper if a console appears at login/startup |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ClaudioHarnessAutopilot` | calls `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...run_claudio_harness_autopilot.ps1 -Full` | only convert to hidden wrapper after a separate host-startup gate |
| `apps/local/wabi-sabi/wabi-window.ps1` | intentionally uses `WindowStyle Normal` for manual operator console | do not hide unless replacing the manual Wabi window UX |

---

Fecha: 2026-05-06
Estado: gates globales restantes no ejecutables localmente

Paquete de evidencia:

- `qa_artifacts/release_validation/global-review-gates-2026-05-06.json`

## 1. Scan global no limpio

Estado: REVIEW

Evidencia:

- Comando: `python tools\release\scan_secrets.py --json --limit 500`
- Resultado actual: `count_reported=223`, `truncated_at=500`.
- Resumen por razon, sin imprimir valores:
  - `secret-like content markers`: 166
  - `secret-like filename`: 37
  - `denylist path`: 34
- Prefijos principales:
  - `-=MEDIOEVO=-/-=LIBROS/claudio`: 126
  - `-=MEDIOEVO=-/CLAUDIO - researchs/GEODIA`: 26
  - `runtime/curador_seto/source_archive`: 20
  - `tools/claw-code/rust`: 12
  - `-=MEDIOEVO=-/-=LIBROS/-=CEREBRO=-`: 7

Accion requerida:

- Triage humano/target-specific antes de cualquier release publico.
- No imprimir secretos.
- No borrar ni mover hallazgos desde este pase.

Paquete:

- `docs/security/GLOBAL_SENSITIVE_SCAN_TRIAGE_2026-05-06.md`

## 2. Licencia global

Estado: LEGAL_REVIEW_REQUIRED

Evidencia:

- `RELEASE_CHECKLIST.md` mantiene la licencia global sin decision.

Accion requerida:

- Revision legal/humana por capa o target.
- No aplicar licencia global al workspace completo.

Paquete:

- `docs/legal/GLOBAL_LICENSE_REVIEW_PACKET_2026-05-06.md`

## 3. Worktree global no limpio

Estado: REVIEW

Evidencia:

- `git status --short` muestra cambios activos de multiples carriles y otros agentes.
- El target `claudio_direct_local` esta acotado, pero el workspace global no esta limpio.

Accion requerida:

- No usar `git add .`.
- No revertir cambios de otros agentes.
- Separar staging/commit por target solo cuando el operador lo pida.

Paquete:

- `docs/developer/WORKTREE_REVIEW_PACKET_2026-05-06.md`

## 4. Publicacion CRM/prompts solicitada

Estado: REVIEW/BLOCK externo

Evidencia:

- Host gate fresco en Claudio: `JAMMING/BLOCK`, `R=0.796`, `Phi_eff=0.305`.
- Host directo posterior: `CONTAMINADO/REVIEW`, `R=0.652`, `Phi_eff=0.378`,
  pero el ActionGate target-specific recalculo host como `JAMMING/BLOCK`,
  `R=0.636`, `Phi_eff=0.387`.
- ActionGate bloqueo `linkedin-profile-post`, `gumroad-products-update`,
  `github-flujocrm-free-release` y `medioevo-site-deploy` aunque el operador
  autorizo la intencion.
- Recheck IDs: `00c38fc2-393c-465b-9b76-27fb48eace09`,
  `4e666ec1-0ce2-4052-bb48-604e90474ea1`,
  `0fe30efc-48e1-4785-a65a-77a81a935488`,
  `43295ef9-bc95-41db-bb44-46a607833ef3`.
- FlujoCRM staging publico ya esta marcado `license=MIT`, `private=false`.
  El producto activo `apps/commercial/flujocrm` no fue cambiado.
- Verificador local de licencia:
  `qa_artifacts/release_validation/flujocrm-free-license-readiness-2026-05-06.json`
  reporta `publication_ready=true`.
- Bloqueos del verificador: ninguno.
- ActionGate GitHub posterior: decision
  `45e925ce-7643-4390-8418-2ef9dc91303e`, `blocked` por host
  `JAMMING/BLOCK`. Decision previa:
  `efb26b49-6e6a-4dee-b8db-a9e5e6e685fb`, mismo resultado.

Accion requerida:

- No publicar LinkedIn/Gumroad/GitHub/deploy desde este gate.
- No publicar hasta que `github-flujocrm-free-release` pase ActionGate.
- Usar `docs/publishing/CRM_PROMPTS_PUBLICATION_PACKET_2026-05-06.md` cuando
  host y ActionGate vuelvan a permitir el target.
- Usar `docs/publishing/WEBSITE_CRM_PROMPTS_DROPIN_2026-05-06.md` para aplicar
  la pagina solo cuando el website worktree y deploy gate esten limpios.

## 5. MemPalace global Python dependency cleanup

Estado: TARGET_CONFLICT_RESOLVED / REVIEW residual

Evidencia:

- Claudio tiene MemPalace avanzado instalado en venv aislada:
  `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\mempalace\.venv` con
  `mempalace 3.3.4`, `chromadb 1.5.9` y `sentence-transformers 5.4.1`.
- Python global queda restaurado a carril CrewAI:
  `crewai 1.14.2`, `chromadb 1.1.1`, `mempalace 3.0.0`.
- El upgrade global fue ejecutado despues de backup:
  `C:\Users\L-Tyr\.mempalace\backups\pre_repair_20260506-193725`.
- Claudio ya no depende del vault global para su wrapper legacy: el default
  reparado usa
  `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\mempalace\palace`.
- `python tools\mempalace_healthcheck.py --write --smoke-write` reporta
  `ok=true`, wrapper `persistent=true`, `collections=1`, `embeddings>=1`,
  `matched=true`.
- `mempalace --palace C:\Users\L-Tyr\.mempalace\palace status` pasa con
  `58 drawers` usando el CLI aislado; `search` devuelve resultados del
  `memory_vault` curado.
- `repair-status` lee `drawers sqlite count=58` y `closets sqlite count=8`;
  HNSW metadata queda `UNKNOWN` porque Chroma aun no flushea esa metadata.
- `python -m pip check | Select-String -Pattern 'crewai|chromadb|mempalace'`
  no devuelve matches; el conflicto directo `crewai`/`chromadb` esta resuelto.
- `runtime\mempalace\.venv\Scripts\python.exe -m pip check` reporta
  `No broken requirements found`.
- `python -m pip check` completo sigue con conflictos historicos no
  relacionados; `docs\developer\PYTHON_GLOBAL_DEPENDENCY_TRIAGE_2026-05-07.md`
  los clasifica en 19 issues por lanes, todos en `REVIEW`.
- La primera busqueda aislada descargo automaticamente el modelo Chroma
  `all-MiniLM-L6-v2` en `C:\Users\L-Tyr\.cache\chroma\onnx_models`.
- `tools\mempalace_healthcheck.py` ahora verifica esa cache y reporta
  `offline_semantic_search_ready=true`, `download_may_be_needed=false` para
  este host.
- Wabi-Sabi registro el aprendizaje `LEARN_LAYERED_ABSORPTION` en
  `runtime\wabisabi_run_ledger\decisions.jsonl`.

Accion requerida:

- No hacer limpieza global amplia de Python desde el carril MemPalace.
- Si CrewAI o MemPalace fallan en uso real, mantener la separacion por capas:
  venv MemPalace avanzado y host Python conservador para orquestacion.
- Mantener `PYTHONIOENCODING=utf-8` para CLI MemPalace en Windows.
- En maquinas nuevas, ejecutar healthcheck antes de declarar busqueda
  semantica offline.

Paquete:

- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\MEMPALACE_INSTALL_VERIFY_2026-05-07.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\reports\WABISABI_MEMPALACE_OBSERVACION_LEARNING_2026-05-07.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\developer\PYTHON_GLOBAL_DEPENDENCY_TRIAGE_2026-05-07.md`

## 6. MEDIOEVO_LIVE_TREE dev dependency major upgrade

Estado: REVIEW

Fecha: 2026-05-13

Evidencia:

- En `C:\Users\L-Tyr\OneDrive\Documentos\New project 3`, `npm audit --omit=dev --json`
  reporta 0 vulnerabilidades prod.
- `npm audit --json` reporta 5 vulnerabilidades moderadas dev en la cadena
  Vite/Vitest/esbuild.
- La correccion sugerida requiere upgrades semver-major:
  `vite` 8.x y `vitest` 4.x.
- La suite actual pasa:
  `npm test -- src/messagebus` 90 tests,
  `npm test` 101 tests,
  `npx tsc -b --pretty false`,
  `npm run build`.

Accion requerida:

- No ejecutar `npm audit fix --force` dentro de cierre de pendientes.
- Abrir carril separado para upgrade mayor con snapshot previo, build visual y
  rollback.
- Mantener `npm audit --omit=dev` como gate prod hasta que el upgrade se haga.

Paquete:

- `MEDIOEVO_LIVE_TREE\10_QUALITY\PENDING_CLOSEOUT_RUN_9_TEST_REPORT.md`

## 7. BRAIN_OS exact duplicate deletion gate

Estado: REVIEW

Fecha: 2026-05-13

Evidencia:

- `-= BRAIN_OS =-`, `-=L.R.GONZALEZ=-` y `MEDIOEVO_LAUNCHPAD` fueron medidos.
- Exact duplicate groups >= 1 MB: `219`.
- Potential reclaim if one copy per SHA256 is kept: `8265.64 MB`.
- BRAIN_OS duplicate candidates: `642` files / `7088.42 MB`.
- L.R.GONZALEZ duplicate candidates: `237` files / `1177.05 MB`.
- En este pase solo se movieron 9 ZIPs/versiones anteriores fuera de la raiz visible de BRAIN_OS; no se borraron ZIP packages.

Accion requerida:

- No ejecutar `Remove-Item` sobre ZIPs, source vaults, archives o exact duplicate sets sin gate explicito.
- Antes de borrar: seleccionar una copia canonica por SHA256, registrar path/hash, confirmar rollback o regenerabilidad, y usar el cleanup gate.
- Mantener `DELETE_CANDIDATES.md` como cola de borrado; no convertirlo en accion automatica.

Paquete:

- `DUPLICATES_AND_DEAD_CODE.md`
- `DELETE_CANDIDATES.md`
- `MIGRATION_MAP.md`
- `-= BRAIN_OS =-\00_START_HERE\WORKSPACE_AUDIT\ZIP_REVIEW_RUN2.md`
## Disk Relief Review Required - 2026-05-14

- Revisar antes de borrar entornos completos:
  `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\env_matrix\model_audio_nlp\.venv`
  (`2056.39 MiB`), `runtime\mempalace\.venv` (`848.76 MiB`) y
  `.venv_api` (`351.60 MiB`). No se detecto `requirements.txt` ni
  `pyproject.toml` en la carpeta padre de esos entornos durante la medicion.
- Revisar si `publish_staging\medioevo-site\.git` (`620.09 MiB`) puede
  retirarse de la copia estatica vieja. No tocar si esa carpeta sigue siendo
  fuente de verdad historica.
- Limpieza global fuera de `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`
  queda en revision por alcance host/global.

## MEDIOEVO GM Lite private GitHub upload - 2026-05-14

Estado: RESOLVED_WITH_EXPLICIT_PRIVATE_REPO_OVERRIDE

Evidencia:

- ZIP solicitado: `C:\Users\L-Tyr\Downloads\medioevo-gm-lite-private-mvp.zip`.
- SHA256: `0421D51E6C1EB76E7F060A589169DC8E42E7B22336F63C5E38B79D74D0CEF57C`.
- Staging local creado: `publish_staging\github-private\medioevo-gm-lite-private-mvp`.
- Secret scan focalizado: `count_reported=0`.
- Boundary check: `PASS`.
- Host gate actual: `CONTAMINADO/REVIEW`, `R=0.537`, `Phi_eff=0.449`, `lambda_sat=0.892`.
- Repos revisados y no encontrados/accesibles: `Lutren/medioevo-gm-lite`, `Lutren/medioevo-gm-lite-private-mvp`.
- Override posterior del operador: `si y verifica todos los pendientes y continua`.
- ActionGate para comando externo autorizado: PASS, decision `e90290a9-b7d5-4d0a-8c39-2e6cf283cc83`.
- `npm install`: PASS, `0 vulnerabilities`.
- `npm run build`: PASS.
- `npm audit --audit-level=moderate`: PASS, `0 vulnerabilities`.
- Repo creado: `https://github.com/Lutren/medioevo-gm-lite`.
- Verificacion GitHub API: `private=true`, `visibility=private`, default branch `main`.
- Commit inicial: `ec755ca64ed3fb949ce5908036f0be01f3e51fd8`.

Accion requerida:

- Ninguna pendiente para este ZIP privado.
- No hacer deploy publico, Cloudflare/Netlify, cambio de visibilidad, release publico o redes desde este cierre.

Paquete:

- `docs\intake\MEDIOEVO_GM_LITE_PRIVATE_MVP_FICHA_2026-05-14.md`
- `qa_artifacts\release_validation\MEDIOEVO_GM_LITE_PRIVATE_GITHUB_REVIEW_2026-05-14.md`
