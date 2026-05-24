import type { QAction, QEvaluation, QInput, QuaternaryGateOptions } from "./types";
import type { TimingWindow } from "./timingWindow";
import { encodeQState, qStateMeaning } from "./qstate";
import { applyFibMobToQEvaluation } from "./quaternaryFibMob";

const clamp01 = (n: number) => Math.max(0, Math.min(1, Number.isFinite(n) ? n : 0));
const round = (n: number) => Math.round(n * 1000) / 1000;

const actionRank: Record<QAction, number> = {
  IGNORE: 0,
  COMPRESS: 1,
  HOLD: 2,
  EXPAND: 3,
  REVIEW: 4,
  BLOCK: 5,
};

function atLeast(action: QAction, minimum: QAction): QAction {
  return actionRank[action] >= actionRank[minimum] ? action : minimum;
}

export function evaluateQuaternary(
  input: QInput,
  timingWindow: TimingWindow,
  options: QuaternaryGateOptions = {},
): QEvaluation {
  const minDwellTicks = Math.max(1, options.minDwellTicks ?? 2);
  const anomalyWeight = Number.isFinite(options.anomalyWeight) ? options.anomalyWeight! : 1;
  const frequencyPenalty = Number.isFinite(options.frequencyPenalty) ? options.frequencyPenalty! : 0.05;

  const state = encodeQState(input.presence, input.difference);
  timingWindow.push(state, input.tick);
  const timing = timingWindow.getStats();
  const changed = timing.current !== timing.previous;

  let action: QAction = "HOLD";
  let R_delta = 0;
  let Phi_delta = 0;
  let confidence = timing.confidence;
  let reason = "";

  if (state === "00") {
    if (input.expected === true) {
      action = "REVIEW";
      R_delta = 0.04 * anomalyWeight;
      Phi_delta = -0.02;
      confidence = clamp01(confidence - 0.10);
      reason = "expected signal missing from silent channel";
    } else {
      action = "COMPRESS";
      R_delta = -0.01;
      Phi_delta = 0.01;
      reason = "stable silence can be cached or skipped";
    }
  } else if (state === "01") {
    action = "REVIEW";
    R_delta = 0.10 * anomalyWeight;
    Phi_delta = -0.05;
    confidence = clamp01(confidence - 0.18);
    reason = "expected signal missing or difference without presence";
  } else if (state === "10") {
    action = timing.permanence > 0.18 ? "COMPRESS" : "HOLD";
    R_delta = -0.02;
    Phi_delta = 0.03;
    confidence = clamp01(confidence + Math.min(0.18, timing.dwellTicks / Math.max(timing.windowSize, 1)));
    reason = "presence is stable and can use lower detail";
  } else {
    const evidence = input.rawValue !== undefined || input.previousValue !== undefined;
    const stableEvent = timing.stability >= 0.52 && timing.frequency <= 0.45;
    action = stableEvent ? "EXPAND" : "REVIEW";
    R_delta = stableEvent && evidence ? -0.03 : 0.06;
    Phi_delta = stableEvent ? 0.04 : -0.02;
    confidence = clamp01(confidence + (stableEvent ? 0.08 : -0.06));
    reason = stableEvent ? "active event with stable timing" : "active event is noisy or still settling";
  }

  if (timing.frequency > 0.45) {
    R_delta += frequencyPenalty;
    confidence = clamp01(confidence - timing.frequency * 0.18);
    action = atLeast(action, "REVIEW");
    reason += "; high Q frequency penalized";
  }

  if (changed && timing.dwellTicks < minDwellTicks) {
    if (action === "EXPAND") action = "HOLD";
    if (state === "01") action = "REVIEW";
    confidence = clamp01(confidence - 0.08);
    reason += "; hysteresis holding new state";
  }

  const evaluation: QEvaluation = {
    sourceId: input.sourceId,
    sourceKind: input.sourceKind,
    tick: input.tick,
    state,
    meaning: qStateMeaning(state),
    action,
    R_delta: round(R_delta),
    Phi_delta: round(Phi_delta),
    confidence: round(confidence),
    reason: reason.trim(),
    timing: {
      ...timing,
      confidence: round(confidence),
      residue: round(timing.residue),
      frequency: round(timing.frequency),
      permanence: round(timing.permanence),
      stability: round(timing.stability),
    },
  };

  return options.useFibMob ? applyFibMobToQEvaluation(evaluation, input.sourceId, input.tick, options.k ?? 1) : evaluation;
}

