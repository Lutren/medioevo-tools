import { describe, expect, it } from "vitest";
import { createProceduralTonePlan } from "../audio/proceduralSynth";
import type { AudioCue } from "../audio/audioTypes";

const cue: AudioCue = {
  id: "test-fire",
  kind: "material_fire",
  source: "material",
  label: "test fire",
  frequencyHz: 92,
  durationMs: 180,
  gain: 0.2,
  pan: -0.2,
  priority: 0.8,
  tags: ["test"],
};

describe("procedural audio synth v1.3.1", () => {
  it("creates finite deterministic tone plans without samples", () => {
    const a = createProceduralTonePlan(cue, 131);
    const b = createProceduralTonePlan(cue, 131);
    expect(a).toEqual(b);
    expect(a.deterministic).toBe(true);
    expect([a.frequencyHz, a.durationMs, a.gain, a.pan, a.attackMs, a.decayMs, a.releaseMs, a.filterHz].every(Number.isFinite)).toBe(true);
    expect(a.frequencyHz).toBeGreaterThan(20);
  });

  it("clamps unsafe cue input into valid browser synthesis ranges", () => {
    const plan = createProceduralTonePlan({ ...cue, frequencyHz: Number.NaN, gain: 99, pan: 99 });
    expect(plan.frequencyHz).toBeGreaterThanOrEqual(20);
    expect(plan.gain).toBeLessThanOrEqual(1);
    expect(plan.pan).toBeLessThanOrEqual(1);
  });
});
