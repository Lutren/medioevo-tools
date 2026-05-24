import { describe, expect, it } from "vitest";
import { createTimingWindow } from "../quaternary";

describe("quaternary timing window", () => {
  it("increments dwell ticks for stable state", () => {
    const window = createTimingWindow(8);
    window.push("10", 1);
    window.push("10", 2);
    window.push("10", 3);
    expect(window.dwellTicks()).toBe(3);
    expect(window.getStats().current).toBe("10");
  });

  it("counts transitions and frequency", () => {
    const window = createTimingWindow(8);
    window.push("00", 1);
    window.push("11", 2);
    window.push("00", 3);
    expect(window.transitionCount()).toBe(2);
    expect(window.frequency()).toBe(1);
  });

  it("computes permanence and period without NaN", () => {
    const window = createTimingWindow(8);
    window.push("11", 1);
    window.push("10", 2);
    window.push("11", 5);
    window.push("11", 6);
    const stats = window.getStats();
    expect(stats.permanence).toBeGreaterThan(0);
    expect(stats.period).not.toBeNull();
    expect(JSON.stringify(stats)).not.toMatch(/NaN|Infinity/);
  });

  it("resets cleanly", () => {
    const window = createTimingWindow(8);
    window.push("01", 1);
    window.reset();
    expect(window.getStats().dwellTicks).toBe(0);
    expect(window.getStats().current).toBe("00");
  });
});

