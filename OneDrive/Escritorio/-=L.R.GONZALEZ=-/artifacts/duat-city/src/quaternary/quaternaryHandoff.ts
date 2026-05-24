import type { QEvaluation, QuaternaryHandoff, QuaternarySystemMetrics } from "./types";

function topBy(evaluations: QEvaluation[], score: (evaluation: QEvaluation) => number): string[] {
  return evaluations
    .slice()
    .sort((a, b) => score(b) - score(a))
    .slice(0, 5)
    .map(e => `${e.sourceId}:${e.state}:R${e.R_delta.toFixed(3)}:f${e.timing.frequency.toFixed(3)}`);
}

export function toQuaternaryHandoff(metrics: QuaternarySystemMetrics, recentEvaluations: QEvaluation[]): QuaternaryHandoff {
  const topAnomalies = topBy(
    recentEvaluations.filter(e => e.state === "01" || e.action === "REVIEW" || e.action === "BLOCK"),
    e => Math.max(0, e.R_delta) + e.timing.residue,
  );
  const topUnstable = topBy(
    recentEvaluations.filter(e => e.timing.frequency > 0.25 || e.timing.stability < 0.45),
    e => e.timing.frequency + (1 - e.timing.stability),
  );
  const next_action = metrics.recommendedGate === "BLOCK"
    ? "compress noisy channels and investigate missing signals"
    : metrics.recommendedGate === "REVIEW"
      ? "review top anomalies before expanding rendering or tasks"
      : "continue local simulation and use stable 10 channels for LOD compression";

  return {
    schema: "duat/quaternary-timing/v0.9",
    R_quaternary: metrics.R_quaternary,
    Phi_quaternary: metrics.Phi_quaternary,
    gate: metrics.recommendedGate,
    counts: metrics.counts,
    top_anomalies: topAnomalies,
    top_unstable: topUnstable,
    next_action,
  };
}

