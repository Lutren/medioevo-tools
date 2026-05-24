# VERMEER_LIGHTING_MODEL_NOTES

## Objetivo artistico

Iluminacion estilo Vermeer: pocas fuentes, contraste alto, penumbra, caida por distancia, y solo se ilumina lo que la fuente alcanza.

## Modelo operacional

```txt
I(p, l) =
  I0_l
  * cone_l(p)
  * occlusion_l(p)
  / (1 + k_l * distance(p, l)^2)
```

```txt
Light(p) =
  ambient_floor
  + sum(active_lights_near_camera I(p, l))
  + optional_bounce(p)
```

## Presupuesto

Low:
- 1 a 3 luces activas.
- Grid bajo.
- Sin bounce.
- Sombras blob/contact.

Medium:
- 3 a 6 luces.
- Occlusion por tiles.
- Penumbra por blur barato.

High:
- 6 a 12 luces.
- Bounce simplificado 1 pasada.
- Sombras selectivas.

Beautiful:
- Solo cerca de camara.
- Bounce 1-2 pasadas.
- Reflejos/fog si FPS lo permite.

## Estado actual

- `graphics/lightEngine.ts`: simple y barato.
- `light/lightPropagation.ts`: mejor base tecnica para falloff/occlusion/bounce.
- `iso3d/vermeerIsoLighting.ts`: direccion artistica, no modelo fisico completo.

## Accion recomendada

Crear `LightingBackend`:
- `simple_canvas`
- `propagation_grid`
- `vermeer_iso`

Todos consumen `LightBudget` y reportan costo.

