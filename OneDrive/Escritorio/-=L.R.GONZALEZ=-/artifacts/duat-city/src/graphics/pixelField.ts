import type { PhysicsFieldSummary } from "../physicsField/pixelTypes";

export function fieldSummaryToOverlay(summary?: PhysicsFieldSummary): { color: string; alpha: number; label: string } {
  if (!summary) return { color: "rgba(36,232,255,0)", alpha: 0, label: "field:none" };
  if (summary.hazards.includes("fire")) return { color: "rgba(255,68,68,0.18)", alpha: 0.18, label: "field:fire" };
  if (summary.hazards.includes("flooding")) return { color: "rgba(116,220,255,0.14)", alpha: 0.14, label: "field:water" };
  if (summary.R_field > 0.45) return { color: "rgba(255,209,102,0.12)", alpha: 0.12, label: "field:loaded" };
  return { color: "rgba(36,232,255,0.05)", alpha: 0.05, label: "field:stable" };
}
