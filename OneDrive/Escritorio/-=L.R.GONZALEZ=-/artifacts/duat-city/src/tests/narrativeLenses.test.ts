import { describe, expect, it } from "vitest";
import { compileNarrativeLens, generateAgentConflict, generateQuestTone, generateSceneText, PUBLIC_BOUNDARY_NOTE } from "../artDirection/narrativeLenses";

describe("narrative lenses v1.2", () => {
  it("compile to safe internal tokens", () => {
    const lens = compileNarrativeLens({ R: 0.2, regime: "FUNCIONAL" }, "surveillance_dystopia_lens");
    expect(lens.internalToken).toBe("surveillance_control_language");
    expect(lens.publicBoundaryNote).toBe(PUBLIC_BOUNDARY_NOTE);
  });

  it("does not emit protected author/world/character labels", () => {
    const text = [
      generateQuestTone("perception_break_lens", { R: 0.5 }),
      generateAgentConflict("mythic_archive_lens", [{ name: "Archivist" }]),
      generateSceneText("absurd_trial_lens", "gatehouse"),
    ].join(" ");
    expect(text).not.toMatch(/orwell|huxley|borges|tolkien|kafka|pkd|vermeer|caravaggio/i);
  });

  it("generates quest tones", () => {
    expect(generateQuestTone("moral_conflict_lens", { R: 0.1 })).toContain("witness");
  });
});
