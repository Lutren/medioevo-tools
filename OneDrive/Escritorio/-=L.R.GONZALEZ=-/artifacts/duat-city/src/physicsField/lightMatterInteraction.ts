import type { LightCell } from "../light/lightTypes";
import type { PixelCell } from "./pixelTypes";
import { getMaterialDefinition } from "./materialRules";

export function interactLightWithMatter(light: LightCell, cell: PixelCell): LightCell {
  const material = getMaterialDefinition(cell.material);
  const reflectance = Math.max(material.reflectance, cell.reflectance ?? 0);
  const opacity = Math.max(material.opacity, cell.opacity ?? 0);
  const emissive = Math.max(material.emissive, cell.emissive ?? 0);
  return {
    ...light,
    intensity: clamp01(light.intensity * (1 - opacity * 0.55) + emissive * 0.35 + reflectance * 0.08),
    opacity: Math.max(light.opacity, opacity),
    reflectance: Math.max(light.reflectance, reflectance),
    scatter: Math.max(light.scatter, material.lightScatter),
    emission: {
      r: Math.max(light.emission.r, emissive * 255),
      g: Math.max(light.emission.g, emissive * (cell.material === "neon" ? 230 : 150)),
      b: Math.max(light.emission.b, emissive * (cell.material === "neon" ? 255 : 80)),
    },
    dirty: true,
  };
}

function clamp01(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(1, value));
}
