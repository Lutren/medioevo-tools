import { createVermeerLightProfile } from "../artDirection/vermeerLightProfile";
import type { IsoLightSource, IsoScene } from "./isoTypes";

export function createVermeerIsoWindowLight(sceneId = "vermeer-window-main"): IsoLightSource {
  const profile = createVermeerLightProfile();
  return {
    id: sceneId,
    kind: "window",
    position: { x: -96, y: -120, z: 92 },
    color: { r: 255, g: 218, b: 168 },
    intensity: profile.windowSourceClarity * 0.7,
    radius: 260,
    softness: profile.sideLight,
  };
}

export function applyVermeerIsoLighting(scene: IsoScene): IsoScene {
  const windowLight = createVermeerIsoWindowLight();
  const lights = [
    windowLight,
    ...scene.lights.map(light => ({
      ...light,
      intensity: clamp(light.intensity * 0.9, 0.08, 1.2),
      softness: clamp(Math.max(light.softness, 0.58), 0, 1),
    })),
  ];
  return {
    ...scene,
    lightProfile: "vermeer",
    lights,
    billboards: scene.billboards.map(billboard => ({
      ...billboard,
      brightness: clamp(billboard.brightness * 0.92 + 0.12, 0.2, 1.35),
      metadata: { ...billboard.metadata, vermeerLight: true },
    })),
  };
}

export function scoreVermeerIsoLegibility(scene: IsoScene): number {
  const softLights = scene.lights.filter(light => light.kind === "window" && light.softness >= 0.58).length;
  const spriteLegibility = scene.billboards.reduce((sum, billboard) => sum + clamp(billboard.brightness, 0, 1.4), 0) / Math.max(1, scene.billboards.length);
  return Number(Math.min(1, softLights * 0.18 + spriteLegibility * 0.52 + scene.metrics.Phi_iso * 0.3).toFixed(3));
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, Number.isFinite(value) ? value : min));
}
