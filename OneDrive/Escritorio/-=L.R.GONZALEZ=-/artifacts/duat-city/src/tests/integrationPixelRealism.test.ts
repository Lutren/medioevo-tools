import { describe, expect, it } from "vitest";
import { generateHandoff } from "../core/handoff";
import { createPixelRealismRuntime } from "../pixelRealism/pixelRealismMetrics";
import { defaultPixelRealismConfig } from "../pixelRealism/renderPasses";
import { createCity } from "../sim/city";
import { tickEngine } from "../sim/engine";

describe("Pixel realism integration v1.0", () => {
  it("OSIT handoff includes pixel_realism metrics", () => {
    const state = tickEngine(createCity());
    const runtime = createPixelRealismRuntime(state, defaultPixelRealismConfig("DEBUG"));
    const handoff = generateHandoff({ ...state, pixelRealism: runtime.metrics });
    expect(handoff.pixel_realism).toBeDefined();
    expect(Number.isNaN(handoff.pixel_realism?.R_light)).toBe(false);
    expect(Number.isNaN(handoff.pixel_realism?.Phi_light)).toBe(false);
    expect(handoff.pixel_realism?.qStateCounts).toBeDefined();
  });

  it("does not break existing simulation tick", () => {
    const next = tickEngine(createCity());
    const runtime = createPixelRealismRuntime(next, defaultPixelRealismConfig());
    expect(next.tick).toBe(1);
    expect(runtime.metrics.finite).toBe(true);
  });
});
