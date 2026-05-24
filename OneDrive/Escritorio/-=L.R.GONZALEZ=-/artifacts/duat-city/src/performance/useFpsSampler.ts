import { useCallback, useEffect, useRef, useState } from "react";
import { createFpsSampler } from "./fpsSampler";
import type { FpsSnapshot, PerformanceRenderCounters } from "./performanceTypes";

export function useFpsSampler(enabled: boolean) {
  const samplerRef = useRef(createFpsSampler());
  const [snapshot, setSnapshot] = useState<FpsSnapshot>(() => samplerRef.current.getSnapshot());

  const beginFrame = useCallback((now: number) => {
    if (!enabled) return;
    samplerRef.current.beginFrame(now);
  }, [enabled]);

  const endFrame = useCallback((now: number, counters: PerformanceRenderCounters) => {
    if (!enabled) return;
    samplerRef.current.endFrame(now, counters);
  }, [enabled]);

  const reset = useCallback(() => {
    samplerRef.current.reset();
    setSnapshot(samplerRef.current.getSnapshot());
  }, []);

  const getSnapshot = useCallback(() => samplerRef.current.getSnapshot(), []);

  useEffect(() => {
    if (!enabled) return;
    const id = window.setInterval(() => {
      setSnapshot(samplerRef.current.getSnapshot());
    }, 250);
    return () => window.clearInterval(id);
  }, [enabled]);

  return {
    beginFrame,
    endFrame,
    reset,
    snapshot,
    getSnapshot,
  };
}
