import { describe, expect, it } from "vitest";
import { computeIsoDepth, createIsoGrid, createIsoWorldTile, gridToIsoWorld, isoWorldToGrid, sortIsoDepth } from "../iso3d/isoGrid";

describe("Iso3D grid v1.3.2", () => {
  it("roundtrips grid/world coordinates and depth sorts deterministically", () => {
    const grid = createIsoGrid(24, 18);
    const world = gridToIsoWorld({ x: 6, y: 4 }, grid, 1);
    const back = isoWorldToGrid(world, grid);
    expect(back.x).toBeCloseTo(6);
    expect(back.y).toBeCloseTo(4);
    expect(Number.isFinite(computeIsoDepth(world))).toBe(true);
    const a = createIsoWorldTile({ id: "b", grid: { x: 1, y: 2 }, type: "road", elevation: 0, R: 0, Phi_eff: 1 }, grid);
    const b = createIsoWorldTile({ id: "a", grid: { x: 1, y: 2 }, type: "road", elevation: 0, R: 0, Phi_eff: 1 }, grid);
    expect(sortIsoDepth([a, b]).map(item => item.id)).toEqual(["a", "b"]);
  });
});
