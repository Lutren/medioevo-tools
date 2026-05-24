import { describe, expect, it } from "vitest";
import { createTimingWindow, evaluateQuaternary, type QInput } from "../quaternary";

function input(presence: boolean, difference: boolean, tick: number, expected = false): QInput {
  return {
    sourceId: "system:test",
    sourceKind: "system",
    tick,
    presence,
    difference,
    expected,
    rawValue: presence ? 1 : 0,
  };
}

describe("quaternary gate", () => {
  it("compresses stable silence", () => {
    const win = createTimingWindow();
    const evaluation = evaluateQuaternary(input(false, false, 1), win);
    expect(evaluation.state).toBe("00");
    expect(evaluation.action).toBe("COMPRESS");
    expect(evaluation.R_delta).toBeLessThanOrEqual(0);
  });

  it("raises R for significant absence", () => {
    const win = createTimingWindow();
    const evaluation = evaluateQuaternary(input(false, true, 1, true), win);
    expect(evaluation.state).toBe("01");
    expect(evaluation.action).toBe("REVIEW");
    expect(evaluation.R_delta).toBeGreaterThan(0);
  });

  it("lowers R for stable presence", () => {
    const win = createTimingWindow();
    evaluateQuaternary(input(true, false, 1, true), win);
    const evaluation = evaluateQuaternary(input(true, false, 2, true), win);
    expect(evaluation.state).toBe("10");
    expect(evaluation.R_delta).toBeLessThan(0);
  });

  it("expands stable active event after dwell", () => {
    const win = createTimingWindow();
    evaluateQuaternary(input(true, true, 1, true), win);
    evaluateQuaternary(input(true, true, 2, true), win);
    const evaluation = evaluateQuaternary(input(true, true, 3, true), win);
    expect(evaluation.state).toBe("11");
    expect(["EXPAND", "REVIEW"]).toContain(evaluation.action);
  });

  it("penalizes high frequency and hysteresis prevents immediate expand", () => {
    const win = createTimingWindow(8);
    evaluateQuaternary(input(true, false, 1, true), win);
    evaluateQuaternary(input(true, true, 2, true), win);
    evaluateQuaternary(input(true, false, 3, true), win);
    const evaluation = evaluateQuaternary(input(true, true, 4, true), win, { minDwellTicks: 3 });
    expect(evaluation.action).not.toBe("EXPAND");
    expect(evaluation.R_delta).toBeGreaterThan(0);
  });
});

