import type { CityState } from "../core/types";

export interface ArenaState {
  schema: "duat/vs-arena/v1.3";
  fighters: Array<{ id: string; faction: string; x: number; y: number; health: number; R: number }>;
  hazards: string[];
  tick: number;
}

export function createVsArenaState(city: CityState): ArenaState {
  const fighters = city.agents.slice(0, 2).map((agent, index) => ({
    id: agent.id,
    faction: index === 0 ? "archive" : "forge",
    x: 6 + index * 10,
    y: 3,
    health: 100,
    R: finite(agent.R),
  }));
  while (fighters.length < 2) {
    fighters.push({ id: `arena-bot-${fighters.length}`, faction: fighters.length === 0 ? "archive" : "forge", x: 6 + fighters.length * 10, y: 3, health: 100, R: 0.1 });
  }
  return {
    schema: "duat/vs-arena/v1.3",
    fighters,
    hazards: ["water slows", "fire damages", "neon reveals"],
    tick: city.tick,
  };
}

export function tickVsArena(arena: ArenaState): ArenaState {
  return {
    ...arena,
    tick: arena.tick + 1,
    fighters: arena.fighters.map((fighter, index) => ({
      ...fighter,
      x: finite(fighter.x + (index === 0 ? 0.15 : -0.15)),
      R: finite(Math.min(1, fighter.R + 0.001)),
    })),
  };
}

function finite(value: number): number {
  return Number.isFinite(value) ? Number(value.toFixed(3)) : 0;
}
