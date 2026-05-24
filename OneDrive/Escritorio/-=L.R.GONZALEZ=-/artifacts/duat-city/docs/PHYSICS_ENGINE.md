# PHYSICS_ENGINE

## Scope

Motor fisico 2D ligero para DUAT Agent City. No intenta ser un motor fisico realista completo; su funcion es evitar solapamientos, impedir cruces basicos por edificios solidos y producir metricas operativas (`R_physics`, `Phi_physics`).

## Integrador

- Semi-implicit Euler con `dt` fijo.
- `dt` se limita a `[0.01, 0.05]`.
- Cada cuerpo mantiene `prevX/prevY`, `vx/vy`, radio, masa, damping, `R`, `Phi_eff` y `gate`.
- `BLOCK` reduce velocidad por damping/factor de gate.

## Broad / Narrow Phase

- Broad phase: spatial hash con `cellSize` default `1.5`.
- Narrow phase: colision circulo-circulo con separacion por masa inversa e impulso simple.
- El hash evita el barrido `O(n^2)` completo en escenarios densos.

## Tile Collision

- `empty`, `road`, `plaza` y `garden` son transitables.
- Edificios solidos bloquean movimiento salvo el edificio objetivo de la tarea activa.
- Bounds de ciudad siempre hacen clamp y rebotan velocidad.

## Forces

- Seek hacia edificio/tile objetivo.
- Atraccion ligera a roads.
- Atraccion a market si hunger baja.
- Atraccion a clinic si safety/energy baja.
- Repulsion de ruins para roles no Scout/Observer.

## Metrics

- `bodyCount`
- `pairChecks`
- `resolvedCollisions`
- `unresolvedCollisions`
- `outOfBounds`
- `nanDetected`
- `frameCostEstimate`
- `R_physics`
- `Phi_physics`

`R_physics` sube por colisiones sin resolver, cuerpos fuera de bounds, NaN y presion alta de pares. `Phi_physics` mide resoluciones utiles sobre checks.

## Tests

- `physics.test.ts`
- `agentPhysicsAdapter.test.ts`
- `integrationV05.test.ts`

## Limits

- No pathfinding A* todavia.
- No constraints complejos.
- No rigid bodies poligonales.
- No Rapier/WebGL.
