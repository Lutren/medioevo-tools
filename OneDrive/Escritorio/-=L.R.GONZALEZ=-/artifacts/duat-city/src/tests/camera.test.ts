import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import {
  applyCameraPreset,
  centerOnActiveDistrict,
  centerOnCity,
  fitCityToViewport,
  isFiniteCamera,
} from "../render/cameraPresets";

describe("camera framing v0.8", () => {
  it("fitCityToViewport and centers return finite camera values", () => {
    const city = createCity();
    for (const camera of [
      fitCityToViewport(city, 1024, 720, 64),
      centerOnCity(city, 1024, 720, 1),
      centerOnActiveDistrict(city, 1024, 720, 1.3),
    ]) {
      expect(isFiniteCamera(camera)).toBe(true);
      expect(camera.zoom).toBeGreaterThan(0);
    }
  });

  it("presets return finite zoom/x/y and Beautiful hides debug overlays", () => {
    const city = createCity();
    const viewport = { width: 1024, height: 720 };
    const beautiful = applyCameraPreset("CITY", "BEAUTIFUL", city, viewport);
    expect(isFiniteCamera(beautiful.camera)).toBe(true);
    expect(beautiful.showHeatmap).toBe(false);
    expect(beautiful.showFibmob).toBe(false);
    expect(beautiful.showPhysicsDebug).toBe(false);
    expect(beautiful.showChunkDebug).toBe(false);
  });

  it("debug preset enables technical overlays without NaN on resize-sized input", () => {
    const debug = applyCameraPreset("OSIT", "DEBUG", createCity(), { width: 1, height: 1 });
    expect(isFiniteCamera(debug.camera)).toBe(true);
    expect(debug.showHeatmap).toBe(true);
    expect(debug.showFibmob).toBe(true);
    expect(debug.showPhysicsDebug).toBe(true);
    expect(debug.showChunkDebug).toBe(true);
  });
});
