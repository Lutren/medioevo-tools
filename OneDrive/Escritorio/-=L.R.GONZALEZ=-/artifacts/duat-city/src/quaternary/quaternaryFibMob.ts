import { muK } from "../core/fibmob";
import type { QEvaluation } from "./types";

const clamp01 = (n: number) => Math.max(0, Math.min(1, Number.isFinite(n) ? n : 0));
const round = (n: number) => Math.round(n * 1000) / 1000;

function stableHash(input: string): number {
  let hash = 2166136261;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

export function qFibMobWeight(sourceId: string, tick: number, k = 1): number {
  const seed = stableHash(`${sourceId}:${Math.max(0, Math.floor(tick))}`);
  const n = Math.max(1, (seed % 97) + 1);
  return muK(n, k);
}

export function applyFibMobToQEvaluation(evaluation: QEvaluation, sourceId: string, tick: number, k = 1): QEvaluation {
  const mu = qFibMobWeight(sourceId, tick, k);
  let R_delta = evaluation.R_delta;
  let Phi_delta = evaluation.Phi_delta;
  let confidence = evaluation.confidence;
  let marker = "";

  if (mu === 0) {
    R_delta -= 0.01;
    Phi_delta += 0.005;
    confidence -= 0.03;
    marker = "FibMob compressed/reconstructive";
  } else if (mu > 0) {
    R_delta -= 0.01;
    Phi_delta += 0.015;
    confidence += 0.03;
    marker = "FibMob coherent";
  } else {
    R_delta += 0.015;
    Phi_delta -= 0.005;
    confidence -= 0.02;
    marker = "FibMob contrast";
  }

  return {
    ...evaluation,
    R_delta: round(R_delta),
    Phi_delta: round(Phi_delta),
    confidence: round(clamp01(confidence)),
    reason: `${evaluation.reason}; ${marker} mu=${mu}`.trim(),
  };
}

