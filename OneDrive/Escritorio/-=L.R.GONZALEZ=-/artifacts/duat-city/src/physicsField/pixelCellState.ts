import type { PixelCell, PixelMaterial } from "./pixelTypes";
import { makeCell } from "./materials";
import { getMaterialDefinition, evaluateMaterialRules } from "./materialRules";

export function createPhysicalPixelCell(material: PixelMaterial, active = false): PixelCell {
  const base = makeCell(material, active);
  const def = getMaterialDefinition(material);
  const rules = evaluateMaterialRules(material, base.wetness, 0);
  return {
    ...base,
    color: def.baseColor,
    density: def.density,
    opacity: def.opacity,
    reflectance: rules.reflectance,
    roughness: def.roughness,
    emissive: def.emissive,
    qState: rules.qState,
    vx: rules.velocity.x,
    vy: rules.velocity.y,
    active: active || def.emissive > 0.2 || material === "water" || material === "smoke" || material === "fire",
  };
}

export function updatePhysicalPixelCell(cell: PixelCell, tick: number): PixelCell {
  const rules = evaluateMaterialRules(cell.material, cell.wetness, tick);
  return {
    ...cell,
    temperature: Math.max(0, Math.min(1, cell.temperature + rules.heatDelta * 0.1)),
    wetness: Math.max(0, Math.min(1, cell.wetness + rules.wetnessDelta * 0.05)),
    vx: rules.velocity.x,
    vy: rules.velocity.y,
    light: Math.max(cell.light, rules.emitsLight ? 0.8 : cell.light * 0.98),
    reflectance: rules.reflectance,
    qState: rules.qState,
    active: cell.active || rules.emitsLight || Math.abs(rules.velocity.x) + Math.abs(rules.velocity.y) > 0.02,
  };
}
