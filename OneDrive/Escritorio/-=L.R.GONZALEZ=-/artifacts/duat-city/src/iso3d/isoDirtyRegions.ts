import type { IsoLayerKey } from "./isoTypes";

export interface IsoDirtyRegion {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  layers: IsoLayerKey[];
  reason: string;
}

export function createIsoDirtyRegion(x: number, y: number, reason: string, layers: IsoLayerKey[] = ["terrain", "lights"]): IsoDirtyRegion {
  return {
    id: `dirty-${Math.round(x)}-${Math.round(y)}`,
    x: finite(x),
    y: finite(y),
    width: 2,
    height: 2,
    layers,
    reason,
  };
}

export function mergeIsoDirtyRegions(regions: IsoDirtyRegion[]): IsoDirtyRegion[] {
  const byId = new Map<string, IsoDirtyRegion>();
  for (const region of regions) {
    if (!Number.isFinite(region.x) || !Number.isFinite(region.y)) continue;
    const existing = byId.get(region.id);
    if (!existing) byId.set(region.id, region);
    else byId.set(region.id, { ...existing, layers: Array.from(new Set([...existing.layers, ...region.layers])) });
  }
  return Array.from(byId.values()).sort((a, b) => a.id.localeCompare(b.id));
}

export function cameraChangeInvalidatesIsoLayers(): IsoLayerKey[] {
  return ["terrain", "buildings", "agents", "heatmap", "qglyphs"];
}

function finite(value: number): number {
  return Number.isFinite(value) ? value : 0;
}
