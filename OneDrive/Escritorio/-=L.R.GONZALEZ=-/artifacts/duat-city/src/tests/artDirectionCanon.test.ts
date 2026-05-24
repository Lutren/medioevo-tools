import { describe, expect, it } from "vitest";
import { applyLightCanon, getLightCanonProfile, scoreLightDrama, scoreMaterialDetail } from "../artDirection/lightCanon";
import { listMaterialDetailProfiles } from "../artDirection/materialDetailCanon";

describe("art direction canon v1.2", () => {
  it("light profiles and material profiles are finite", () => {
    for (const name of ["balanced_medioevo", "caravaggio_chiaroscuro", "vermeer_interior_light", "van_eyck_detail_light"]) {
      const profile = getLightCanonProfile(name);
      expect(Number.isFinite(profile.contrast)).toBe(true);
      expect(profile.publicToken.length).toBeGreaterThan(0);
    }
    for (const material of listMaterialDetailProfiles()) {
      expect(material.baseColor).toMatch(/^#/);
      expect(Number.isFinite(material.reflectance)).toBe(true);
      expect(Number.isFinite(material.detailDensity)).toBe(true);
    }
  });

  it("Caravaggio profile increases contrast and drama", () => {
    const base = { contrast: 0.35, shadowStrength: 0.35, backgroundDarkness: 0.3 };
    const directed = applyLightCanon(base, "caravaggio_chiaroscuro");
    expect(directed.contrast).toBeGreaterThan(base.contrast);
    expect(scoreLightDrama(directed)).toBeGreaterThan(scoreLightDrama(base));
  });

  it("Vermeer softens interior light", () => {
    const directed = applyLightCanon({ contrast: 0.8, shadowStrength: 0.8, lightProfile: "" }, "vermeer_interior_light");
    expect(directed.shadowStrength).toBeLessThan(0.8);
    expect(directed.lightProfile).toBe("soft_interior_window_light");
  });

  it("van Eyck profile increases detail density", () => {
    const directed = applyLightCanon({ detailDensity: 0.2, materialReflection: 0.2 }, "van_eyck_detail_light");
    expect(scoreMaterialDetail(directed)).toBeGreaterThan(0.5);
  });
});
