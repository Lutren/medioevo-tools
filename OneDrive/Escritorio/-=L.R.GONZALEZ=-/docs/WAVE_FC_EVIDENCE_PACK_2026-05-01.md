# Wave FC - Evidence Pack Local

Fecha: 2026-05-01

Decision: `LOCAL_DEMO_READY / PUBLICACION_BLOCK`. Se genero evidence pack local con datos sinteticos Markdown, DOCX y CSV; no usa APIs externas, no publica, no edita originales y conserva revision humana.

## Cambios

- `tools\wave_fc_client_demo_package.py` ahora genera `operations_brief.docx` sintetico ademas de Markdown/CSV.
- El demo registra 3 documentos autorizados: `.md`, `.md`, `.docx`.
- El DOCX se analiza por el lector seguro de Wave FC y queda con `docx_analysis`.
- `tests\test_wave_fc_client_demo_package.py` valida que el DOCX exista y tenga `obs_state_hash`.

## Evidence Pack Generado

Ruta:

`-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01`

Resultados:

- schema: `wave_fc.client_demo_package.v1`
- documentos: 3 (`.md`, `.md`, `.docx`)
- originals_unchanged: `true`
- drafts_total: 4
- artifacts_total: 4
- case_review_pack.ok: `true`
- workforce coverage_score: `1.0`
- docx_obs_state_hash: `f927d8f37ee1d086bddf0f9c2c0e72c89ad569df0e1d09f98e6a19fdc933ba7d`
- demo manifest SHA256: `5bf6ff36d424934ea7e4bd0fc7276b007e75caca1b4cf1283e61e0b3acb24733`
- input DOCX SHA256: `d5f6877377024763891e5efb45c319c656da9ebb0c5326a4518c421095a56e22`
- secret scan del pack: `count_reported=0`

## Release Gate Local

Ruta:

`-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01`

Resultados:

- schema: `wave_wabi.release_gate.v1`
- local_demo_ready: `true`
- public_publication_ready: `false`
- demo checks: `23 passed / 0 failed`
- benchmark checks: `17 passed / 0 failed`
- release gate report SHA256: `22167b4be3f4a2b165d95106d82248d4889152bb2059992567f1e024103ea557`
- gate demo manifest SHA256: `cc3d0a04d1a420a00542e04fbb0b6de84f0f3867c93f57c850eb2f2074ef6623`
- gate input DOCX SHA256: `336102c90dbeb221f1b0ba49ab61845c860a9734e076fbd66d25eca6e1fd6295`
- secret scan del gate: `count_reported=0`

## Validaciones

| Comando | Resultado |
|---|---|
| `python -m py_compile tools\wave_fc_client_demo_package.py` | OK |
| `python -m pytest tests\test_wave_fc_client_demo_package.py tests\test_wave_wabi_release_gate.py tests\test_wave_collapse_report.py tests\test_wave_fc_local_server.py -q` | `61 passed` |
| `python tools\wave_fc_client_demo_package.py --name wave_fc_evidence_pack_2026-05-01` | pack local generado |
| `python tools\wave_wabi_release_gate.py --name wave_wabi_gate_2026-05-01` | `local_demo_ready=true`, `public_publication_ready=false` |
| `python tools\release\scan_secrets.py --path='-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01' --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --path='-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01' --json --fail-on-findings` | `count_reported=0` |

## Capturas Locales

Ruta:

`qa_artifacts\2026-05-01-wave-fc-captures`

Capturas generadas con Playwright Python usando Chrome local, desde
`website\wave-collapse.html` via `file://`, sin servidor y sin acciones externas.

| Archivo | Tamano | SHA256 | Verificacion |
|---|---:|---|---|
| `desktop-1365x768.png` | 616847 | `718f82de95cf089ecbef2ce95b7c016660c15b32c54985ba4f45cfa90cb6e056` | no vacia; 1365x3242; extrema RGB no uniforme |
| `mobile-390x844.png` | 309802 | `1ebc0fe854dbbda1e72fbb24a232e5274c19d49ea19d0367f5ff771cf24806c4` | no vacia; 390x4049; extrema RGB no uniforme |

## Bloqueo Pendiente

No se completo render visual DOCX: `render_docx.py --renderer artifact-tool` fallo porque no encontro `@oai/artifact-tool`, y `--renderer libreoffice` fallo porque no hay `soffice/libreoffice`. Por eso el DOCX queda validado por parser/zip seguro y tests, pero no por QA visual.

Bloqueos de publicacion:

- licencia para artefactos publicos;
- docs de instalacion para usuario objetivo;
- landing copy public-safe;
- video opcional si se requiere para landing o Devpost;
- aprobacion de ActionGate para publicacion.

## Public-Safe Closure

Decision adicional 2026-05-01:

- `docs\product\wave-fc-public-safe-release-closure-2026-05-01.md`

El video no se requiere para el siguiente paso porque ya existen capturas
desktop/mobile con hashes. Wave FC queda apto para demo privada con datos
sinteticos y bloqueado para publicacion amplia hasta resolver QA visual DOCX,
legal/EULA y ActionGate.
