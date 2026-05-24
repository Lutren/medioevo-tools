import { describe, expect, it } from "vitest";
import { computeGraphicsBudget } from "../graphics/graphicsMetrics";
import { computeLODV2 } from "../render/lod-controller-v2";

const camera = { x: 0, y: 0, zoom: 1 };

describe("graphics budget and LOD v2", () => {
  it("high R compresses", () => {
    expect(computeGraphicsBudget(0.7, 0.4, 1, 0.1, 5).direction).toBe("COMPRESS");
  });

  it("low R high Phi expands", () => {
    expect(computeGraphicsBudget(0.1, 0.9, 1, 0.1, 5).direction).toBe("EXPAND");
  });

  it("compressed FibMob tick compresses", () => {
    expect(computeGraphicsBudget(0.1, 0.9, 1, 0.1, 8).direction).toBe("COMPRESS");
  });

  it("same input is deterministic", () => {
    const a = computeLODV2({ camera, R: 0.2, Phi_eff: 0.7, tick: 13 });
    const b = computeLODV2({ camera, R: 0.2, Phi_eff: 0.7, tick: 13 });
    expect(b).toEqual(a);
  });
});
