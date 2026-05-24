import type { Gate } from "../core/types";

export function evaluatePrefrontalActionGate(input: { action: string; risk: number; external?: boolean; destructive?: boolean }): { gate: Gate; reason: string } {
  if (input.external || input.destructive || /push|deploy|cloud|real_apply|mcp/i.test(input.action)) {
    return { gate: "BLOCK", reason: "External/destructive/Wabi/MCP execution remains blocked." };
  }
  if (input.risk > 0.35) return { gate: "REVIEW", reason: "Risk above local automatic threshold." };
  return { gate: "APPROVE", reason: "Local reversible action within DUAT scope." };
}
