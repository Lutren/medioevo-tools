import type { CityState } from "../core/types";
import type { PixelRealismConfig } from "./renderPasses";

export interface DirtyRegionState {
  width: number;
  height: number;
  regionSize: number;
  dirty: Set<string>;
  cameraKey?: string;
}

export function createDirtyRegionState(width: number, height: number, regionSize = 16): DirtyRegionState {
  return { width, height, regionSize: Math.max(1, regionSize), dirty: new Set<string>() };
}

export function markCellDirty(state: DirtyRegionState, x: number, y: number): DirtyRegionState {
  if (!Number.isFinite(x) || !Number.isFinite(y)) return state;
  const rx = Math.max(0, Math.min(Math.ceil(state.width / state.regionSize) - 1, Math.floor(x / state.regionSize)));
  const ry = Math.max(0, Math.min(Math.ceil(state.height / state.regionSize) - 1, Math.floor(y / state.regionSize)));
  state.dirty.add(`${rx},${ry}`);
  return state;
}

export function markCameraDirty(state: DirtyRegionState, cameraKey: string): DirtyRegionState {
  if (state.cameraKey === cameraKey) return state;
  state.cameraKey = cameraKey;
  const cols = Math.ceil(state.width / state.regionSize);
  const rows = Math.ceil(state.height / state.regionSize);
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) state.dirty.add(`${x},${y}`);
  }
  return state;
}

export function shouldSkipStableRegion(state: DirtyRegionState, regionX: number, regionY: number): boolean {
  return !state.dirty.has(`${regionX},${regionY}`);
}

export function consumeDirtyRegions(state: DirtyRegionState): string[] {
  const regions = [...state.dirty].sort();
  state.dirty.clear();
  return regions;
}

export function dirtyRegionCount(state: DirtyRegionState): number {
  return state.dirty.size;
}

export function lightDirtySignature(state: CityState, config: PixelRealismConfig): string {
  const scene = state.playableScene;
  const sceneMaterials = scene?.materials
    .map(cell => `${cell.x},${cell.y},${cell.material},${Math.round(cell.wetness * 10)},${cell.qState}`)
    .sort()
    .join(";") ?? "";
  const sceneLights = scene?.lights
    .map(light => `${light.x},${light.y},${light.kind},${Math.round(light.intensity * 10)},${light.active ? 1 : 0}`)
    .sort()
    .join(";") ?? "";
  const buildings = state.buildings
    .map(building => `${building.id}:${building.x},${building.y}:${building.type}:${building.gate}:${Math.round(building.Phi_eff * 20)}`)
    .join(";");
  return [
    state.width,
    state.height,
    config.qualityPreset,
    config.lightIntensity.toFixed(2),
    config.timeOfDay,
    config.weather,
    config.lightProfile,
    scene?.timeOfDay ?? "",
    scene?.weather ?? "",
    scene?.activeVibe?.id ?? "",
    sceneMaterials,
    sceneLights,
    buildings,
  ].join("|");
}
