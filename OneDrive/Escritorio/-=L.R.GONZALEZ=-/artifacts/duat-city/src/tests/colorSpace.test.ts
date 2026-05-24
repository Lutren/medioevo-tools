import { describe, expect, it } from "vitest";
import { hslToRgb, hsvToRgb, rgbToHsl, rgbToHsv, rgbToOKLab, okLabToRgb } from "../color/colorSpace";
import { kelvinToRgb } from "../color/temperature";
import { generatePalette, PALETTE_PROFILES } from "../color/paletteEngine";
import { toneMapRgb } from "../color/toneMapping";

describe("color theory engine v1.0", () => {
  it("keeps color conversions finite and roundtrips acceptably", () => {
    const rgb = { r: 92, g: 188, b: 210 };
    const hslRound = hslToRgb(rgbToHsl(rgb));
    const hsvRound = hsvToRgb(rgbToHsv(rgb));
    const labRound = okLabToRgb(rgbToOKLab(rgb));
    for (const color of [hslRound, hsvRound, labRound]) {
      expect(Number.isFinite(color.r)).toBe(true);
      expect(Number.isFinite(color.g)).toBe(true);
      expect(Number.isFinite(color.b)).toBe(true);
      expect(Math.abs(color.r - rgb.r)).toBeLessThan(6);
      expect(Math.abs(color.g - rgb.g)).toBeLessThan(6);
      expect(Math.abs(color.b - rgb.b)).toBeLessThan(6);
    }
  });

  it("kelvin colors map warm and cold sensibly", () => {
    const warm = kelvinToRgb(1800);
    const cold = kelvinToRgb(9000);
    expect(warm.r).toBeGreaterThan(warm.b);
    expect(cold.b).toBeGreaterThanOrEqual(cold.r);
  });

  it("palettes generate valid colors", () => {
    const generated = generatePalette({ r: 180, g: 120, b: 60 }, "triadic");
    for (const profile of [...Object.values(PALETTE_PROFILES), generated]) {
      expect(profile.colors.length).toBeGreaterThan(0);
      for (const color of profile.colors) {
        expect(color.r).toBeGreaterThanOrEqual(0);
        expect(color.r).toBeLessThanOrEqual(255);
        expect(color.g).toBeGreaterThanOrEqual(0);
        expect(color.g).toBeLessThanOrEqual(255);
        expect(color.b).toBeGreaterThanOrEqual(0);
        expect(color.b).toBeLessThanOrEqual(255);
      }
    }
  });

  it("tone mapping clamps output", () => {
    const mapped = toneMapRgb({ r: 999, g: -20, b: 120 }, { exposure: 1.4, contrast: 1.2 });
    expect(mapped.r).toBeLessThanOrEqual(255);
    expect(mapped.g).toBeGreaterThanOrEqual(0);
    expect(mapped.b).toBeGreaterThanOrEqual(0);
  });
});
