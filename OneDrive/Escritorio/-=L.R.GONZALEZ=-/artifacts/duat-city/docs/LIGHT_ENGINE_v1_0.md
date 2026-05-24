# Light Engine v1.0

The v1.0 light engine lives in `src/light`.

## Model

The engine uses a logical light grid, not screen-pixel path tracing. Default internal resolution is 160x90, with low/high presets at 80x45 and 320x180. Light cells store RGB, intensity, opacity, emission, reflectance, scatter, temperature and dirty state.

## Sources

Implemented source kinds:

- sun
- moon
- torch/fire
- window
- neon
- magic/signal
- water reflection
- ruin anomaly

## Propagation

`buildLightGridForCity` builds the grid from city state and applies:

- ambient light;
- directional sun/moon;
- point light radial falloff;
- tile opacity blocking;
- soft shadow approximation;
- bounce approximation capped by preset;
- water/wet surface reflection;
- fog/scatter approximation.

This is a physically inspired light approximation for pixel-art realism, not real global illumination or path tracing.

## Metrics

`computeLightMetrics` returns active light cells, blocked cells, emitted/reflected cells, `R_light`, `Phi_light` and finite checks. Too many active light cells increases `R_light`; stable finite lighting improves `Phi_light`.
