# ENGINE_FIX_QUEUE

## P0 corregido en este ciclo

- Aleatoriedad no inyectada en sim core:
  - `src/core/math.ts`
  - `src/sim/agents.ts`
  - `src/sim/buildings.ts`
  - `src/sim/needs.ts`
  - `src/sim/tasks.ts`
  - `src/sim/scheduler.ts`
  - `src/sim/events.ts`
  - `src/sim/city.ts`
  - `src/sim/engine.ts`
- Aleatoriedad en RPG encounter generator:
  - `src/rpg/encounterGenerator.ts`
- Test agregado:
  - `src/tests/engine.test.ts`

## P0 pendiente

- `quaternaryAdapter` usa sensor bank global de modulo. Mover historia a `CityState` o a runtime explicitamente inyectado.
- `core/witnesslog.ts` usa contador global. Cambiar a contador state-local o hash por tick/evento.
- Crear replay hash real por tick.

## P1 pendiente

- Sacar tick loop de React state hacia worker/external store.
- Unificar `graphics/lightEngine`, `lightPropagation` y `vermeerIsoLighting`.
- Crear benchmark vivo de FPS/tick/ms/agent_count, no solo validacion de reportes.
- Probar memory smoke en ciudad/dungeon/metroidvania.

## P2 pendiente

- Audio: cerrar/desconectar `AudioContext` y nodos en `proceduralSynth.disable()`.
- Placeholder UI en `src/components/ui/sidebar.tsx` usa `Math.random`; bajo riesgo, no sim.
- Sprite lighting benchmark.
- Godot proof-of-concept solo despues de contratos.

