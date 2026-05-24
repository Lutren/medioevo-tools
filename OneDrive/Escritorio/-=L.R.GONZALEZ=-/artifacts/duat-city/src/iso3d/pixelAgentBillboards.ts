import type { Agent } from "../core/types";
import { createPixelBillboard, orientBillboardToCamera } from "./isoBillboard";
import { gridToIsoWorld } from "./isoGrid";
import type { IsoBillboard, IsoCamera, IsoGridConfig, IsoLightSource } from "./isoTypes";
import { DEFAULT_PIXEL_BILLBOARD_PALETTE } from "./pixelBillboardTypes";

export function createAgentBillboards(agents: Agent[], grid: IsoGridConfig, camera: IsoCamera, lights: IsoLightSource[], selectedAgentId?: string): IsoBillboard[] {
  return agents.map(agent => {
    const position = gridToIsoWorld({ x: agent.x, y: agent.y }, grid, 0.34);
    const tint = agent.gate === "BLOCK" ? "#ff6c6c" : agent.gate === "REVIEW" ? "#e6c95b" : DEFAULT_PIXEL_BILLBOARD_PALETTE.agent;
    return orientBillboardToCamera(createPixelBillboard({
      id: `agent-${agent.id}`,
      kind: "agent",
      label: agent.name,
      position,
      tint,
      width: 14,
      height: 24,
      selected: selectedAgentId === agent.id,
      spriteKey: `procedural:agent:${agent.role}`,
      metadata: { role: agent.role, R: agent.R, Phi_eff: agent.Phi_eff, mood: agent.mood },
    }, lights), camera);
  });
}
