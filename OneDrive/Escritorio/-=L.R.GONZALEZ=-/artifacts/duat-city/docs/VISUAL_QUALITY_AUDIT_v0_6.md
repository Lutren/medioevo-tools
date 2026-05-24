# VISUAL_QUALITY_AUDIT v0.6

## Baseline Issue

The v0.5 app worked, but the main city view read as a flat grid with simple circles. That was acceptable for telemetry, not for a 90s city/life-sim inspired MEDIOEVO RPG base.

## v0.6 Changes

- Tiles now render as 2.5D diamond-like surfaces.
- Buildings render as small raised masses with roof, shadow, gate outline and label.
- Agents render with blob shadows, need markers, gate ring, selection and labels.
- Day/night ambient light and building point lights are deterministic.
- OSIT mode can overlay field state from the pixel/cell physics summary.

## Remaining Quality Gaps

- No reviewed bitmap sprite pack was copied yet.
- No browser screenshot/performance benchmark was captured in this run.
- Click picking still uses the existing orthographic tile coordinate system; visual projection is 2.5D styled rather than a full isometric camera conversion.

## Direction

Keep Canvas 2D CPU-friendly. Adopt reviewed assets one-by-one only after provenance/license review, using the atlas manifest rather than raw imports.
