import { describe, expect, it } from "vitest";
import { cameraChangeInvalidatesIsoLayers, createIsoDirtyRegion, mergeIsoDirtyRegions } from "../iso3d/isoDirtyRegions";
import { updateIsoLayerCache } from "../iso3d/isoLayerCache";
import { applyIsoSpriteBudget, getIsoPerformanceBudget } from "../iso3d/isoPerformanceBudget";
import { createCity } from "../sim/city";

describe("Iso3D performance budget v1.3.2", () => {
  it("keeps quality presets finite and reuses unchanged layers", () => {
    const debug = getIsoPerformanceBudget("DEBUG");
    const beautiful = getIsoPerformanceBudget("BEAUTIFUL");
    expect(debug.maxVisibleSprites).toBeGreaterThan(0);
    expect(beautiful.cacheStaticLayers).toBe(true);
    expect(applyIsoSpriteBudget([1, 2, 3], { ...debug, maxVisibleSprites: 2 })).toEqual([1, 2]);
    const city = createCity();
    const first = updateIsoLayerCache(undefined, city);
    const second = updateIsoLayerCache(first, city);
    expect(Number.isFinite(second.hitRatio)).toBe(true);
    expect(second.hitRatio).toBeGreaterThan(0.5);
  });

  it("marks dirty regions and camera invalidation deterministically", () => {
    const merged = mergeIsoDirtyRegions([
      createIsoDirtyRegion(1, 2, "material", ["terrain"]),
      createIsoDirtyRegion(1, 2, "light", ["lights"]),
    ]);
    expect(merged).toHaveLength(1);
    expect(merged[0].layers).toEqual(["terrain", "lights"]);
    expect(cameraChangeInvalidatesIsoLayers()).toContain("agents");
  });
});
