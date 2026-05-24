import { describe, expect, it } from "vitest";
import { createFpsSampler } from "../performance/fpsSampler";
import { defaultRenderCounters } from "../performance/performanceTypes";

describe("FPS sampler v0.8", () => {
  it("records frames and computes FPS percentiles without NaN", () => {
    const sampler = createFpsSampler({ sampleWindowSeconds: 5 });
    const counters = defaultRenderCounters("OPERATIONAL", 1.4);
    for (let i = 0; i < 8; i++) {
      sampler.beginFrame(i * 16);
      sampler.endFrame(i * 16 + 2, { ...counters, agentsRendered: 12, tilesRendered: 256 });
    }
    const snapshot = sampler.getSnapshot();
    expect(snapshot.totalFrames).toBe(8);
    expect(snapshot.avgFps).toBeGreaterThan(0);
    expect(snapshot.p95FrameMs).toBeGreaterThan(0);
    expect(snapshot.agentsRendered).toBe(12);
    for (const value of [snapshot.avgFps, snapshot.p50FrameMs, snapshot.p95FrameMs, snapshot.p99FrameMs]) {
      expect(Number.isFinite(value)).toBe(true);
    }
  });

  it("detects dropped and long frames", () => {
    const sampler = createFpsSampler();
    const counters = defaultRenderCounters();
    sampler.beginFrame(0);
    sampler.endFrame(0, counters);
    sampler.beginFrame(50);
    sampler.endFrame(52, counters);
    const snapshot = sampler.getSnapshot();
    expect(snapshot.droppedFrames).toBeGreaterThan(0);
    expect(snapshot.longFramesOver33ms).toBeGreaterThan(0);
  });

  it("reset clears accumulated values", () => {
    const sampler = createFpsSampler();
    sampler.beginFrame(0);
    sampler.endFrame(16, defaultRenderCounters());
    expect(sampler.getSnapshot().totalFrames).toBe(1);
    sampler.reset();
    const snapshot = sampler.getSnapshot();
    expect(snapshot.totalFrames).toBe(0);
    expect(snapshot.droppedFrames).toBe(0);
  });
});
