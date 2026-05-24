import type { CityState } from "../core/types";
import { gridToIsoWorld, sortIsoDepth } from "./isoGrid";
import { createPixelBillboard } from "./isoBillboard";
import type { IsoBillboard, IsoCamera, IsoGridConfig, IsoLightSource } from "./isoTypes";
import type { PixelBillboardPopulation } from "./pixelBillboardTypes";
import { createAgentBillboards } from "./pixelAgentBillboards";
import { createBuildingBillboards } from "./pixelBuildingBillboards";
import { createMaterialBillboards } from "./pixelMaterialBillboards";
import { createPropBillboards } from "./pixelPropBillboards";

export function createPixelBillboardPopulation(state: CityState, grid: IsoGridConfig, camera: IsoCamera, lights: IsoLightSource[]): PixelBillboardPopulation {
  return {
    agents: createAgentBillboards(state.agents, grid, camera, lights),
    buildings: createBuildingBillboards(state.buildings, grid, lights),
    props: createPropBillboards(state.objects, grid, lights),
    materials: createMaterialBillboards(state.playableScene, grid, lights),
    qglyphs: createQGlyphBillboards(state, grid, lights),
  };
}

export function flattenBillboardPopulation(population: PixelBillboardPopulation): IsoBillboard[] {
  return sortIsoDepth([...population.buildings, ...population.props, ...population.materials, ...population.agents, ...population.qglyphs]);
}

function createQGlyphBillboards(state: CityState, grid: IsoGridConfig, lights: IsoLightSource[]): IsoBillboard[] {
  return state.tiles
    .filter(tile => tile.R > 0.42 || tile.Phi_eff < 0.5)
    .slice(0, 48)
    .map(tile => createPixelBillboard({
      id: `qglyph-${tile.id}`,
      kind: "qglyph",
      label: tile.R > 0.55 ? "Q11" : "Q01",
      position: gridToIsoWorld({ x: tile.x, y: tile.y }, grid, 1.8),
      tint: tile.R > 0.55 ? "#dd6a6a" : "#d6b85a",
      width: 8,
      height: 8,
      spriteKey: tile.R > 0.55 ? "procedural:q:11" : "procedural:q:01",
      metadata: { tileId: tile.id, R: tile.R, Phi_eff: tile.Phi_eff },
    }, lights));
}
