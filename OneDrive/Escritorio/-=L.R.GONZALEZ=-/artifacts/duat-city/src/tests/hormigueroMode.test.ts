import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createHormigueroHeatmap, hormigueroAllowsDirectControl } from "../gameModes/hormigueroMode";

describe("hormiguero mode v1.3", () => {
  it("is observer-only and exposes finite agent/tile heatmap metrics", () => {
    const heatmap = createHormigueroHeatmap(createCity());
    expect(hormigueroAllowsDirectControl()).toBe(false);
    expect(heatmap.length).toBeGreaterThan(0);
    expect(heatmap.every(cell => Number.isFinite(cell.R) && Number.isFinite(cell.Phi_eff))).toBe(true);
  });
});
