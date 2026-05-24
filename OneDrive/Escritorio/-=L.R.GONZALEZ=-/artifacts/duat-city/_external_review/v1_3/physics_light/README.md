# DUAT Physics + Light + Mechanics Engine v1.3.0

**Fingerprint:** DUAT-v1.3.0-PHYSICS-LIGHT-MECHANICS-CPU

Motor unificado para DUAT/MEDIOEVO. CPU-first. Residue-first.

## Ciencia

- **Fibonacci-Möbius:** agregados estructurados, propagación lumínica, spatial hash
- **EML:** selector expansión/compresión para física, luz y render
- **OSIT:** cada celda y NPC es observador con estado
- **Q-State:** audio, luz, física y mecánicas bajo codificación unificada
- **Conway-Material:** reglas locales para materiales como personajes

## Estructura

```
src/
  core/         — FibMob, EML, OSIT, Q-State
  physics/      — SpatialHash, CellState, VerletEML, PhysicsEngine
  light/        — LightFieldFM, QStateLight, LightEML, LightBridge
  mechanics/    — NPCState, QuestEngine, GameMechanics
  render/       — DeltaFramebuffer, CPURenderer, IndexedPalette
  bridge/       — LightAudioBridge, PhysicsAudioBridge
  types/        — Tipos unificados
```

## Uso

```typescript
import { GameMechanics, makeCell } from '@workspace/duat-physics-light';

const game = new GameMechanics(config);
game.addCell(makeCell(100, 100, 'STONE', '10'));
game.addNPC('npc1', 'archivist', 100, 100);

const state = game.step();
console.log(state.metrics.R, state.metrics.Phi_eff);
```

## Estado

- INTERNO_LOCAL
- NO_PUBLICAR_SIN_GATE
- Wabi execution: disabled
- No cloud
- No assets sin allowlist
