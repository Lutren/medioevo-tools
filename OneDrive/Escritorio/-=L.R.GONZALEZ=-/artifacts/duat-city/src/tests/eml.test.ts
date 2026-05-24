import { describe, it, expect } from "vitest";
import { safeEml, emlForCity } from "../core/eml";

describe("safeEml", () => {
  it("uses the canonical bounded sigmoid EML form", () => {
    const r = safeEml(0, 0);
    expect(r.value).toBeCloseTo(0.5, 6);
    expect(r.direction).toBe("HOLD");
  });
  it("returns EXPAND for high values", () => {
    const r = safeEml(5, 1);
    expect(r.direction).toBe("EXPAND");
  });
  it("returns COMPRESS for low values", () => {
    const r = safeEml(-5, 100);
    expect(r.direction).toBe("COMPRESS");
  });
  it("value is finite", () => {
    const r = safeEml(100, 0.0001);
    expect(Number.isFinite(r.value)).toBe(true);
  });
  it("value is bounded", () => {
    const r = safeEml(20, 1);
    expect(r.value).toBeLessThanOrEqual(1);
    expect(r.value).toBeGreaterThanOrEqual(0);
  });
  it("penalizes complexity through log1p", () => {
    const simple = safeEml(1, 0);
    const complex = safeEml(1, 10);
    expect(simple.value).toBeGreaterThan(complex.value);
  });
});

describe("emlForCity", () => {
  it("returns HOLD for balanced state", () => {
    const r = emlForCity(0.7, 0.2);
    expect(["EXPAND", "HOLD", "COMPRESS"]).toContain(r.direction);
  });
  it("returns finite value", () => {
    const r = emlForCity(0, 1);
    expect(Number.isFinite(r.value)).toBe(true);
  });
});
