import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { applyCameraPreset, isFiniteCamera } from "../render/cameraPresets";

describe("Beautiful mode v0.8", () => {
  it("hides debug overlays while keeping a finite camera preset", () => {
    const preset = applyCameraPreset("CITY", "BEAUTIFUL", createCity(), { width: 1440, height: 900 });
    expect(isFiniteCamera(preset.camera)).toBe(true);
    expect(preset.showHeatmap).toBe(false);
    expect(preset.showFibmob).toBe(false);
    expect(preset.showPhysicsDebug).toBe(false);
    expect(preset.showChunkDebug).toBe(false);
  });

  it("keeps the city large enough for visual capture", () => {
    const preset = applyCameraPreset("CITY", "BEAUTIFUL", createCity(), { width: 1440, height: 900 });
    expect(preset.camera.zoom).toBeGreaterThanOrEqual(1);
  });
});
