import { describe, expect, it } from "vitest";
import { compileVibeScene, vibeToPixelRealismConfig } from "../vibecoding/vibeSceneCompiler";

describe("VibeCoding deterministic parser v1.0", () => {
  it("maps neon rain prompts to rain/night/neon", () => {
    const result = compileVibeScene("calle lluviosa de noche con neon cian y charcos", "prompt");
    expect(result.cloudUsed).toBe(false);
    expect(result.externalApiUsed).toBe(false);
    expect(result.config.weather).toBe("rain");
    expect(result.config.timeOfDay).toBe("night");
    expect(result.config.lightProfile).toContain("neon");
  });

  it("maps warm interior prompts to warm palette/interior", () => {
    const result = compileVibeScene("interior calido de taberna con fuego", "prompt");
    expect(result.config.timeOfDay).toBe("interior");
    expect(result.config.palette).toBe("warm_interior");
    expect(result.config.materials).toContain("fire");
  });

  it("ignores unknown and API-like words safely", () => {
    const result = compileVibeScene("xqz cloud api token nonsense", "prompt");
    expect(result.cloudUsed).toBe(false);
    expect(result.externalApiUsed).toBe(false);
    expect(result.warnings.join(" ")).toContain("External/API");
  });

  it("compiles scene to pixel config", () => {
    const result = compileVibeScene("neon rain street", "prompt");
    const config = vibeToPixelRealismConfig(result.config);
    expect(config.weather).toBe("rain");
    expect(config.vibePreset).toBe(result.config.id);
  });
});
