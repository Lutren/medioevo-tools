import { describe, expect, it } from "vitest";
import { generateCosmologyQuestHooks } from "../lore/cosmologyQuestHooks";
import { blockPublicCosmologyClaim, fireEventLoreMechanic } from "../lore/inWorldPhysics";
import { compileInWorldCosmology } from "../lore/medioevoCosmology";

describe("cosmology boundary v1.3", () => {
  it("marks in-world physics as lore/formal-lab and blocks public science claim", () => {
    const profile = compileInWorldCosmology();
    expect(profile.publicClaimAllowed).toBe(false);
    expect(profile.concepts[0].boundary).toContain("IN_WORLD_COSMOLOGY");
    expect(blockPublicCosmologyClaim("this is real physics").gate).toBe("BLOCK");
  });

  it("generates quest hooks and fire mechanic with boundary", () => {
    expect(generateCosmologyQuestHooks().length).toBeGreaterThan(0);
    expect(fireEventLoreMechanic().boundary).toContain("fictional");
  });
});
