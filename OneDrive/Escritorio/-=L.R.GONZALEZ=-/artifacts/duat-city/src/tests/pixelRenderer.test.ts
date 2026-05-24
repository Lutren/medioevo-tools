import { describe, expect, it } from "vitest";
import { defaultPixelRealismConfig, normalizeQualityForView, PIXEL_RENDER_PASS_ORDER, QUALITY_SETTINGS } from "../pixelRealism/renderPasses";
import { createPixelRealismRuntime } from "../pixelRealism/pixelRealismMetrics";
import { createCity } from "../sim/city";

describe("pixel realism renderer v1.0", () => {
  it("keeps render passes ordered", () => {
    expect(PIXEL_RENDER_PASS_ORDER).toEqual([
      "world",
      "material",
      "light",
      "shadow",
      "reflection",
      "atmosphere",
      "bloom",
      "colorGrade",
      "dither",
      "pixelScale",
      "uiOverlay",
    ]);
  });

  it("quality presets are valid", () => {
    expect(QUALITY_SETTINGS.LOW.internalWidth).toBe(80);
    expect(QUALITY_SETTINGS.MEDIUM.internalWidth).toBe(160);
    expect(QUALITY_SETTINGS.HIGH.internalWidth).toBe(320);
  });

  it("Beautiful disables debug and Debug enables grids", () => {
    const beautiful = normalizeQualityForView(defaultPixelRealismConfig(), "BEAUTIFUL");
    const debug = normalizeQualityForView(defaultPixelRealismConfig(), "DEBUG");
    expect(beautiful.qualityPreset).toBe("BEAUTIFUL");
    expect(QUALITY_SETTINGS.BEAUTIFUL.debugGrids).toBe(false);
    expect(debug.qualityPreset).toBe("DEBUG");
    expect(QUALITY_SETTINGS.DEBUG.debugGrids).toBe(true);
  });

  it("computes finite runtime metrics", () => {
    const runtime = createPixelRealismRuntime(createCity(), defaultPixelRealismConfig());
    expect(runtime.metrics.finite).toBe(true);
    expect(runtime.metrics.activeLightCells).toBeGreaterThan(0);
  });
});
