import { describe, expect, it } from "vitest";
import {
  consumeDirtyRegions,
  createDirtyRegionState,
  dirtyRegionCount,
  markCameraDirty,
  markCellDirty,
  shouldSkipStableRegion,
} from "../pixelRealism/dirtyRegions";

describe("dirty regions v1.1.1", () => {
  it("changed cell marks a region dirty", () => {
    const regions = markCellDirty(createDirtyRegionState(80, 45, 10), 12, 18);
    expect(dirtyRegionCount(regions)).toBe(1);
    expect(shouldSkipStableRegion(regions, 1, 1)).toBe(false);
  });

  it("stable region is skipped", () => {
    const regions = markCellDirty(createDirtyRegionState(80, 45, 10), 12, 18);
    expect(shouldSkipStableRegion(regions, 7, 4)).toBe(true);
  });

  it("camera change marks visible regions dirty", () => {
    const regions = markCameraDirty(createDirtyRegionState(32, 16, 8), "x0-y0-z1");
    expect(dirtyRegionCount(regions)).toBe(8);
    expect(consumeDirtyRegions(regions)).toHaveLength(8);
    expect(dirtyRegionCount(regions)).toBe(0);
  });

  it("handles non-finite cells safely", () => {
    const regions = markCellDirty(createDirtyRegionState(80, 45, 10), Number.NaN, 2);
    expect(dirtyRegionCount(regions)).toBe(0);
  });
});
