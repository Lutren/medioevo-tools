# ASSET_AWARE_PIXEL_ENGINE_v1_2

## Result

DUAT now has an asset-aware 2D/2.5D game-engine layer with:

- metadata-only scan of Assets Du WABI;
- asset manifest and review allowlist;
- reviewed-asset atlas v2 with safe fallback;
- procedural pixel-art generators;
- VibeCoding game authoring commands;
- serializable game loop;
- material/light gameplay hooks;
- RPG world v3 export.

## Asset Boundary

No asset was copied in v1.2 because scanned files remain `license_status=unknown/review`. Runtime asset mode defaults to procedural fallback. `publication_allowed=false` remains enforced in v1.2 manifests.

## Physics Boundary

Pixel physics means logical low-res/sparse cells with minimal physical state. It is not full screen-pixel rigid-body simulation and not exact physics.
