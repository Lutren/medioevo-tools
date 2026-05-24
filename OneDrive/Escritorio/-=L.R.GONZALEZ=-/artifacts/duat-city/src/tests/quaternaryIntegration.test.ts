import { describe, expect, it } from "vitest";
import { generateHandoff } from "../core/handoff";
import { createCity } from "../sim/city";
import { tickEngine } from "../sim/engine";

describe("quaternary city integration", () => {
  it("city tick produces quaternary metrics without NaN", () => {
    const state = tickEngine(createCity());
    expect(state.quaternary).toBeDefined();
    expect(state.quaternary?.counts["00"]).toBeGreaterThanOrEqual(0);
    expect(JSON.stringify(state.quaternary)).not.toMatch(/NaN|Infinity/);
  });

  it("handoff includes quaternary timing", () => {
    const state = tickEngine(createCity());
    expect(generateHandoff(state).quaternary_timing).toBeDefined();
  });

  it("witnesslog does not spam every tick", () => {
    let state = createCity();
    for (let i = 0; i < 20; i++) state = tickEngine(state);
    const qEntries = state.witnesslog.filter(entry => entry.type === "quaternary_timing_gate");
    expect(qEntries.length).toBeLessThanOrEqual(2);
  });
});

