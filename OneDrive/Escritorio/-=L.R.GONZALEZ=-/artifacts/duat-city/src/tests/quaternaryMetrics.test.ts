import { describe, expect, it } from "vitest";
import { computeQuaternarySystemMetrics, type QEvaluation } from "../quaternary";

function evaluation(state: QEvaluation["state"], frequency = 0.1, stability = 0.7): QEvaluation {
  return {
    sourceId: `s:${state}:${frequency}`,
    sourceKind: "system",
    tick: 1,
    state,
    meaning: state === "01" ? "ABSENCE_SIGNIFICANT" : state === "11" ? "EVENT_ACTIVE" : state === "10" ? "PRESENCE_STABLE" : "SILENCE_STABLE",
    action: state === "01" ? "REVIEW" : "HOLD",
    R_delta: state === "01" ? 0.1 : 0,
    Phi_delta: 0,
    confidence: 0.7,
    reason: "test",
    timing: {
      current: state,
      previous: state,
      dwellTicks: 2,
      transitions: 1,
      frequency,
      period: null,
      permanence: 0.2,
      stability,
      confidence: 0.7,
      residue: 0.1,
      windowSize: 8,
    },
  };
}

describe("quaternary system metrics", () => {
  it("counts states", () => {
    const metrics = computeQuaternarySystemMetrics([evaluation("00"), evaluation("01"), evaluation("10"), evaluation("11")]);
    expect(metrics.counts).toEqual({ "00": 1, "01": 1, "10": 1, "11": 1 });
  });

  it("R increases with anomalies and frequency", () => {
    const stable = computeQuaternarySystemMetrics([evaluation("10", 0.05, 0.9), evaluation("10", 0.05, 0.9)]);
    const noisy = computeQuaternarySystemMetrics([evaluation("01", 0.8, 0.2), evaluation("11", 0.9, 0.2)]);
    expect(noisy.R_quaternary).toBeGreaterThan(stable.R_quaternary);
  });

  it("Phi increases with stability", () => {
    const stable = computeQuaternarySystemMetrics([evaluation("10", 0.05, 0.9), evaluation("00", 0.05, 0.9)]);
    const unstable = computeQuaternarySystemMetrics([evaluation("01", 0.8, 0.2), evaluation("11", 0.8, 0.2)]);
    expect(stable.Phi_quaternary).toBeGreaterThan(unstable.Phi_quaternary);
  });

  it("computes gate", () => {
    const metrics = computeQuaternarySystemMetrics([evaluation("01", 1, 0), evaluation("01", 1, 0)]);
    expect(["APPROVE", "REVIEW", "BLOCK"]).toContain(metrics.recommendedGate);
  });
});

