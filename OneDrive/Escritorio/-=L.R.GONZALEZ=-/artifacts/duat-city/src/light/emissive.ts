import type { Building, CityState } from "../core/types";
import type { RGB } from "../color/colorTypes";
import { kelvinToRgb } from "../color/temperature";
import type { LightSource, LightSourceKind } from "./lightTypes";

export function sourceForBuilding(building: Building, tick: number): LightSource | undefined {
  const kind = kindForBuilding(building.type);
  if (!kind) return undefined;
  const color = colorForKind(kind, building.gate);
  const flicker = kind === "neon" || kind === "ruin_anomaly" ? 0.88 + 0.12 * Math.sin((tick + building.x * 17) * 0.35) : 1;
  return {
    id: `building:${building.id}`,
    kind,
    x: building.x + 0.5,
    y: building.y + 0.5,
    radius: kind === "ruin_anomaly" ? 8 : kind === "window" ? 5 : 6,
    intensity: Math.max(0.15, Math.min(1, (0.35 + building.Phi_eff * 0.5) * flicker)),
    color,
    flicker,
  };
}

export function createCityLightSources(state: CityState): LightSource[] {
  const hour = (state.tick / 4) % 24;
  const night = hour < 6 || hour > 18;
  const sunOrMoon: LightSource = {
    id: night ? "directional:moon" : "directional:sun",
    kind: night ? "moon" : "sun",
    x: state.width * 0.35,
    y: state.height * 0.1,
    radius: Math.max(state.width, state.height),
    intensity: night ? 0.18 : 0.52,
    color: night ? kelvinToRgb(7600) : kelvinToRgb(5400),
    direction: night ? { x: -0.45, y: 0.65 } : { x: 0.35, y: 0.75 },
  };
  return [sunOrMoon, ...state.buildings.map(b => sourceForBuilding(b, state.tick)).filter(Boolean) as LightSource[]];
}

export function colorForKind(kind: LightSourceKind, gate?: string): RGB {
  if (gate === "BLOCK") return { r: 255, g: 62, b: 70 };
  if (gate === "REVIEW") return { r: 255, g: 204, b: 74 };
  switch (kind) {
    case "sun": return kelvinToRgb(5400);
    case "moon": return kelvinToRgb(7600);
    case "torch":
    case "fire":
      return kelvinToRgb(1900);
    case "window": return kelvinToRgb(2600);
    case "neon": return { r: 30, g: 232, b: 255 };
    case "water_reflection": return { r: 90, g: 185, b: 235 };
    case "ruin_anomaly": return { r: 164, g: 87, b: 255 };
    case "magic":
    case "signal":
      return { r: 92, g: 220, b: 190 };
  }
}

function kindForBuilding(type: Building["type"]): LightSourceKind | undefined {
  if (type === "market") return "neon";
  if (type === "clinic" || type === "archive" || type === "residential") return "window";
  if (type === "observatory" || type === "temple" || type === "gatehouse") return "signal";
  if (type === "ruin") return "ruin_anomaly";
  return undefined;
}
