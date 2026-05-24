import { describe, expect, it } from "vitest";
import { defaultPixelRealismConfig } from "../pixelRealism/renderPasses";
import { createDefaultPlayableSceneState } from "../scene/sceneState";
import { compileVibeScene } from "../vibecoding/vibeSceneCompiler";
import { createVibeUndoSnapshot, restoreVibeUndoSnapshot } from "../vibecoding/vibeHistory";

describe("VibeCoding usability v1.1", () => {
  it("maps night rain neon wording", () => {
    const result = compileVibeScene("hazlo de noche con lluvia y neon", "prompt");
    expect(result.config.timeOfDay).toBe("night");
    expect(result.config.weather).toBe("rain");
    expect(result.config.lightProfile).toContain("neon");
    expect(result.parsedIntent).toContain("weather:rain");
  });

  it("maps warm tavern wording", () => {
    const result = compileVibeScene("mas calido, interior de taberna", "prompt");
    expect(result.config.timeOfDay).toBe("interior");
    expect(result.config.palette).toBe("warm_interior");
  });

  it("maps fog reflection water wording", () => {
    const result = compileVibeScene("mas niebla y reflejos en agua", "prompt");
    expect(result.config.fog).toBeGreaterThan(0.2);
    expect(result.config.materials).toContain("water");
    expect(result.parsedIntent).toContain("material:water_reflection");
  });

  it("maps archeopunk sunset wording", () => {
    const result = compileVibeScene("ciudad archeopunk al atardecer", "prompt");
    expect(result.config.id).toBe("archeopunk_city_night");
    expect(result.config.timeOfDay).toBe("golden");
    expect(result.config.palette).toBe("medioevo_archeopunk");
  });

  it("undo snapshot restores previous vibe state", () => {
    const scene = createDefaultPlayableSceneState();
    const config = defaultPixelRealismConfig();
    const previous = compileVibeScene("warm_interior_tavern", "preset").config;
    const snapshot = createVibeUndoSnapshot(previous, config, scene);
    const restored = restoreVibeUndoSnapshot(snapshot);
    expect(restored.activeVibeScene?.id).toBe("warm_interior_tavern");
    expect(restored.visualConfig.qualityPreset).toBe(config.qualityPreset);
    expect(restored.playableScene.schema).toBe("duat/playable-scene/v1.1");
  });
});
