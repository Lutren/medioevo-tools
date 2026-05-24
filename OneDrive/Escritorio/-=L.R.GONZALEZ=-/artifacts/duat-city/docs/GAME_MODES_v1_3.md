# GAME_MODES_v1_3

## Implemented Modes

- DUAT Interface: central OSIT/gates/handoff surface.
- Hormiguero: observer-only macro view with heatmap metrics.
- Agent Sims: select/follow agent with needs, task, memory and causal boundary.
- City President: indirect policy/resource control.
- Era Progression: fictional era game config, not historical claim.
- VS Arena: original 2D/2.5D arena prototype.
- RPG: isometric city RPG surface.
- Metroidvania: side-view exploration layer connected by gates.

## Runtime Rule

Mode state is serializable and separate from renderer state. Canvas remains playfield; DOM panels are mode controls.
