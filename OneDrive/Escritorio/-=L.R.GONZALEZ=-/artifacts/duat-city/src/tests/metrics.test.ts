import { describe, it, expect } from "vitest";
import { computeRegime, computeGate, computePhiEff, computeNextAction } from "../core/metrics";

describe("computeRegime", () => {
  it("OPTIMO when R≤0.15 and Phi_eff≥0.75", () => {
    expect(computeRegime(0.1, 0.8)).toBe("OPTIMO");
  });
  it("FUNCIONAL when R≤0.30 and Phi_eff≥0.60", () => {
    expect(computeRegime(0.25, 0.65)).toBe("FUNCIONAL");
  });
  it("CARGADO when R≤0.60", () => {
    expect(computeRegime(0.5, 0.4)).toBe("CARGADO");
  });
  it("SATURADO when R>0.60", () => {
    expect(computeRegime(0.7, 0.3)).toBe("SATURADO");
  });
});

describe("computeGate", () => {
  it("APPROVE when R≤0.35", () => expect(computeGate(0.2)).toBe("APPROVE"));
  it("REVIEW when 0.35<R≤0.60", () => expect(computeGate(0.5)).toBe("REVIEW"));
  it("BLOCK when R>0.60", () => expect(computeGate(0.8)).toBe("BLOCK"));
});

describe("computePhiEff", () => {
  it("is between 0 and 1", () => {
    const v = computePhiEff(0.2, 0.7, 0.6);
    expect(v).toBeGreaterThanOrEqual(0);
    expect(v).toBeLessThanOrEqual(1);
  });
  it("decreases as R increases", () => {
    const low = computePhiEff(0.1, 0.7, 0.7);
    const high = computePhiEff(0.5, 0.7, 0.7);
    expect(low).toBeGreaterThan(high);
  });
});

describe("computeNextAction", () => {
  it("BLOCK gate → COMPRESS action", () => {
    const a = computeNextAction("BLOCK", "SATURADO");
    expect(a).toContain("COMPRESS");
  });
  it("APPROVE + OPTIMO → EXPAND action", () => {
    const a = computeNextAction("APPROVE", "OPTIMO");
    expect(a).toContain("EXPAND");
  });
});
