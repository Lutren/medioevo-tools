import type { CityState } from "../core/types";

export interface MetroidvaniaModeScene {
  schema: "duat/metroidvania-mode-scene/v1.3";
  width: number;
  height: number;
  spawn: { x: number; y: number };
  doors: Array<{ id: string; target: string; lockedBy?: string }>;
  platforms: Array<{ x: number; y: number; w: number; material: string }>;
  npcs: string[];
}

export function createMetroidvaniaModeScene(city: CityState): MetroidvaniaModeScene {
  return {
    schema: "duat/metroidvania-mode-scene/v1.3",
    width: 64,
    height: 18,
    spawn: { x: 4, y: 12 },
    doors: city.buildings
      .filter(building => ["gatehouse", "ruin", "archive"].includes(building.type))
      .slice(0, 6)
      .map(building => ({ id: `door:${building.id}`, target: building.id, lockedBy: building.gate === "BLOCK" ? "ActionGate" : undefined })),
    platforms: city.tiles
      .filter(tile => tile.type !== "empty")
      .slice(0, 24)
      .map((tile, index) => ({ x: index * 3, y: 14 - (index % 4), w: 3, material: tile.type })),
    npcs: city.agents.slice(0, 8).map(agent => agent.id),
  };
}
