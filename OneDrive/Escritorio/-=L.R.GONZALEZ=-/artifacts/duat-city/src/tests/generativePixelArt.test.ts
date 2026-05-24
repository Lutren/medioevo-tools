import { describe, expect, it } from "vitest";
import { pixelArtHash } from "../generative/pixelArtGenerator";
import { generateProceduralBuilding } from "../generative/proceduralBuildingGenerator";
import { generateProceduralTile } from "../generative/proceduralTileGenerator";
import { generateProceduralUi } from "../generative/proceduralUiGenerator";
import { composeGenerativeScene } from "../generative/generativeSceneComposer";

describe("generative pixel art v1.2", () => {
  it("tile, building and UI generation are deterministic", () => {
    expect(pixelArtHash(generateProceduralTile("wet_street", 42))).toBe(pixelArtHash(generateProceduralTile("wet_street", 42)));
    expect(pixelArtHash(generateProceduralBuilding("archive", 42))).toBe(pixelArtHash(generateProceduralBuilding("archive", 42)));
    expect(pixelArtHash(generateProceduralUi("terminal_frame", 42))).toBe(pixelArtHash(generateProceduralUi("terminal_frame", 42)));
  });

  it("output dimensions are valid", () => {
    const scene = composeGenerativeScene("underground_market", 7);
    expect(scene.elements.terminal_frame.width).toBeGreaterThan(0);
    expect(scene.elements.agent.height).toBeGreaterThan(0);
  });
});
