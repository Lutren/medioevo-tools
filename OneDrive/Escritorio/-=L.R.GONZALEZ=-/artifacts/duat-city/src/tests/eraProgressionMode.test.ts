import { describe, expect, it } from "vitest";
import { compileEraConfig, listEras } from "../gameModes/eraProgressionMode";

describe("era progression mode v1.3", () => {
  it("registers eras and changes materials/language/audio config", () => {
    const eras = listEras(true);
    expect(eras.length).toBeGreaterThanOrEqual(10);
    const config = compileEraConfig("cyber_archeopunk", true);
    expect(config.changes.materials.length).toBeGreaterThan(0);
    expect(config.changes.language).toBe("signal");
    expect(config.changes.audio).toContain("neon");
    expect(config.boundary).toContain("fictional");
  });

  it("keeps secret era gated when not unlocked", () => {
    expect(listEras(false).some(era => era.id === "duat_epoch")).toBe(false);
  });
});
