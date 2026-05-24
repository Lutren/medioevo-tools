import { describe, expect, it } from "vitest";
import { applyVermeerLightProfile, createVermeerLightProfile, scoreVermeerLight } from "../artDirection/vermeerLightProfile";
import { createDefaultIsoRendererConfig, createIsoSceneAdapter } from "../iso3d/isoSceneAdapter";
import { applyVermeerIsoLighting, scoreVermeerIsoLegibility } from "../iso3d/vermeerIsoLighting";
import { createCity } from "../sim/city";

describe("Vermeer lighting profile v1.3.2", () => {
  it("is finite, soft and side-lit", () => {
    const profile = createVermeerLightProfile();
    expect(profile.sideLight).toBeGreaterThan(0.5);
    expect(profile.windowSourceClarity).toBeGreaterThan(0.7);
    expect(profile.bloomDiscipline).toBeGreaterThan(0.7);
    const scene = applyVermeerLightProfile({ contrast: 0.8, shadowStrength: 0.8, materialReflection: 0.3, moodTags: [] });
    expect(scoreVermeerLight(scene)).toBeGreaterThan(0.5);
  });

  it("adds a soft window light to the Iso3D scene", () => {
    const city = createCity();
    const scene = createIsoSceneAdapter(city, {
      mode: "CITY",
      viewMode: "BEAUTIFUL",
      config: { ...createDefaultIsoRendererConfig("BEAUTIFUL"), enabled: true, mode: "iso3d" },
    });
    const vermeer = applyVermeerIsoLighting(scene);
    expect(vermeer.lights.some(light => light.kind === "window" && light.softness >= 0.58)).toBe(true);
    expect(Number.isFinite(scoreVermeerIsoLegibility(vermeer))).toBe(true);
  });
});
