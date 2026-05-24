import { describe, expect, it } from "vitest";
import { runPlayableInteractionQaSequence } from "../scene/playableInteractionQa";
import { createCity } from "../sim/city";
import { getWabiMcpStatus } from "../wabi/mcpDesignBridge";

describe("playable interaction QA v1.1.1", () => {
  it("sequence places materials and erases one cell", () => {
    const result = runPlayableInteractionQaSequence(createCity());
    expect(result.checks.controlsWork).toBe(true);
    expect(result.sceneJson).toContain("water");
    expect(result.sceneJson).toContain("fire");
    expect(result.sceneJson).toContain("neon");
  });

  it("exports scene with materials lights and vibe config", () => {
    const result = runPlayableInteractionQaSequence(createCity());
    expect(result.checks.exportsContainMaterialsLightsVibe).toBe(true);
    expect(result.rpgSceneJson).toContain("visual_scene_profile");
    expect(result.rpgSceneJson).toContain("pixel_physics_profile");
  });

  it("remains finite and keeps Wabi flags false", () => {
    const result = runPlayableInteractionQaSequence(createCity());
    const handoff = getWabiMcpStatus();
    expect(result.checks.noNaN).toBe(true);
    expect(handoff.execution_allowed).toBe(false);
    expect(handoff.sandbox_execution_allowed).toBe(false);
    expect(handoff.real_apply_allowed).toBe(false);
  });
});
