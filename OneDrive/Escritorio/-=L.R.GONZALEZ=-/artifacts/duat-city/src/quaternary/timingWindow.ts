import type { QState, QTimingStats } from "./types";
import { qStateFromIndex, qStateToIndex } from "./qstate";

const clamp01 = (n: number) => Math.max(0, Math.min(1, Number.isFinite(n) ? n : 0));

export interface TimingWindow {
  push(state: QState, tick: number): void;
  getStats(): QTimingStats;
  reset(): void;
  transitionCount(): number;
  dwellTicks(): number;
  frequency(): number;
  period(): number | null;
  permanence(): number;
  stability(): number;
}

export function createTimingWindow(windowSize = 64): TimingWindow {
  const capacity = Math.max(2, Math.floor(Number.isFinite(windowSize) ? windowSize : 64));
  const states = new Array<number>(capacity);
  const ticks = new Array<number>(capacity);
  let cursor = 0;
  let length = 0;

  function orderedStates(): number[] {
    const out: number[] = [];
    for (let i = 0; i < length; i++) {
      const idx = (cursor - length + i + capacity) % capacity;
      out.push(states[idx] ?? 0);
    }
    return out;
  }

  function orderedTicks(): number[] {
    const out: number[] = [];
    for (let i = 0; i < length; i++) {
      const idx = (cursor - length + i + capacity) % capacity;
      out.push(ticks[idx] ?? 0);
    }
    return out;
  }

  function currentIndex(): number {
    if (length === 0) return 0;
    return states[(cursor - 1 + capacity) % capacity] ?? 0;
  }

  function previousIndex(): number {
    if (length < 2) return currentIndex();
    return states[(cursor - 2 + capacity) % capacity] ?? currentIndex();
  }

  const api: TimingWindow = {
    push(state: QState, tick: number): void {
      states[cursor] = qStateToIndex(state);
      ticks[cursor] = Number.isFinite(tick) ? tick : 0;
      cursor = (cursor + 1) % capacity;
      length = Math.min(capacity, length + 1);
    },

    getStats(): QTimingStats {
      const current = qStateFromIndex(currentIndex());
      const previous = qStateFromIndex(previousIndex());
      const transitions = api.transitionCount();
      const frequency = api.frequency();
      const period = api.period();
      const permanence = api.permanence();
      const stability = api.stability();
      const residue = clamp01(0.45 * frequency + (current === "01" ? 0.35 : 0) + 0.20 * (1 - stability));
      const confidence = clamp01(0.35 + 0.45 * stability + 0.20 * permanence - 0.25 * residue);
      return {
        current,
        previous,
        dwellTicks: api.dwellTicks(),
        transitions,
        frequency,
        period,
        permanence,
        stability,
        confidence,
        residue,
        windowSize: capacity,
      };
    },

    reset(): void {
      cursor = 0;
      length = 0;
      states.fill(0);
      ticks.fill(0);
    },

    transitionCount(): number {
      const values = orderedStates();
      let count = 0;
      for (let i = 1; i < values.length; i++) {
        if (values[i] !== values[i - 1]) count++;
      }
      return count;
    },

    dwellTicks(): number {
      if (length === 0) return 0;
      const values = orderedStates();
      const current = values[values.length - 1];
      let dwell = 0;
      for (let i = values.length - 1; i >= 0; i--) {
        if (values[i] !== current) break;
        dwell++;
      }
      return dwell;
    },

    frequency(): number {
      return clamp01(api.transitionCount() / Math.max(length - 1, 1));
    },

    period(): number | null {
      if (length < 2) return null;
      const values = orderedStates();
      const tickValues = orderedTicks();
      const current = values[values.length - 1];
      const currentTicks: number[] = [];
      for (let i = 0; i < values.length; i++) {
        if (values[i] === current) currentTicks.push(tickValues[i]);
      }
      if (currentTicks.length < 2) return null;
      let total = 0;
      let gaps = 0;
      for (let i = 1; i < currentTicks.length; i++) {
        const gap = currentTicks[i] - currentTicks[i - 1];
        if (Number.isFinite(gap) && gap > 0) {
          total += gap;
          gaps++;
        }
      }
      if (gaps === 0) return null;
      return total / gaps;
    },

    permanence(): number {
      return clamp01(api.dwellTicks() / capacity);
    },

    stability(): number {
      const period = api.period();
      const periodScore = period != null ? clamp01(period / capacity) : 0.5;
      return clamp01(0.45 * api.permanence() + 0.35 * (1 - api.frequency()) + 0.20 * periodScore);
    },
  };

  return api;
}

