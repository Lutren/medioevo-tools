# ARGUS_ARCHIVE_GENERATED_ARTIFACTS_FICHA_2026-05-03

## Scope

Generated archive material under:

- `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\node_modules_status_cleanup_112717`
- `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\dist_status_cleanup_112717`

## Curador Preflight

Command:

```powershell
python tools\release\curador_preflight.py --path '_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\node_modules_status_cleanup_112717'
python tools\release\curador_preflight.py --path '_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\dist_status_cleanup_112717'
```

Results:

- `node_modules_status_cleanup_112717`: `DENIED_OR_SECRET_LIKE_DO_NOT_COPY`,
  `registered=True`, tech signals `python_package`, `node_package`, `docs`,
  `license`, `local_state`.
- `dist_status_cleanup_112717`: `DENIED_OR_SECRET_LIKE_DO_NOT_COPY`,
  `registered=False`, tech signals `none`.

## Inventory

| path | files | bytes | approx MB | top payload |
|---|---:|---:|---:|---|
| `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\node_modules_status_cleanup_112717` | 19,643 | 774,765,902 | 738.87 | `electron\dist\electron.exe` 213,915,136 bytes |
| `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\dist_status_cleanup_112717` | 16 | 3,785,323 | 3.61 | `medioevo-geodia-plaza.png` 2,725,085 bytes |

Other large generated binaries in the `node_modules` archive include
`dxcompiler.dll`, `app-builder.exe` variants for Windows/macOS/Linux and other
Electron-builder payloads.

## Boundary

- Classification: `ARCHIVE_GENERATED_ARTIFACT_REVIEW`.
- Do not copy into public, commercial or open-dev packages.
- Do not treat as active Argus source.
- Do not delete while host gate is `REVIEW`.
- The only useful value identified in this pass is cleanup/release evidence:
  it proves a prior generated artifact existed and was archived.

## Decision

Deleted after focused dry-run and ActionGate.

Evidence:

- Dry-run:
  `qa_artifacts\release_validation\argus-archive-generated-artifacts-second-pass-cleanup-dry-run-2026-05-03.json`.
- ActionGate:
  `322b8392-70a1-4f4b-a1f2-cc3b7171563c`.
- Result:
  `qa_artifacts\release_validation\argus-archive-generated-artifacts-second-pass-cleanup-result-2026-05-03.json`.

Deleted:

- `19,659` generated files.
- `778,551,225` bytes.
- Both target folders absent after deletion.
- Parent archive folder remains present but empty.
