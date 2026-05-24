# MIGRATION_PLAN v0.6

## Applied

1. Preserve v0.5 simulation and tests.
2. Add asset manifests and internal inventory docs.
3. Add procedural render modules instead of copying unreviewed assets.
4. Add pixel/cell physics field as a low-resolution active-cell subsystem.
5. Add object interaction and routine helpers for Sims-style behavior.
6. Upgrade RPG export to `medioevo-rpg/world/v2`.
7. Add Wabi v0.6 workpack draft generators with execution disabled.

## Reversible Boundaries

- New code is path-scoped under `artifacts/duat-city/src`.
- Original scanned folders were not modified.
- Asset manifests can be regenerated from the run dir.
- No external deployment or MCP execution was enabled.

## Next Safe Migration

Review `visual_assets_manifest_v0_6.json` and approve a small allowlist of 5-10 assets. Only then copy to a dedicated `public/duat-assets-reviewed/` folder with source hash, license note and updated manifest.
