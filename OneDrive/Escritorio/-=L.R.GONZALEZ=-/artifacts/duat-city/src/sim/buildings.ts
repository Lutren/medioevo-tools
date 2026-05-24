import type { Building, TileType, ResourceKey } from "../core/types";
import { uid, type RandomSource } from "../core/math";

export interface BuildingDef {
  label: string;
  produces: Partial<Record<ResourceKey, number>>;
  consumes: Partial<Record<ResourceKey, number>>;
  R_delta: number;
  Phi_delta: number;
  capacity: number;
  description: string;
}

export const BUILDING_DEFS: Record<TileType, BuildingDef | null> = {
  empty: null,
  road: null,
  plaza: { label: "Plaza", produces: { trust: 1, culture: 1 }, consumes: {}, R_delta: -0.02, Phi_delta: 0.01, capacity: 0, description: "Social gathering" },
  residential: { label: "Residence", produces: { energy: 2 }, consumes: { food: 1 }, R_delta: -0.03, Phi_delta: 0.02, capacity: 4, description: "Houses agents, restores energy" },
  workshop: { label: "Workshop", produces: { materials: 3 }, consumes: { energy: 1 }, R_delta: -0.02, Phi_delta: 0.03, capacity: 3, description: "Produces materials" },
  archive: { label: "Archive", produces: { knowledge: 2 }, consumes: { materials: 1 }, R_delta: -0.04, Phi_delta: 0.04, capacity: 2, description: "Stores knowledge, generates evidence" },
  observatory: { label: "Observatory", produces: { signal: 2, knowledge: 1 }, consumes: { energy: 1 }, R_delta: -0.03, Phi_delta: 0.05, capacity: 2, description: "Detects events, improves Phi_eff" },
  market: { label: "Market", produces: { food: 2, trust: 2 }, consumes: { materials: 1 }, R_delta: -0.02, Phi_delta: 0.02, capacity: 4, description: "Trades resources, builds trust" },
  clinic: { label: "Clinic", produces: { energy: 3 }, consumes: { knowledge: 1 }, R_delta: -0.05, Phi_delta: 0.04, capacity: 2, description: "Heals agents, reduces R" },
  academy: { label: "Academy", produces: { knowledge: 3, culture: 2 }, consumes: { materials: 1 }, R_delta: -0.03, Phi_delta: 0.05, capacity: 3, description: "Teaches, generates culture" },
  theater: { label: "Theater", produces: { culture: 3, trust: 1 }, consumes: { energy: 1 }, R_delta: -0.02, Phi_delta: 0.04, capacity: 3, description: "Creates agent profiles and origin stories" },
  temple: { label: "Temple", produces: { trust: 2, culture: 3 }, consumes: {}, R_delta: -0.02, Phi_delta: 0.03, capacity: 2, description: "Community cohesion" },
  garden: { label: "Garden", produces: { food: 3, culture: 1 }, consumes: {}, R_delta: -0.02, Phi_delta: 0.02, capacity: 2, description: "Grows food, social" },
  ruin: { label: "Ruin", produces: { signal: 1 }, consumes: {}, R_delta: 0.05, Phi_delta: -0.03, capacity: 0, description: "Unresolved anomaly — investigate!" },
  gatehouse: { label: "Gatehouse", produces: { trust: 1 }, consumes: { energy: 1 }, R_delta: -0.01, Phi_delta: 0.01, capacity: 2, description: "City defense" },
  water: null,
  forest: null,
  stone: null,
  wall: null,
};

export function createBuilding(type: TileType, x: number, y: number, rng?: RandomSource): Building {
  const def = BUILDING_DEFS[type];
  const label = def?.label ?? type;
  return {
    id: uid(rng),
    type,
    name: `${label} (${x},${y})`,
    x,
    y,
    level: 1,
    workers: [],
    residents: [],
    storage: {},
    R: 0.1,
    Phi_eff: 0.9,
    gate: "APPROVE",
  };
}

export function tickBuilding(
  building: Building,
  resources: Record<ResourceKey, number>
): { building: Building; resourceDelta: Partial<Record<ResourceKey, number>> } {
  const def = BUILDING_DEFS[building.type];
  if (!def) return { building, resourceDelta: {} };

  const delta: Partial<Record<ResourceKey, number>> = {};

  // Production scales with workers (min 0.5 if no workers for passive buildings)
  const workerBonus = building.workers.length > 0 ? 1 + building.workers.length * 0.3 : 0.5;

  for (const [key, amount] of Object.entries(def.produces)) {
    const k = key as ResourceKey;
    delta[k] = (delta[k] ?? 0) + Math.round((amount as number) * workerBonus);
  }

  // Consumption
  for (const [key, amount] of Object.entries(def.consumes)) {
    const k = key as ResourceKey;
    const available = resources[k] ?? 0;
    const consumed = Math.min(available, (amount as number));
    delta[k] = (delta[k] ?? 0) - consumed;
  }

  const updatedBuilding: Building = {
    ...building,
    R: Math.max(0, Math.min(1, building.R + def.R_delta * 0.1)),
    Phi_eff: Math.max(0, Math.min(1, building.Phi_eff + def.Phi_delta * 0.1)),
  };

  return { building: updatedBuilding, resourceDelta: delta };
}

export function getBuildingAt(buildings: Building[], x: number, y: number): Building | undefined {
  return buildings.find(b => b.x === x && b.y === y);
}

export function getBuildingById(buildings: Building[], id: string): Building | undefined {
  return buildings.find(b => b.id === id);
}

export function getBuildingsByType(buildings: Building[], type: TileType): Building[] {
  return buildings.filter(b => b.type === type);
}
