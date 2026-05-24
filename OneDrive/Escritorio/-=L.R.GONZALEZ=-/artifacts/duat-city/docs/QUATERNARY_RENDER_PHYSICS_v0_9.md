# QUATERNARY RENDER AND PHYSICS v0.9

## Render / LOD

Quaternary timing modulates render budget:

- unstable or blocked quaternary gate compresses rendering;
- stable `10` channels support cached/low-detail rendering;
- active `11` channels can expand only when timing is stable enough.

The DEBUG view can display Q overlays:

- `00`: no visible overlay;
- `01`: amber/red review outline;
- `10`: low-opacity green/cyan stable outline;
- `11`: bright cyan event pulse.

Beautiful mode remains clean and does not display Q overlays.

## Pixel Field

The pixel physics field stores optional compact Q state in `qPacked`:

- lower 2 bits: Q state index `0..3`;
- upper bits: dwell ticks clamped to `0..63`.

This is per simulated pixel-cell/material cell, not per screen pixel. It keeps the engine local, 2D/isometric and performant while still allowing material behavior such as falling water, rising smoke, fire/light and dust/residue.

## Asset Direction

The v0.9 visual target is retrofuturistic pixel art: archeopunk, steampunk, cyberpunk, ecopunk and solarpunk. No assets were copied in this implementation.

