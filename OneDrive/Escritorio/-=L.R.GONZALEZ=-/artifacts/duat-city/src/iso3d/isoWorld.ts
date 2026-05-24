import type { CityState, TileType } from "../core/types";
import { createIsoGrid, createIsoWorldTile, sortIsoDepth } from "./isoGrid";
import type { IsoGridConfig, IsoWorldTile } from "./isoTypes";

const ELEVATION_BY_TILE: Partial<Record<TileType, number>> = {
  water: -0.18,
  road: 0,
  plaza: 0.02,
  forest: 0.18,
  garden: 0.1,
  residential: 0.7,
  workshop: 0.86,
  archive: 1.05,
  observatory: 1.28,
  market: 0.75,
  clinic: 0.72,
  academy: 0.9,
  theater: 0.95,
  temple: 1.1,
  ruin: 0.55,
  gatehouse: 1.2,
  stone: 0.2,
  wall: 1.35,
};

export function buildIsoWorldTiles(state: CityState, grid: IsoGridConfig = createIsoGrid(state.width, state.height)): IsoWorldTile[] {
  const tiles = state.tiles.map(tile => createIsoWorldTile({
    id: `tile-${tile.id}`,
    tileId: tile.id,
    grid: { x: tile.x, y: tile.y },
    type: tile.type,
    elevation: ELEVATION_BY_TILE[tile.type] ?? 0,
    R: finite(tile.R, 0),
    Phi_eff: finite(tile.Phi_eff, 0.7),
    gate: tile.R > 0.45 ? "REVIEW" : "APPROVE",
  }, grid));
  return sortIsoDepth(tiles);
}

export function estimateIsoMaterialCells(state: CityState): number {
  const playable = state.playableScene;
  const placed = playable?.materials?.length ?? 0;
  const wetTiles = state.tiles.filter(tile => tile.type === "water" || tile.type === "road").length;
  return Math.max(0, placed + wetTiles);
}

export function estimateIsoLightCells(state: CityState): number {
  const playableLights = state.playableScene?.lights?.length ?? 0;
  const emissiveBuildings = state.buildings.filter(building => ["market", "archive", "observatory", "workshop"].includes(building.type)).length;
  return Math.max(1, playableLights * 24 + emissiveBuildings * 8);
}

function finite(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}
