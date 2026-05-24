import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { applyCameraPreset, centerOnSelectedAgent, centerOnSelectedBuilding, isFiniteCamera } from "../render/cameraPresets";

describe("visual polish regression v0.8", () => {
  it("OSIT operational preset can still show operational heatmap", () => {
    const preset = applyCameraPreset("OSIT", "OPERATIONAL", createCity(), { width: 1200, height: 800 });
    expect(preset.showHeatmap).toBe(true);
    expect(preset.showPhysicsDebug).toBe(false);
  });

  it("debug mode keeps pixel/FibMob/physics debug surface available", () => {
    const preset = applyCameraPreset("CITY", "DEBUG", createCity(), { width: 1200, height: 800 });
    expect(preset.showFibmob).toBe(true);
    expect(preset.showPhysicsDebug).toBe(true);
    expect(preset.showChunkDebug).toBe(true);
  });

  it("selected agent/building camera helpers preserve finite composition", () => {
    const city = createCity();
    expect(isFiniteCamera(centerOnSelectedAgent(city.agents[0], 1200, 800))).toBe(true);
    expect(isFiniteCamera(centerOnSelectedBuilding(city.buildings[0], 1200, 800))).toBe(true);
  });
});
