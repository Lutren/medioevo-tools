import type { CityState } from "../core/types";
import type { RGB } from "../color/colorTypes";
import { clamp01 } from "../color/colorSpace";
import { createLightGrid, addLightSource, accumulateCellLight, getLightCell, setLightCell } from "./lightGrid";
import type { LightGrid, LightSource } from "./lightTypes";
import { createCityLightSources } from "./emissive";
import { applyTileOpacity, softShadowFactor } from "./shadowCaster";
import { applyWaterReflection } from "./reflection";
import { createPlayableSceneLightSources, sceneMaterialOpacity } from "../scene/sceneLighting";

export interface PropagationOptions {
  width?: number;
  height?: number;
  ambient?: RGB;
  bouncePasses?: number;
  fog?: number;
  intensityScale?: number;
}

export function buildLightGridForCity(state: CityState, options: PropagationOptions = {}): LightGrid {
  const grid = createLightGrid(options.width ?? 160, options.height ?? 90, options.ambient ?? ambientForState(state));
  for (const source of [...createCityLightSources(state), ...createPlayableSceneLightSources(state)]) {
    addLightSource(grid, projectSource({ ...source, intensity: source.intensity * (options.intensityScale ?? 1) }, state, grid));
  }
  applyTileOpacity(grid, state);
  applyPlayableSceneOpacity(grid, state);
  propagateSources(grid);
  const bounces = Math.max(0, Math.min(12, options.bouncePasses ?? 1));
  for (let i = 0; i < bounces; i++) bounceLight(grid);
  grid.bouncePasses = bounces;
  applyWaterReflection(grid, state);
  applyFog(grid, options.fog ?? fogForState(state));
  return grid;
}

export function propagateSources(grid: LightGrid): void {
  for (const source of grid.sources) {
    const sx = Math.floor(source.x);
    const sy = Math.floor(source.y);
    const radius = Math.max(1, Math.floor(source.radius));
    for (let y = Math.max(0, sy - radius); y <= Math.min(grid.height - 1, sy + radius); y++) {
      for (let x = Math.max(0, sx - radius); x <= Math.min(grid.width - 1, sx + radius); x++) {
        const d = Math.hypot(x - sx, y - sy);
        if (d > radius) continue;
        const falloff = (1 - d / radius) ** 1.7;
        const shadow = softShadowFactor(grid, source, x, y);
        const directional = source.direction ? Math.max(0.25, source.direction.x * ((x - sx) / radius) + source.direction.y * ((y - sy) / radius) + 0.65) : 1;
        const intensity = clamp01(source.intensity * falloff * shadow * directional * (source.flicker ?? 1));
        const cell = getLightCell(grid, x, y);
        if (cell) accumulateCellLight(cell, source.color, intensity);
      }
    }
  }
}

export function bounceLight(grid: LightGrid): void {
  const next = grid.cells.map(c => ({ ...c, emission: { ...c.emission } }));
  for (let y = 1; y < grid.height - 1; y++) {
    for (let x = 1; x < grid.width - 1; x++) {
      const cell = grid.cells[y * grid.width + x];
      if (cell.intensity <= 0.08 && cell.reflectance <= 0.04 && cell.scatter <= 0.02) continue;
      const share = cell.intensity * (0.018 + cell.reflectance * 0.028 + cell.scatter * 0.02);
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
        const n = next[(y + dy) * grid.width + x + dx];
        if (!n || n.opacity > 0.9) continue;
        n.intensity = clamp01(n.intensity + share * (1 - n.opacity));
        n.r = clamp01(n.r + cell.r * share * 0.35);
        n.g = clamp01(n.g + cell.g * share * 0.35);
        n.b = clamp01(n.b + cell.b * share * 0.35);
        n.dirty = true;
      }
    }
  }
  grid.cells = next;
}

export function applyFog(grid: LightGrid, fog: number): void {
  const amount = clamp01(fog);
  if (amount <= 0) return;
  for (let i = 0; i < grid.cells.length; i++) {
    const cell = grid.cells[i];
    cell.scatter = Math.max(cell.scatter, amount);
    cell.intensity = clamp01(cell.intensity + amount * 0.08);
    cell.dirty = true;
  }
}

function projectSource(source: LightSource, state: CityState, grid: LightGrid): LightSource {
  return {
    ...source,
    x: (source.x / state.width) * grid.width,
    y: (source.y / state.height) * grid.height,
    radius: (source.radius / Math.max(state.width, state.height)) * Math.max(grid.width, grid.height),
  };
}

function applyPlayableSceneOpacity(grid: LightGrid, state: CityState): void {
  const scene = state.playableScene;
  if (!scene) return;
  for (const cell of scene.materials) {
    const opacity = sceneMaterialOpacity(cell.material);
    if (opacity <= 0) continue;
    const x = Math.floor((cell.x / state.width) * grid.width);
    const y = Math.floor((cell.y / state.height) * grid.height);
    setLightCell(grid, x, y, { opacity, reflectance: cell.material === "water" || cell.wetness > 0.35 ? Math.max(0.35, cell.wetness) : 0.08 });
  }
}

function ambientForState(state: CityState): RGB {
  const hour = (state.tick / 4) % 24;
  if (hour < 6 || hour > 20) return { r: 13, g: 21, b: 39 };
  if (hour > 17) return { r: 48, g: 39, b: 47 };
  return { r: 55, g: 66, b: 70 };
}

function fogForState(state: CityState): number {
  const ruins = state.buildings.filter(b => b.type === "ruin").length;
  const water = state.tiles.filter(t => t.type === "water").length;
  return Math.min(0.22, ruins * 0.025 + water * 0.001);
}
