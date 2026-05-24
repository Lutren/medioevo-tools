# Pixel Billboard Population v1.3.2

DUAT now maps city simulation entities into 2D pixel billboards inside the Iso3D shell.

Population sources:
- agents: `src/iso3d/pixelAgentBillboards.ts`
- buildings: `src/iso3d/pixelBuildingBillboards.ts`
- props: `src/iso3d/pixelPropBillboards.ts`
- materials: `src/iso3d/pixelMaterialBillboards.ts`
- Q glyphs: `src/iso3d/isoSpriteLayer.ts`

Rules:
- billboards face the camera;
- light affects billboard brightness/tint;
- missing assets use procedural fallback keys;
- Agent Sims zoom-in and Hormiguero zoom-out use different camera presets;
- Debug mode can show Q overlays without disabling Canvas fallback.
