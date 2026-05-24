# Isometric Tech Reuse Map v1.3.2

DUAT v1.3.2 uses the local zip scan as an architecture reference, not as executable source.

Reuse decision:
- Three.js / R3F signals: adapt concepts only; no dependency added.
- Isometric grid signals: implemented as local `src/iso3d/isoGrid.ts`.
- Camera/zoom signals: implemented as local `src/iso3d/isoCamera.ts`.
- Sprite/billboard signals: implemented as local `src/iso3d/isoBillboard.ts` and pixel population modules.
- UI/panel signals: mapped into DUAT panels without raw component import.

Adapter files:
- `src/iso3d/isoSceneAdapter.ts`
- `src/iso3d/isoWorld.ts`
- `src/iso3d/isoLighting.ts`
- `src/iso3d/isoRenderMetrics.ts`
- `src/iso3d/isoLayerCache.ts`
- `src/iso3d/isoDirtyRegions.ts`
- `src/iso3d/isoPerformanceBudget.ts`

The existing Canvas renderer remains authoritative and available as fallback.
