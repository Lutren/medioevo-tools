import type { PlayableSceneState } from "../scene/sceneTypes";
import { createPixelBillboard } from "./isoBillboard";
import { gridToIsoWorld } from "./isoGrid";
import type { IsoBillboard, IsoGridConfig, IsoLightSource } from "./isoTypes";
import { DEFAULT_PIXEL_BILLBOARD_PALETTE } from "./pixelBillboardTypes";

export function createMaterialBillboards(scene: PlayableSceneState | undefined, grid: IsoGridConfig, lights: IsoLightSource[]): IsoBillboard[] {
  if (!scene) return [];
  return scene.materials.map(cell => {
    const position = gridToIsoWorld({ x: cell.x, y: cell.y }, grid, cell.material === "smoke" ? 0.9 : 0.12);
    const tint = materialTint(cell.material);
    return createPixelBillboard({
      id: `material-${cell.id}`,
      kind: "material",
      label: cell.material,
      position,
      tint,
      width: 16,
      height: cell.material === "smoke" ? 24 : 12,
      spriteKey: `procedural:material:${cell.material}`,
      metadata: { material: cell.material, wetness: cell.wetness ?? 0, temperature: cell.temperature ?? 0 },
    }, lights);
  });
}

function materialTint(material: string): string {
  switch (material) {
    case "water": return DEFAULT_PIXEL_BILLBOARD_PALETTE.water;
    case "fire": return DEFAULT_PIXEL_BILLBOARD_PALETTE.fire;
    case "smoke": return DEFAULT_PIXEL_BILLBOARD_PALETTE.smoke;
    case "neon": return DEFAULT_PIXEL_BILLBOARD_PALETTE.neon;
    case "stone": return "#7f8078";
    case "wood": return "#8a5c36";
    default: return "#b8a77c";
  }
}
