# ASSET_BOUNDARY_REPORT v0.6

## Boundary

All scanned owner folders are treated as `UNKNOWN_REVIEW_REQUIRED` unless already marked public-safe. v0.6 did not copy candidate images, zips, audio, 3D models or private docs into the app.

## Public Manifest Policy

The public manifests under `public/asset-manifest/` use root tokens:

- `ROOT_BRAIN_OS`
- `ROOT_WORKSPACE`
- `ROOT_PUBLIC_SAFE_20260515`
- other explicit root tokens

They do not expose absolute `C:\Users\...` paths. This is enforced by `src/tests/assetInventory.test.ts`.

## Copy Status

All discovered visual candidates are currently `copy_status: not_copied`.

## Blocked / Review Areas

- Private game/TCG paths remain excluded.
- Secret-like paths remain blocked.
- Archives are registered but not extracted.
- Editorial or commercial assets require owner review before use.

## Safe Extraction Used

Only design principles were extracted into code: color/material direction, atlas fallback behavior, and the need for 2.5D city rendering.
