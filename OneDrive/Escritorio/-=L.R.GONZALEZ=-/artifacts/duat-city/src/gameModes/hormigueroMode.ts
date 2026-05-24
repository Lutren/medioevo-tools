import type { CityState } from "../core/types";
import type { HeatmapMetric } from "./gameModeTypes";

export function createHormigueroHeatmap(state: CityState): HeatmapMetric[] {
  const tileMetrics = state.tiles
    .filter(tile => tile.type !== "empty")
    .slice(0, 220)
    .map(tile => ({
      id: `tile:${tile.id}`,
      x: tile.x,
      y: tile.y,
      R: finite(tile.R),
      Phi_eff: finite(tile.Phi_eff),
      qState: tile.R > 0.55 ? "01" as const : tile.Phi_eff > 0.75 ? "10" as const : "00" as const,
    }));
  const agentMetrics = state.agents.slice(0, 80).map(agent => ({
    id: `agent:${agent.id}`,
    x: Math.round(agent.x),
    y: Math.round(agent.y),
    R: finite(agent.R),
    Phi_eff: finite(agent.Phi_eff),
    qState: agent.gate === "BLOCK" ? "01" as const : agent.gate === "REVIEW" ? "11" as const : "10" as const,
  }));
  return [...tileMetrics, ...agentMetrics];
}

export function hormigueroAllowsDirectControl(): false {
  return false;
}

function finite(value: number): number {
  return Number.isFinite(value) ? Number(value.toFixed(3)) : 0;
}
