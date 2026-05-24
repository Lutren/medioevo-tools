import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { compileEpistemicStatement, computeLanguageMetrics, languageGate } from "../language/epistemicDialogue";
import { generateNpcUtterance } from "../language/npcSpeechEngine";
import { parseVibeCommandToGameAction } from "../language/vibeCommandLanguage";
import { compileSourceCardFromEvent } from "../language/sourceCardDialogue";

describe("language cortex v1.3", () => {
  it("classifies NPC utterance and computes finite metrics", () => {
    const city = createCity();
    const utterance = generateNpcUtterance(city.agents[0], city, "agent_sims");
    expect(["CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEO"]).toContain(utterance.classification);
    const metrics = computeLanguageMetrics([utterance]);
    expect(Number.isFinite(metrics.R_language)).toBe(true);
    expect(Number.isFinite(metrics.Phi_language)).toBe(true);
  });

  it("downgrades unsupported public claims and parses vibe commands", () => {
    const gated = languageGate(compileEpistemicStatement("This is real physics and scientifically proven", []));
    expect(gated.gate).toBe("BLOCK");
    const action = parseVibeCommandToGameAction("haz una calle lluviosa con neon y exporta escena RPG");
    expect(action.cloudUsed).toBe(false);
    expect(action.action).toBe("export_rpg");
  });

  it("compiles source cards from events", () => {
    const card = compileSourceCardFromEvent({
      id: "evt-test",
      tick: 1,
      type: "system",
      title: "Observed gate event",
      detail: "Local test evidence",
      R_delta: 0.1,
      gate: "APPROVE",
    });
    expect(card.schema).toBe("duat/source-card/v1.3");
    expect(card.evidence.length).toBeGreaterThan(0);
  });
});
