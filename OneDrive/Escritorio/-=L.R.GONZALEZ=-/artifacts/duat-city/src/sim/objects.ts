import type { Building, CityObject, ObjectDef, TileType } from "../core/types";
import { clamp } from "../core/math";

export const OBJECT_DEFS: ObjectDef[] = [
  {
    id: "bed",
    name: "Bed",
    category: "rest",
    buildingTypes: ["residential"],
    effects: { energy: 0.28, safety: 0.04, R_delta: -0.02, Phi_delta: 0.01 },
    sprite: "object/bed",
  },
  {
    id: "table",
    name: "Table",
    category: "food",
    buildingTypes: ["residential", "plaza"],
    effects: { hunger: 0.12, social: 0.06, R_delta: -0.01 },
    sprite: "object/table",
  },
  {
    id: "archive-desk",
    name: "Archive Desk",
    category: "archive",
    buildingTypes: ["archive"],
    effects: { curiosity: 0.14, purpose: 0.08, R_delta: -0.025, Phi_delta: 0.025 },
    sprite: "object/archive-desk",
  },
  {
    id: "market-stall",
    name: "Market Stall",
    category: "food",
    buildingTypes: ["market"],
    effects: { hunger: 0.24, social: 0.08, R_delta: -0.02, resource_delta: { food: -1 } },
    sprite: "object/market-stall",
  },
  {
    id: "clinic-bed",
    name: "Clinic Bed",
    category: "health",
    buildingTypes: ["clinic"],
    effects: { safety: 0.22, energy: 0.06, R_delta: -0.025, Phi_delta: 0.015 },
    sprite: "object/clinic-bed",
  },
  {
    id: "workbench",
    name: "Workbench",
    category: "work",
    buildingTypes: ["workshop"],
    effects: { purpose: 0.16, R_delta: -0.015, Phi_delta: 0.015, resource_delta: { materials: 1 } },
    sprite: "object/workbench",
  },
  {
    id: "observatory-lens",
    name: "Observatory Lens",
    category: "learning",
    buildingTypes: ["observatory", "academy"],
    effects: { curiosity: 0.18, purpose: 0.08, R_delta: -0.02, Phi_delta: 0.03 },
    sprite: "object/observatory-lens",
  },
  {
    id: "theater-stage",
    name: "Theater Stage",
    category: "learning",
    buildingTypes: ["theater"],
    effects: { social: 0.08, purpose: 0.12, curiosity: 0.08, R_delta: -0.02, Phi_delta: 0.02 },
    sprite: "object/theater-stage",
  },
  {
    id: "garden-plot",
    name: "Garden Plot",
    category: "garden",
    buildingTypes: ["garden"],
    effects: { hunger: 0.12, safety: 0.04, R_delta: -0.015, resource_delta: { food: 1 } },
    sprite: "object/garden-plot",
  },
  {
    id: "ruin-relic",
    name: "Ruin Relic",
    category: "ruin",
    buildingTypes: ["ruin"],
    effects: { curiosity: 0.16, safety: -0.06, R_delta: 0.02, Phi_delta: 0.01 },
    sprite: "object/ruin-relic",
  },
  {
    id: "gate-lever",
    name: "Gate Lever",
    category: "gate",
    buildingTypes: ["gatehouse"],
    effects: { purpose: 0.12, safety: 0.05, R_delta: -0.015, Phi_delta: 0.015 },
    sprite: "object/gate-lever",
  },
];

export function objectDefsForBuilding(type: TileType): ObjectDef[] {
  return OBJECT_DEFS.filter(def => def.buildingTypes.includes(type));
}

export function createObjectsForBuilding(building: Building): CityObject[] {
  return objectDefsForBuilding(building.type).map((def, index) => ({
    id: `${building.id}:${def.id}`,
    defId: def.id,
    name: def.name,
    buildingId: building.id,
    x: building.x + 0.18 * (index % 2),
    y: building.y + 0.18 * Math.floor(index / 2),
    R: clamp(building.R + (def.category === "ruin" ? 0.12 : -0.02), 0, 1),
    Phi_eff: clamp(building.Phi_eff + (def.category === "learning" ? 0.04 : 0), 0, 1),
  }));
}

export function createObjectsForBuildings(buildings: Building[]): CityObject[] {
  return buildings.flatMap(createObjectsForBuilding);
}

export function getObjectDef(defId: string): ObjectDef | undefined {
  return OBJECT_DEFS.find(def => def.id === defId);
}
