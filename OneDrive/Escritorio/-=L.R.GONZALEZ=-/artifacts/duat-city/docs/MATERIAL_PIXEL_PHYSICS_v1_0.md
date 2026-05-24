# Material Pixel Physics v1.0

The material pixel/cell field extends `src/physicsField`.

## Pixel Cell Meaning

A physical pixel means a logical `PixelCell` in the world field. It is not every rendered screen pixel. The engine updates active logical cells and summarizes inactive cells.

Tracked fields include material, color, light, temperature, wetness, velocity, density, emissive, opacity, reflectance, roughness, active state, qState, R and Phi_eff.

## Materials

Implemented definitions include:

`empty`, `air`, `stone`, `brick`, `wood`, `metal`, `glass`, `water`, `soil`, `grass`, `fire`, `smoke`, `dust`, `neon`, `cloth`, `skin`, `obsidian`, `gold`, `crystal`, `ruinMatter`.

## Rules

- Fire emits light and heat.
- Water reflects light and moves down/laterally.
- Smoke rises and scatters light.
- Glass transmits some light.
- Metal reflects more.
- Wet stone reflects more than dry stone.
- Neon emits colored light.
- Ruin matter flickers as an anomaly.

Boundary: this is a lightweight logical material model for rendering and OSIT metrics, not exact material physics.
