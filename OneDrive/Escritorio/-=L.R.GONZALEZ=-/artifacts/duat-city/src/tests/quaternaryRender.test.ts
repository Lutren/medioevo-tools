import { describe, expect, it } from "vitest";
import { computeGraphicsBudget } from "../graphics/graphicsMetrics";

describe("quaternary render integration", () => {
  it("render budget compresses when quaternary gate blocks", () => {
    const budget = computeGraphicsBudget(0.1, 0.9, 1, 0, 5, {
      R: 0.7,
      Phi_eff: 0.2,
      gate: "BLOCK",
      counts: { "00": 0, "01": 8, "10": 0, "11": 8 },
      avgFrequency: 0.7,
      avgPermanence: 0.1,
      avgStability: 0.2,
      anomalyRate: 0.5,
      eventRate: 0.5,
      R_delta: 0.1,
      Phi_delta: -0.1,
      combinedR: 0.4,
      combinedPhi: 0.5,
      topAnomalies: [],
      topUnstable: [],
      recent: [],
      next_action: "review",
    });
    expect(budget.direction).toBe("COMPRESS");
  });

  it("beautiful mode policy is kept outside Q overlay by app contract", () => {
    const budget = computeGraphicsBudget(0.1, 0.9, 1, 0, 5);
    expect(budget.direction).toBe("EXPAND");
  });
});

