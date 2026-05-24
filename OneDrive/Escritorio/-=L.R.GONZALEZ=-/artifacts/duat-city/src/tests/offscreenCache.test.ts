import { describe, expect, it } from "vitest";
import { composeLayers } from "../pixelRealism/layerCompositor";
import { createOffscreenLayerCache, getOrCreateLayer, invalidateLayer } from "../pixelRealism/offscreenLayerCache";
import { createPostprocessCache, getCachedPostprocess, invalidatePostprocess } from "../pixelRealism/postprocessCache";

describe("offscreen cache v1.2", () => {
  it("unchanged layer is reused and dirty material invalidates", () => {
    const cache = createOffscreenLayerCache<string>();
    expect(getOrCreateLayer(cache, "material:1", () => "a")).toBe("a");
    expect(getOrCreateLayer(cache, "material:1", () => "b")).toBe("a");
    invalidateLayer(cache, "material");
    expect(getOrCreateLayer(cache, "material:1", () => "b")).toBe("b");
  });

  it("weather invalidates atmosphere and compositor changes hash", () => {
    const cache = createPostprocessCache<string>();
    expect(getCachedPostprocess(cache, "atmosphere", { weather: "rain" }, () => "rain")).toBe("rain");
    invalidatePostprocess(cache, "atmosphere");
    expect(getCachedPostprocess(cache, "atmosphere", { weather: "fog" }, () => "fog")).toBe("fog");
    const a = composeLayers([{ id: "terrain", order: 0, visible: true, hash: "1" }]);
    const b = composeLayers([{ id: "terrain", order: 0, visible: true, hash: "2" }]);
    expect(a.compositeHash).not.toBe(b.compositeHash);
  });
});
