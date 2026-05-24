import type { CityState } from "../core/types";
import type { RGB } from "../color/colorTypes";
import { colorForKind } from "../light/emissive";
import type { LightSource } from "../light/lightTypes";
import type { PointLight } from "../graphics/lightEngine";
import type { PlacedLightSource, PlacedMaterialCell, PlayableLightKind, PlayableSceneState } from "./sceneTypes";

export function createPlayableSceneLightSources(state: CityState): LightSource[] {
  const scene = state.playableScene;
  if (!scene) return [];
  const lightSources = scene.lights
    .filter(light => light.active)
    .map(light => sceneLightToSource(light, state.tick));
  const materialSources = scene.materials
    .filter(cell => cell.material === "fire" || cell.material === "neon")
    .map(cell => sceneMaterialToSource(cell, state.tick));
  const reflectionSources = scene.materials
    .filter(cell => cell.material === "water" && cell.wetness > 0.5)
    .slice(0, 10)
    .map(cell => ({
      id: `scene-reflection:${cell.id}`,
      kind: "water_reflection" as const,
      x: cell.x + 0.5,
      y: cell.y + 0.5,
      radius: 4,
      intensity: 0.2 + cell.wetness * 0.22,
      color: { r: 90, g: 185, b: 235 },
      flicker: 1,
    }));
  return [...lightSources, ...materialSources, ...reflectionSources];
}

export function pointLightsForPlayableScene(scene: PlayableSceneState | undefined, tick: number): PointLight[] {
  if (!scene) return [];
  const fromLights = scene.lights.filter(light => light.active).map(light => ({
    id: light.id,
    x: light.x + 0.5,
    y: light.y + 0.5,
    radius: light.radius,
    intensity: light.intensity,
    color: light.color,
  }));
  const fromMaterials = scene.materials
    .filter(cell => cell.material === "fire" || cell.material === "neon")
    .map(cell => ({
      id: cell.id,
      x: cell.x + 0.5,
      y: cell.y + 0.5,
      radius: cell.material === "neon" ? 6 : 5,
      intensity: cell.material === "neon" ? 0.85 + Math.sin(tick * 0.5 + cell.x) * 0.12 : Math.max(0.5, cell.light),
      color: cell.material === "neon" ? "#22e8ff" : "#ff7a2f",
    }));
  return [...fromLights, ...fromMaterials];
}

export function sceneMaterialOpacity(material: PlacedMaterialCell["material"]): number {
  if (material === "stone") return 0.82;
  if (material === "wood") return 0.5;
  if (material === "smoke") return 0.24;
  if (material === "water") return 0.12;
  return 0.04;
}

function sceneLightToSource(light: PlacedLightSource, tick: number): LightSource {
  return {
    id: `scene:${light.id}`,
    kind: light.kind,
    x: light.x + 0.5,
    y: light.y + 0.5,
    radius: light.radius,
    intensity: light.kind === "neon" || light.kind === "ruin_anomaly"
      ? Math.max(0.4, light.intensity * (0.92 + Math.sin(tick * 0.45 + light.x) * 0.08))
      : light.intensity,
    color: parseColor(light.color) ?? colorForSceneKind(light.kind),
    flicker: light.kind === "neon" || light.kind === "ruin_anomaly" ? 0.92 + Math.sin(tick * 0.45 + light.x) * 0.08 : 1,
  };
}

function sceneMaterialToSource(cell: PlacedMaterialCell, tick: number): LightSource {
  return {
    id: `scene-material:${cell.id}`,
    kind: cell.material === "neon" ? "neon" : "fire",
    x: cell.x + 0.5,
    y: cell.y + 0.5,
    radius: cell.material === "neon" ? 6 : 5,
    intensity: cell.material === "neon" ? 0.9 + Math.sin(tick * 0.5 + cell.x) * 0.08 : Math.max(0.45, cell.light),
    color: cell.material === "neon" ? { r: 34, g: 232, b: 255 } : { r: 255, g: 122, b: 47 },
    flicker: 0.9 + Math.sin(tick * 0.8 + cell.x) * 0.1,
  };
}

function colorForSceneKind(kind: PlayableLightKind): RGB {
  return colorForKind(kind);
}

function parseColor(input: string): RGB | undefined {
  const match = /^#?([0-9a-f]{6})$/i.exec(input);
  if (!match) return undefined;
  const value = match[1];
  return {
    r: parseInt(value.slice(0, 2), 16),
    g: parseInt(value.slice(2, 4), 16),
    b: parseInt(value.slice(4, 6), 16),
  };
}
