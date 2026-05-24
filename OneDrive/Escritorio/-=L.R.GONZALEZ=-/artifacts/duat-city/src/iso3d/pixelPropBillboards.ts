import type { CityObject } from "../core/types";
import { createPixelBillboard } from "./isoBillboard";
import { gridToIsoWorld } from "./isoGrid";
import type { IsoBillboard, IsoGridConfig, IsoLightSource } from "./isoTypes";

export function createPropBillboards(objects: CityObject[], grid: IsoGridConfig, lights: IsoLightSource[]): IsoBillboard[] {
  return objects.slice(0, 80).map(object => createPixelBillboard({
    id: `prop-${object.id}`,
    kind: "prop",
    label: object.name,
    position: gridToIsoWorld({ x: object.x, y: object.y }, grid, 0.55),
    tint: "#b79c68",
    width: 14,
    height: 18,
    spriteKey: `procedural:prop:${object.defId}`,
    metadata: { buildingId: object.buildingId, R: object.R, Phi_eff: object.Phi_eff },
  }, lights));
}
