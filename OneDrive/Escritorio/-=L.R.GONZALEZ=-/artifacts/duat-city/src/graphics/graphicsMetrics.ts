import { muK } from "../core/fibmob";
import type { Direction } from "../core/types";
import type { GraphicsBudget, GraphicsMetrics } from "./types";
import type { QuaternaryStateSummary } from "../quaternary/types";

const clamp01 = (n: number) => Math.max(0, Math.min(1, Number.isFinite(n) ? n : 0));

export function computeGraphicsBudget(
  R: number,
  Phi_eff: number,
  cameraZoom: number,
  physicsR: number,
  tick: number,
  quaternary?: QuaternaryStateSummary,
): GraphicsBudget {
  const mu = muK(Math.max(1, tick), 1);
  let direction: Direction = "HOLD";
  let reason = "balanced";

  if (quaternary && (quaternary.R > 0.60 || quaternary.avgFrequency > 0.45 || quaternary.gate === "BLOCK")) {
    direction = "COMPRESS";
    reason = quaternary.gate === "BLOCK" ? "quaternary gate BLOCK" : "quaternary timing unstable";
  } else if (R > 0.60 || physicsR > 0.60 || mu === 0) {
    direction = "COMPRESS";
    reason = R > 0.60 ? "global R high" : physicsR > 0.60 ? "physics R high" : "FibMob compressed tick";
  } else if (Phi_eff > 0.75 && R < 0.20 && (!quaternary || quaternary.gate === "APPROVE")) {
    direction = "EXPAND";
    reason = "low R and high Phi_eff";
  } else if (quaternary?.avgStability && quaternary.avgStability > 0.65 && quaternary.counts["10"] > quaternary.counts["11"]) {
    direction = "HOLD";
    reason = "quaternary stable presence supports cached LOD";
  }

  if (direction === "COMPRESS") {
    return {
      tileDetail: cameraZoom > 1.3 ? 1 : 0,
      agentDetail: 0,
      particlesEnabled: false,
      shadowsEnabled: false,
      heatmapEnabled: false,
      chunkMode: "DIRTY",
      direction,
      reason,
    };
  }

  if (direction === "EXPAND") {
    return {
      tileDetail: 2,
      agentDetail: 2,
      particlesEnabled: true,
      shadowsEnabled: true,
      heatmapEnabled: true,
      chunkMode: cameraZoom < 0.75 ? "DIRTY" : "FULL",
      direction,
      reason,
    };
  }

  return {
    tileDetail: cameraZoom >= 1.2 ? 2 : cameraZoom >= 0.8 ? 1 : 0,
    agentDetail: cameraZoom >= 1.0 ? 1 : 0,
    particlesEnabled: R <= 0.45,
    shadowsEnabled: false,
    heatmapEnabled: true,
    chunkMode: "DIRTY",
    direction,
    reason,
  };
}

export function estimateGraphicsMetrics(
  budget: GraphicsBudget,
  chunksRendered: number,
  dirtyChunks: number,
  particlesCount: number,
  quaternary?: QuaternaryStateSummary,
): GraphicsMetrics {
  const qPressure = quaternary ? quaternary.avgFrequency * 0.15 + quaternary.anomalyRate * 0.20 : 0;
  const pressure = clamp01((chunksRendered / 64) * 0.35 + (particlesCount / 300) * 0.45 + qPressure);
  const R_graphics = budget.direction === "COMPRESS" ? clamp01(pressure + 0.18) : pressure;
  const Phi_graphics = clamp01(1 - R_graphics + (budget.direction === "EXPAND" ? 0.08 : 0));
  return {
    direction: budget.direction,
    chunksRendered,
    dirtyChunks,
    particlesCount,
    renderBudget: `${budget.direction}:${budget.reason}`,
    R_graphics,
    Phi_graphics,
    quaternaryGate: quaternary?.gate,
  };
}
