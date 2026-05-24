import type { Building, CityState } from "../core/types";
import { mobiusField } from "../core/fibmob";
import { pointLightsForPlayableScene } from "../scene/sceneLighting";

export interface PointLight {
  id: string;
  x: number;
  y: number;
  radius: number;
  intensity: number;
  color: string;
}

export interface LightMap {
  width: number;
  height: number;
  ambient: number;
  values: number[];
  lights: PointLight[];
}

export function ambientLightForTick(tick: number): number {
  const hour = (tick / 4) % 24;
  const daylight = Math.max(0, Math.sin(((hour - 6) / 12) * Math.PI));
  return clamp01(0.22 + daylight * 0.58);
}

export function pointLightForBuilding(building: Building, tick: number): PointLight | undefined {
  const luminous = ["market", "clinic", "observatory", "archive", "temple", "gatehouse"].includes(building.type);
  if (!luminous) return undefined;
  const flicker = mobiusField(tick + building.x * 13 + building.y * 7, 1).mu === 0 ? 0.88 : 1;
  return {
    id: building.id,
    x: building.x + 0.5,
    y: building.y + 0.5,
    radius: building.type === "observatory" ? 7 : 5,
    intensity: clamp01((0.35 + building.Phi_eff * 0.45) * flicker),
    color: building.gate === "BLOCK" ? "#ff4444" : building.gate === "REVIEW" ? "#ffd166" : "#24e8ff",
  };
}

export function computeLightMap(state: CityState, width = 32, height = 24): LightMap {
  const ambient = ambientLightForTick(state.tick);
  const lights = [
    ...state.buildings.map(b => pointLightForBuilding(b, state.tick)).filter(Boolean) as PointLight[],
    ...pointLightsForPlayableScene(state.playableScene, state.tick),
  ];
  const values = new Array(width * height).fill(ambient);
  for (const light of lights) {
    const lx = Math.floor((light.x / state.width) * width);
    const ly = Math.floor((light.y / state.height) * height);
    const r = Math.max(1, Math.floor(light.radius));
    for (let y = Math.max(0, ly - r); y <= Math.min(height - 1, ly + r); y++) {
      for (let x = Math.max(0, lx - r); x <= Math.min(width - 1, lx + r); x++) {
        const d = Math.hypot(x - lx, y - ly);
        if (d > r) continue;
        const idx = y * width + x;
        values[idx] = clamp01(values[idx] + light.intensity * (1 - d / r));
      }
    }
  }
  return { width, height, ambient, values, lights };
}

export function sampleLight(map: LightMap, xNorm: number, yNorm: number): number {
  const x = Math.max(0, Math.min(map.width - 1, Math.floor(xNorm * map.width)));
  const y = Math.max(0, Math.min(map.height - 1, Math.floor(yNorm * map.height)));
  const value = map.values[y * map.width + x] ?? map.ambient;
  return clamp01(value);
}

export function applyLightOverlay(ctx: CanvasRenderingContext2D, map: LightMap, alpha = 0.45): void {
  const darkness = clamp01(1 - map.ambient);
  if (darkness <= 0.05) return;
  ctx.save();
  ctx.fillStyle = `rgba(2,7,12,${darkness * alpha})`;
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  ctx.restore();
}

function clamp01(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(1, value));
}
