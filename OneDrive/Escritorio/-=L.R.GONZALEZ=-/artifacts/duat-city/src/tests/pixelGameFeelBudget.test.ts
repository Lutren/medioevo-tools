import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createAudioGameFeelSnapshot } from "../audio/gameFeelAdapter";
import { capAudioGameFeelSnapshot, computeGameFeelRenderBudget } from "../pixelRealism/gameFeelPerformance";

describe("pixel game-feel render budget v1.3.1", () => {
  it("caps cue and pulse budgets deterministically", () => {
    const snapshot = createAudioGameFeelSnapshot(createCity());
    const budget = computeGameFeelRenderBudget("LOW", snapshot);
    const capped = capAudioGameFeelSnapshot(snapshot, budget);
    expect(budget.dirtyOnly).toBe(true);
    expect(capped.cues.length).toBeLessThanOrEqual(budget.maxAudioCues);
    expect(Number.isFinite(capped.gameFeel.lightPulse)).toBe(true);
  });
});
