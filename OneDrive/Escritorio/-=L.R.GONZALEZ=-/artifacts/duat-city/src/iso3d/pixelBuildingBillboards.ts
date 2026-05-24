import type { Building } from "../core/types";
import { createPixelBillboard } from "./isoBillboard";
import { gridToIsoWorld } from "./isoGrid";
import type { IsoBillboard, IsoGridConfig, IsoLightSource } from "./isoTypes";
import { DEFAULT_PIXEL_BILLBOARD_PALETTE } from "./pixelBillboardTypes";

export function createBuildingBillboards(buildings: Building[], grid: IsoGridConfig, lights: IsoLightSource[], selectedBuildingId?: string): IsoBillboard[] {
  return buildings.map(building => {
    const position = gridToIsoWorld({ x: building.x, y: building.y }, grid, 0.95 + building.level * 0.15);
    return createPixelBillboard({
      id: `building-${building.id}`,
      kind: "building",
      label: building.name,
      position,
      tint: building.gate === "BLOCK" ? "#9f5a58" : DEFAULT_PIXEL_BILLBOARD_PALETTE.building,
      width: 32,
      height: 34 + building.level * 4,
      selected: selectedBuildingId === building.id,
      spriteKey: `procedural:building:${building.type}`,
      metadata: { type: building.type, level: building.level, R: building.R, Phi_eff: building.Phi_eff },
    }, lights);
  });
}
