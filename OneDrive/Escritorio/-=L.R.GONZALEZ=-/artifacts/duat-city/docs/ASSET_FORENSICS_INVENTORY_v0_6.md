# ASSET_FORENSICS_INVENTORY v0.6

Fingerprint: `DUAT-ASSET-FORENSICS-PIXEL-PHYSICS-v0.6`

Run dir: `qa_artifacts/release_validation/RUN_DUAT_ASSET_FORENSICS_PIXEL_PHYSICS_v0_6_20260519`

## Scope

Read-only metadata scan over the owner-provided local roots. No source folder was modified, no archive was extracted, and no asset was copied into the app from those roots.

## Roots Scanned

| root token | scanned files | candidates | visual seen | visual recorded | code/doc/archive seen | archives registered |
|---|---:|---:|---:|---:|---:|---:|
| `ROOT_MEDIOEVO` | 7 | 0 | 0 | 0 | 0 | 0 |
| `ROOT_BRAIN_OS` | 34,981 | 14,817 | 3,011 | 700 | 13,278 | 855 |
| `ROOT_WORKSPACE` | 42,644 | 8,577 | 3,663 | 700 | 5,142 | 203 |
| `ROOT_LAUNCHPAD` | 18 | 0 | 0 | 0 | 0 | 0 |
| `ROOT_PORTFOLIO_OSIT_20260515` | 12 | 3 | 0 | 0 | 3 | 1 |
| `ROOT_PORTFOLIO_20260516` | 50 | 14 | 0 | 0 | 14 | 2 |
| `ROOT_PUBLIC_SAFE_20260515` | 13 | 3 | 0 | 0 | 3 | 1 |

## Useful Signals

- `ROOT_BRAIN_OS/DUAT ASSETS` contains a coherent DUAT visual kit, style guide, icons, UI panels and generated posters. Status: `REVIEW`, not copied.
- `ROOT_WORKSPACE/publish_staging/medioevo-site/medioevo-assets/img/buildings` contains isometric/building imagery. Status: `REVIEW`, not copied.
- `ROOT_WORKSPACE/docs/design/MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02.md` gives the strongest public-safe visual direction: obsidian, bronze/copper, cyan operational state, amber review state, dense agent-city UI.
- Archive candidates were registered only as paths and sizes. No zip was extracted in v0.6.

## Manifests

- `public/asset-manifest/visual_assets_manifest_v0_6.json`
- `public/asset-manifest/code_candidates_manifest_v0_6.json`
- `public/asset-manifest/duat_variants_manifest_v0_6.json`

Public manifests use sanitized root tokens, not absolute Windows private paths.
