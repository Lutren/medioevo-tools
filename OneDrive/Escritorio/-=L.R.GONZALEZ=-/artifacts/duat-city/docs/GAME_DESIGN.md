# DUAT Agent City — Game Design Document

## Concept
A formal-lab city simulator where 12 DUAT synthetic agents live, work, and evolve
in a city built on Fibonacci-Möbius arithmetic. Four modes expose different layers:

- **CITY**: Build and shape the 48×32 grid. Place buildings, roads, plazas.
- **AGENT**: Inspect individual agents, their needs, relationships, memory.
- **RPG**: Export the city as a MEDIOEVO RPG world JSON with quests/factions/NPCs.
- **OSIT/DUAT**: Dashboard view with R, Φ_eff, witness log, handoff JSON.

## Grid
- 48 columns × 32 rows = 1,536 tiles
- Tile size: 16px at zoom=1
- Camera: pan (drag) + zoom (scroll wheel)
- Each tile has FibMob metadata from mobiusField(tileId)

## Building Types

| Type        | Produces             | Consumes  | R_delta | Notes                  |
|-------------|----------------------|-----------|---------|------------------------|
| residential | energy               | food      | −0.03   | Restores agent energy  |
| workshop    | materials            | energy    | −0.02   | Core production        |
| archive     | knowledge            | materials | −0.04   | R-reducing over time   |
| observatory | signal, knowledge    | energy    | −0.03   | Improves Φ_eff         |
| market      | food, trust          | materials | −0.02   | Social + trade hub     |
| clinic      | energy               | knowledge | −0.05   | Strongest R reducer    |
| academy     | knowledge, culture   | materials | −0.03   | Education              |
| garden      | food, culture        | —         | −0.02   | Passive food source    |
| plaza       | trust, culture       | —         | −0.02   | Social bonding         |
| temple      | trust, culture       | —         | −0.02   | Community cohesion     |
| ruin        | signal               | —         | +0.05   | ⚠ Increases R          |
| gatehouse   | trust                | energy    | −0.01   | Security               |

## Agent Roles (12 agents)
Observer · Engineer · Archivist · Medic · Builder · Trader ·
Teacher · Scout · Gatekeeper · Storykeeper · Artisan · Courier

Each role has task preferences (ROLE_TASK_PREFS) that guide idle behavior.

## Simulation Loop (per tick, ~200ms at 1x speed)
1. Building production — resources change
2. Schedule new tasks for idle/needy agents
3. Activate pending tasks
4. Agent update: decay needs → move toward building → restore needs → step task
5. Update relationships (proximity bonding, competition)
6. Compute global R, Φ_eff, regime, gate
7. Generate events (risk alerts, RPG hooks, prosperity)
8. Witness log entry every 25 ticks

## Persistence
- Auto-save every 15 seconds to localStorage
- Manual Save/Load buttons
- Export Handoff JSON (OSIT mode)
- Export RPG World JSON (RPG mode)

## Progression
- Start: 6 buildings, 12 agents, balanced resources
- Goal: Maintain R < 0.35 (APPROVE gate)
- Expand: Add buildings when Φ_eff > 0.80
- Compress: Pause expansion when gate = BLOCK
- Crisis events generate quests → RPG world enriches

## RPG World Export
When city has ≥ 3 buildings, RPG export is enabled.
Output includes:
- Locations (one per building, with lore tags)
- NPCs (one per agent, with quest_giver flag)
- 6 Factions derived from building types
- Quests triggered by resource/R conditions
- Encounters (5 procedural events)
- Full handoff JSON embedded
