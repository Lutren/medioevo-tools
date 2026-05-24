import { describe, expect, it } from "vitest";
import { compileSceneMood } from "../artDirection/sceneMoodCompiler";
import { parseVibePrompt } from "../vibecoding/vibeParser";

describe("vibe art direction parsing v1.2", () => {
  it("parses mas Caravaggio", () => {
    const result = parseVibePrompt("mas Caravaggio en una ruina sagrada");
    expect(result.config.artDirection?.lightCanon).toBe("caravaggio_chiaroscuro");
    expect(result.config.artDirection?.narrativeLenses).toContain("mythic_archive_lens");
  });

  it("parses mas Vermeer and mas van Eyck", () => {
    expect(parseVibePrompt("mas Vermeer, interior de taberna").config.artDirection?.lightCanon).toBe("vermeer_interior_light");
    expect(parseVibePrompt("mas van Eyck, detalle material").config.artDirection?.lightCanon).toBe("van_eyck_detail_light");
  });

  it("parses surveillance archive absurd mythic prompts to MEDIOEVO original tokens", () => {
    const result = compileSceneMood("ciudad Orwell/Huxley, archivo mitico, absurdo kafkiano");
    expect(result.narrativeTokens).toContain("surveillance_control_language");
    expect(result.narrativeTokens).toContain("archive_symbol_memory");
    expect(result.narrativeTokens).toContain("recursive_gate_review");
    expect(result.publicBoundaryNote).toContain("Original MEDIOEVO");
  });
});
