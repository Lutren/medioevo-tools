import type { CityState, Tile, TileType } from "../core/types";
import { mobiusField } from "../core/fibmob";
import { makeDefaultResources } from "./resources";
import { createBuilding } from "./buildings";
import { createInitialAgents } from "./agents";
import { computeRegime, computeGate, computePhiEff } from "../core/metrics";
import { clamp, seededRandom } from "../core/math";
import { createObjectsForBuilding, createObjectsForBuildings } from "./objects";
import { createDefaultCityContext } from "./cityContext";

const CITY_W = 48;
const CITY_H = 32;

function makeTile(id: number, x: number, y: number, type: TileType = "empty"): Tile {
  const mb = mobiusField(id + 1, 1);
  return {
    id,
    x,
    y,
    type,
    fibmob: {
      mu: mb.mu,
      lodFactor: mb.lodFactor,
      polarity: mb.polarity,
      rarity: mb.rarity,
    },
    R: mb.mu === 0 ? 0.3 : 0.1,
    Phi_eff: mb.mu === 0 ? 0.5 : 0.85,
  };
}

export function createCity(seed: string | number = "duat-city-default"): CityState {
  const rng = seededRandom(seed);
  const tiles: Tile[] = [];
  for (let y = 0; y < CITY_H; y++) {
    for (let x = 0; x < CITY_W; x++) {
      const id = y * CITY_W + x;
      tiles.push(makeTile(id, x, y, "empty"));
    }
  }

  // Lay initial roads
  const cx = Math.floor(CITY_W / 2);
  const cy = Math.floor(CITY_H / 2);
  // Horizontal road
  for (let x = cx - 8; x <= cx + 8; x++) tiles[cy * CITY_W + x].type = "road";
  // Vertical road
  for (let y = cy - 5; y <= cy + 5; y++) tiles[y * CITY_W + cx].type = "road";

  const buildings = [
    createBuilding("residential", cx - 3, cy - 2, rng),
    createBuilding("residential", cx + 3, cy - 2, rng),
    createBuilding("workshop", cx - 3, cy + 2, rng),
    createBuilding("garden", cx + 3, cy + 2, rng),
    createBuilding("market", cx, cy - 3, rng),
    createBuilding("archive", cx - 5, cy, rng),
    createBuilding("clinic", cx + 5, cy, rng),
    createBuilding("academy", cx - 6, cy - 3, rng),
    createBuilding("theater", cx + 6, cy + 3, rng),
  ];

  for (const b of buildings) {
    const tileIdx = b.y * CITY_W + b.x;
    if (tileIdx >= 0 && tileIdx < tiles.length) {
      tiles[tileIdx].type = b.type;
      tiles[tileIdx].buildingId = b.id;
    }
  }

  const agents = createInitialAgents(CITY_W, CITY_H, rng);
  // Assign home/workplace
  agents.forEach((a, i) => {
    if (buildings[0]) a.homeId = buildings[i % 2]?.id;
    if (buildings[2]) a.workplaceId = buildings[2 + (i % 3)]?.id;
  });

  const resources = makeDefaultResources();
  const objects = createObjectsForBuildings(buildings);
  const districts = [
    {
      id: "central-cross",
      name: "Central Cross",
      tileIds: tiles
        .filter(t => Math.abs(t.x - cx) <= 8 && Math.abs(t.y - cy) <= 5)
        .map(t => t.id),
      zoning: "mixed" as const,
      growth: 0.18,
      maintenance: 0.82,
      risk: 0.12,
    },
  ];

  return {
    width: CITY_W,
    height: CITY_H,
    tick: 0,
    tiles,
    buildings,
    agents,
    tasks: [],
    objects,
    districts,
    context: createDefaultCityContext(),
    resources,
    events: [],
    witnesslog: [],
    R: 0.15,
    Phi_eff: 0.82,
    regime: "FUNCIONAL",
    gate: "APPROVE",
  };
}

export function placeTile(state: CityState, x: number, y: number, type: TileType): CityState {
  if (x < 0 || x >= state.width || y < 0 || y >= state.height) return state;
  const idx = y * state.width + x;
  const tiles = [...state.tiles];

  // Remove existing building if any
  const existing = tiles[idx];
  let buildings = state.buildings;
  let objects = state.objects ?? [];
  if (existing.buildingId) {
    buildings = buildings.filter(b => b.id !== existing.buildingId);
    objects = objects.filter(obj => obj.buildingId !== existing.buildingId);
  }

  tiles[idx] = { ...tiles[idx], type, buildingId: undefined };

  if (isBuildingTile(type)) {
    const rng = seededRandom(`place:${state.tick}:${x}:${y}:${type}:${state.buildings.length}`);
    const building = createBuilding(type, x, y, rng);
    tiles[idx].buildingId = building.id;
    buildings = [...buildings, building];
    objects = [...objects, ...createObjectsForBuilding(building)];
  }

  return { ...state, tiles, buildings, objects };
}

export function eraseTile(state: CityState, x: number, y: number): CityState {
  return placeTile(state, x, y, "empty");
}

export function computeGlobalR(state: CityState): number {
  const agentRs = state.agents.map(a => a.R);
  const avgAgentR = agentRs.length > 0 ? agentRs.reduce((s, r) => s + r, 0) / agentRs.length : 0;

  const failedTasks = state.tasks.filter(t => t.status === "failed").length;
  const totalTasks = state.tasks.length;
  const failRate = totalTasks > 0 ? failedTasks / totalTasks : 0;

  const resourceR = state.resources.food < 20 ? 0.1 : 0;
  const ruinR = state.buildings.filter(b => b.type === "ruin").length * 0.04;
  const fieldR = state.fieldMetrics ? state.fieldMetrics.R_field * 0.12 : 0;

  return clamp(avgAgentR * 0.4 + failRate * 0.3 + resourceR + ruinR + fieldR, 0, 1);
}

export function isBuildingTile(type: TileType): boolean {
  return !["empty", "road", "water", "forest", "stone", "wall"].includes(type);
}
