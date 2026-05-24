import type { CityState } from "../core/types";
import type { IsoLayerCacheEntry, IsoLayerKey } from "./isoTypes";

export interface IsoLayerCacheState {
  entries: IsoLayerCacheEntry[];
  hitRatio: number;
}

const LAYERS: IsoLayerKey[] = ["terrain", "buildings", "lights", "agents", "heatmap", "qglyphs", "ui"];

export function computeIsoLayerDirtyKeys(state: CityState): Record<IsoLayerKey, string> {
  const weather = state.playableScene?.weather ?? "clear";
  const sceneTick = state.playableScene?.tick ?? 0;
  return {
    terrain: `${state.width}x${state.height}:${state.tiles.length}:${state.tiles.filter(tile => tile.type === "water").length}`,
    buildings: `${state.buildings.length}:${state.buildings.map(building => `${building.id}:${building.level}:${building.gate}`).join("|")}`,
    lights: `${state.tick >> 3}:${weather}:${state.playableScene?.lights?.length ?? 0}`,
    agents: `${state.tick}:${state.agents.map(agent => `${agent.id}:${agent.x}:${agent.y}:${agent.gate}`).join("|")}`,
    heatmap: `${state.tick >> 4}:${round(state.R)}:${round(state.Phi_eff)}`,
    qglyphs: `${state.tick >> 4}:${state.quaternary?.counts?.["11"] ?? 0}:${state.tiles.filter(tile => tile.R > 0.42).length}`,
    ui: `${state.regime}:${state.gate}:${sceneTick}`,
  };
}

export function updateIsoLayerCache(previous: IsoLayerCacheState | undefined, state: CityState): IsoLayerCacheState {
  const dirtyKeys = computeIsoLayerDirtyKeys(state);
  const previousByLayer = new Map((previous?.entries ?? []).map(entry => [entry.key, entry]));
  let reused = 0;
  const entries = LAYERS.map(key => {
    const prior = previousByLayer.get(key);
    const isReused = prior?.dirtyKey === dirtyKeys[key];
    if (isReused) reused += 1;
    return {
      key,
      dirtyKey: dirtyKeys[key],
      reused: isReused,
      lastUpdatedTick: isReused ? prior.lastUpdatedTick : state.tick,
    };
  });
  return { entries, hitRatio: round(reused / LAYERS.length) };
}

function round(value: number): number {
  return Number((Number.isFinite(value) ? value : 0).toFixed(3));
}
