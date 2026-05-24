import { defaultRenderCounters, type FpsSamplerOptions, type FpsSnapshot, type PerformanceRenderCounters } from "./performanceTypes";

interface FrameSample {
  at: number;
  frameMs: number;
}

export interface FpsSampler {
  beginFrame(now: number): void;
  endFrame(now: number, counters: PerformanceRenderCounters): void;
  getSnapshot(): FpsSnapshot;
  reset(): void;
}

export function createFpsSampler(options: FpsSamplerOptions = {}): FpsSampler {
  const sampleWindowSeconds = options.sampleWindowSeconds ?? 10;
  const targetFrameMs = options.targetFrameMs ?? 1000 / 60;
  let samples: FrameSample[] = [];
  let frameStart = 0;
  let lastFrameStart: number | undefined;
  let totalFrames = 0;
  let droppedFrames = 0;
  let longFramesOver16ms = 0;
  let longFramesOver33ms = 0;
  let currentFrameMs = 0;
  let lastCounters = defaultRenderCounters();
  let lastResetAt = Date.now();

  function prune(now: number): void {
    const minAt = now - sampleWindowSeconds * 1000;
    samples = samples.filter(sample => sample.at >= minAt);
  }

  function snapshot(): FpsSnapshot {
    const values = samples.map(sample => sample.frameMs).filter(value => Number.isFinite(value) && value > 0);
    const sorted = values.slice().sort((a, b) => a - b);
    const avgFrameMs = values.length > 0 ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
    const minFrameMs = sorted[0] ?? 0;
    const maxFrameMs = sorted[sorted.length - 1] ?? 0;
    return {
      ...lastCounters,
      currentFps: round(fpsFromFrameMs(currentFrameMs)),
      avgFps: round(fpsFromFrameMs(avgFrameMs)),
      minFps: round(fpsFromFrameMs(maxFrameMs)),
      maxFps: round(fpsFromFrameMs(minFrameMs)),
      frameMs: round(currentFrameMs),
      avgFrameMs: round(avgFrameMs),
      p50FrameMs: round(percentile(sorted, 0.50)),
      p95FrameMs: round(percentile(sorted, 0.95)),
      p99FrameMs: round(percentile(sorted, 0.99)),
      droppedFrames,
      longFramesOver16ms,
      longFramesOver33ms,
      sampleWindowSeconds,
      totalFrames,
      lastResetAt,
    };
  }

  return {
    beginFrame(now: number): void {
      frameStart = Number.isFinite(now) ? now : performance.now();
    },
    endFrame(now: number, counters: PerformanceRenderCounters): void {
      const frameEnd = Number.isFinite(now) ? now : performance.now();
      const interval = lastFrameStart === undefined ? frameEnd - frameStart : frameStart - lastFrameStart;
      const measured = interval > 0 ? interval : frameEnd - frameStart;
      currentFrameMs = Number.isFinite(measured) && measured > 0 ? measured : targetFrameMs;
      lastFrameStart = frameStart;
      totalFrames++;
      if (currentFrameMs > 16) longFramesOver16ms++;
      if (currentFrameMs > 33) longFramesOver33ms++;
      droppedFrames += Math.max(0, Math.floor(currentFrameMs / targetFrameMs) - 1);
      lastCounters = counters;
      samples.push({ at: frameEnd, frameMs: currentFrameMs });
      prune(frameEnd);
    },
    getSnapshot: snapshot,
    reset(): void {
      samples = [];
      frameStart = 0;
      lastFrameStart = undefined;
      totalFrames = 0;
      droppedFrames = 0;
      longFramesOver16ms = 0;
      longFramesOver33ms = 0;
      currentFrameMs = 0;
      lastCounters = defaultRenderCounters(lastCounters.viewMode, lastCounters.cameraZoom);
      lastResetAt = Date.now();
    },
  };
}

function fpsFromFrameMs(frameMs: number): number {
  if (!Number.isFinite(frameMs) || frameMs <= 0) return 0;
  return 1000 / frameMs;
}

function percentile(sorted: number[], ratio: number): number {
  if (sorted.length === 0) return 0;
  const index = Math.min(sorted.length - 1, Math.max(0, Math.ceil(sorted.length * ratio) - 1));
  return sorted[index] ?? 0;
}

function round(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.round(value * 100) / 100;
}
