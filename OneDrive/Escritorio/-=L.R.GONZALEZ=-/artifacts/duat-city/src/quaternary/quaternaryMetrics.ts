import type { Gate } from "../core/types";
import type { QEvaluation, QState, QuaternarySystemMetrics } from "./types";

const clamp01 = (n: number) => Math.max(0, Math.min(1, Number.isFinite(n) ? n : 0));
const round = (n: number) => Math.round(n * 1000) / 1000;

const EMPTY_COUNTS: Record<QState, number> = { "00": 0, "01": 0, "10": 0, "11": 0 };

function avg(values: number[]): number {
  if (values.length === 0) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

export function computeQuaternarySystemMetrics(evaluations: QEvaluation[]): QuaternarySystemMetrics {
  const counts: Record<QState, number> = { ...EMPTY_COUNTS };
  for (const evaluation of evaluations) counts[evaluation.state]++;
  const total = evaluations.length;
  const anomalyRate = total > 0 ? counts["01"] / total : 0;
  const eventRate = total > 0 ? counts["11"] / total : 0;
  const stablePresenceRate = total > 0 ? counts["10"] / total : 0;
  const silenceRate = total > 0 ? counts["00"] / total : 0;
  const avgFrequency = avg(evaluations.map(e => e.timing.frequency));
  const avgPermanence = avg(evaluations.map(e => e.timing.permanence));
  const avgStability = avg(evaluations.map(e => e.timing.stability));
  const unstableEventRate = eventRate * (1 - avgStability);
  const R_quaternary = clamp01(
    0.40 * anomalyRate +
    0.25 * avgFrequency +
    0.20 * (1 - avgStability) +
    0.15 * unstableEventRate,
  );
  const Phi_quaternary = clamp01(
    0.45 * avgStability +
    0.25 * stablePresenceRate +
    0.20 * (1 - anomalyRate) +
    0.10 * (1 - avgFrequency),
  );
  const recommendedGate: Gate = R_quaternary > 0.60 ? "BLOCK" : R_quaternary > 0.35 ? "REVIEW" : "APPROVE";

  return {
    total,
    counts,
    anomalyRate: round(anomalyRate),
    eventRate: round(eventRate),
    stablePresenceRate: round(stablePresenceRate),
    silenceRate: round(silenceRate),
    avgFrequency: round(avgFrequency),
    avgPermanence: round(avgPermanence),
    avgStability: round(avgStability),
    R_quaternary: round(R_quaternary),
    Phi_quaternary: round(Phi_quaternary),
    recommendedGate,
  };
}

