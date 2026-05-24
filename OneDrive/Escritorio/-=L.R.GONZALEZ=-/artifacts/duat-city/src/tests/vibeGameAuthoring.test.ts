import { describe, expect, it } from "vitest";
import { compileVibeAction } from "../vibecoding/vibeActionCompiler";
import { applyVibeGamePatch, undoVibeGamePatch } from "../vibecoding/vibeGameActions";
import { createDefaultPlayableSceneState } from "../scene/sceneState";

describe("vibe game authoring v1.2", () => {
  it("parses target scene commands and apply/undo works", () => {
    for (const prompt of [
      "haz un archivo prohibido con luz azul",
      "haz una forja central con fuego naranja",
      "haz un jardin bio-mecanico con agua y bioluminiscencia",
      "haz un mercado subterraneo con luces rosas y humo",
    ]) {
      const compiled = compileVibeAction(prompt);
      expect(compiled.cloudUsed).toBe(false);
      expect(compiled.externalApiUsed).toBe(false);
      expect(compiled.parsedIntent.length).toBeGreaterThan(0);
    }
    const scene = createDefaultPlayableSceneState();
    const action = compileVibeAction("haz una forja central con fuego naranja");
    const applied = applyVibeGamePatch(scene, action.scenePatch).scene;
    expect(applied.materials.some(cell => cell.material === "fire")).toBe(true);
    expect(undoVibeGamePatch(scene)).toBe(scene);
  });
});
