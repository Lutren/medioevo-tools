import type { QEvaluation, QInput, QuaternaryGateOptions, QuaternarySystemMetrics } from "./types";
import type { TimingWindow } from "./timingWindow";
import { createTimingWindow } from "./timingWindow";
import { evaluateQuaternary } from "./quaternaryGate";
import { computeQuaternarySystemMetrics } from "./quaternaryMetrics";

export class QuaternarySensorBank {
  private readonly windows = new Map<string, TimingWindow>();
  private readonly recent: QEvaluation[] = [];

  constructor(private readonly options: QuaternaryGateOptions = {}) {}

  evaluate(input: QInput): QEvaluation {
    const sourceId = input.sourceId;
    let window = this.windows.get(sourceId);
    if (!window) {
      window = createTimingWindow(this.options.windowSize ?? 64);
      this.windows.set(sourceId, window);
    }
    const evaluation = evaluateQuaternary(input, window, this.options);
    this.recent.push(evaluation);
    if (this.recent.length > 240) this.recent.splice(0, this.recent.length - 240);
    return evaluation;
  }

  get(sourceId: string): TimingWindow | undefined {
    return this.windows.get(sourceId);
  }

  snapshot(): { evaluations: QEvaluation[]; metrics: QuaternarySystemMetrics } {
    const evaluations = this.recent.slice();
    return {
      evaluations,
      metrics: computeQuaternarySystemMetrics(evaluations),
    };
  }

  reset(sourceId?: string): void {
    if (sourceId) {
      this.windows.delete(sourceId);
      for (let i = this.recent.length - 1; i >= 0; i--) {
        if (this.recent[i].sourceId === sourceId) this.recent.splice(i, 1);
      }
      return;
    }
    this.windows.clear();
    this.recent.splice(0);
  }
}

