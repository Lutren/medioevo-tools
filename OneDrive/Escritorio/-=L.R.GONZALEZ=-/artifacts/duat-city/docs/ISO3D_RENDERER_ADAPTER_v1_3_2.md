# Iso3D Renderer Adapter v1.3.2

The v1.3.2 adapter is a local typed 2.5D/isometric shell. It does not execute Lovable zip code and does not require Three.js or R3F.

Capabilities:
- isometric grid/world conversion;
- deterministic depth sorting;
- mode-aware camera presets;
- feature-flagged renderer mode;
- Canvas fallback preservation;
- light sources and render metrics;
- static layer cache and dirty-region helpers.

UI:
- `src/components/IsoRendererPanel.tsx`
- `src/components/RendererModeToggle.tsx`
- `src/components/VermeerLightingPanel.tsx`

Fallback:
- default UI state keeps Canvas authoritative;
- Iso3D can be previewed from the renderer panel;
- missing visual assets resolve to procedural sprite keys.
