import type { CityState } from "../core/types";
import { gridToIsoWorld } from "./isoGrid";
import type { IsoGridConfig, IsoLightProfile, IsoLightSource, IsoVector3 } from "./isoTypes";

export function createIsoLightSources(state: CityState, grid: IsoGridConfig, profile: IsoLightProfile = "medioevo"): IsoLightSource[] {
  const ambient = light("ambient-main", "ambient", { x: 0, y: 0, z: 180 }, profile === "vermeer" ? "#d9c8a4" : "#bfc8d9", 0.26, 900, 0.9);
  const sources: IsoLightSource[] = [ambient];
  for (const building of state.buildings.slice(0, 28)) {
    if (!["archive", "market", "workshop", "observatory", "clinic"].includes(building.type)) continue;
    const pos = gridToIsoWorld({ x: building.x, y: building.y }, grid, 1.2);
    sources.push(light(`window-${building.id}`, "window", { ...pos, z: pos.z + 24 }, profile === "vermeer" ? "#ffd79a" : "#a7d8ff", 0.46, 120, 0.82));
  }
  for (const sceneLight of state.playableScene?.lights ?? []) {
    const pos = gridToIsoWorld({ x: sceneLight.x, y: sceneLight.y }, grid, 0.4);
    const color = sceneLight.kind === "neon" ? "#5ce7ff" : sceneLight.kind === "fire" ? "#ff9b45" : "#d8e8ff";
    sources.push(light(`scene-${sceneLight.id}`, sceneLight.kind === "neon" ? "neon" : sceneLight.kind === "fire" ? "fire" : "window", pos, color, 0.62, 140, 0.55));
  }
  return sources;
}

export function shadeIsoColor(base: string, brightness: number): string {
  const rgb = hexToRgb(base);
  const factor = clamp(brightness, 0.15, 1.65);
  return rgbToHex(rgb.r * factor, rgb.g * factor, rgb.b * factor);
}

export function sampleIsoLighting(position: IsoVector3, lights: IsoLightSource[]): number {
  let value = 0;
  for (const source of lights) {
    const dx = position.x - source.position.x;
    const dy = position.y - source.position.y;
    const dz = position.z - source.position.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    const falloff = Math.max(0, 1 - distance / Math.max(1, source.radius));
    value += source.intensity * falloff * (0.35 + source.softness * 0.65);
  }
  return clamp(value, 0.18, 1.45);
}

function light(id: string, kind: IsoLightSource["kind"], position: IsoVector3, color: string, intensity: number, radius: number, softness: number): IsoLightSource {
  return {
    id,
    kind,
    position,
    color: hexToRgb(color),
    intensity: clamp(intensity, 0, 2),
    radius: Math.max(1, radius),
    softness: clamp(softness, 0, 1),
  };
}

function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const clean = hex.replace("#", "");
  const value = Number.parseInt(clean.length === 3 ? clean.split("").map(char => char + char).join("") : clean, 16);
  return { r: (value >> 16) & 255, g: (value >> 8) & 255, b: value & 255 };
}

function rgbToHex(r: number, g: number, b: number): string {
  const bytes = [r, g, b].map(value => clamp(Math.round(value), 0, 255).toString(16).padStart(2, "0"));
  return `#${bytes.join("")}`;
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, Number.isFinite(value) ? value : min));
}
