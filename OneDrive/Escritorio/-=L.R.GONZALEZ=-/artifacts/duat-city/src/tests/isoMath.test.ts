import { describe, expect, it } from "vitest";
import { gridToScreen, screenToGrid, sortByDepth } from "../graphics/isoMath";

describe("isoMath", () => {
  it("roundtrips grid/screen approximately", () => {
    const cfg = { tileWidth: 32, tileHeight: 16, originX: 120, originY: 40 };
    const p = gridToScreen(7.25, 3.5, 2, cfg);
    const g = screenToGrid(p.x, p.y, 2, cfg);
    expect(g.x).toBeCloseTo(7.25, 5);
    expect(g.y).toBeCloseTo(3.5, 5);
  });

  it("sorts depth deterministically", () => {
    const sorted = sortByDepth([
      { id: "b", x: 1, y: 1 },
      { id: "a", x: 1, y: 1 },
      { id: "c", x: 0, y: 1 },
    ]);
    expect(sorted.map(d => d.id)).toEqual(["c", "a", "b"]);
  });
});
