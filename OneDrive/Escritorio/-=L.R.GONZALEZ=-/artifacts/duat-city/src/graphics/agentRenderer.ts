import type { Agent } from "../core/types";
import type { ViewMode } from "./types";
import type { SpriteResolver } from "./spriteResolver";
import { AGENT_ROLE_COLORS, GATE_COLORS } from "../render/palette";
import { drawBlobShadow } from "./shadowEngine";
import { loadSprite } from "./spriteLoader";

export interface AgentRenderOptions {
  x: number;
  y: number;
  size: number;
  radius: number;
  selected: boolean;
  showLabel: boolean;
  spriteResolver?: SpriteResolver;
  viewMode?: ViewMode;
}

export function drawAgentSprite(ctx: CanvasRenderingContext2D, agent: Agent, opts: AgentRenderOptions): void {
  const cx = opts.x + opts.size / 2;
  const cy = opts.y + opts.size / 2;
  const color = AGENT_ROLE_COLORS[agent.role] ?? "#f4fbff";
  const beautiful = opts.viewMode === "BEAUTIFUL";
  drawBlobShadow(ctx, cx, cy + opts.radius * 0.85, opts.radius * 1.2, opts.radius * 0.38, beautiful ? 0.20 : 0.28);

  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy - opts.radius * 0.25, opts.radius, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.fillStyle = "rgba(244,251,255,0.22)";
  ctx.beginPath();
  ctx.arc(cx - opts.radius * 0.25, cy - opts.radius * 0.55, opts.radius * 0.28, 0, Math.PI * 2);
  ctx.fill();

  const sprite = opts.spriteResolver?.resolve(`agent/${agent.role}`);
  const img = sprite ? loadSprite(sprite) : undefined;
  if (img) {
    const iconSize = opts.radius * 1.45;
    ctx.drawImage(img, cx - iconSize / 2, cy - opts.radius * 0.25 - iconSize / 2, iconSize, iconSize);
  }

  const critical = criticalNeed(agent);
  if (critical) {
    ctx.fillStyle = "rgba(2,7,12,0.86)";
    ctx.fillRect(cx + opts.radius * 0.7, cy - opts.radius * 1.7, opts.radius * 1.3, opts.radius * 1.1);
    ctx.fillStyle = "#ffd166";
    ctx.font = `${Math.max(7, opts.radius * 1.2)}px monospace`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(critical, cx + opts.radius * 1.35, cy - opts.radius * 1.15);
  }

  if (agent.gate !== "APPROVE") {
    ctx.beginPath();
    ctx.arc(cx, cy - opts.radius * 0.25, opts.radius + 2, 0, Math.PI * 2);
    ctx.strokeStyle = GATE_COLORS[agent.gate];
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  if (opts.selected) {
    ctx.beginPath();
    ctx.arc(cx, cy - opts.radius * 0.25, opts.radius + 4, 0, Math.PI * 2);
    ctx.strokeStyle = "#f4fbff";
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  if (opts.showLabel) {
    ctx.fillStyle = "rgba(244,251,255,0.86)";
    ctx.font = `${Math.max(8, opts.radius * 1.35)}px monospace`;
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillText(agent.role.slice(0, 3), cx, cy - opts.radius - 3);
  }
  ctx.restore();
}

function criticalNeed(agent: Agent): string | undefined {
  const entries = Object.entries(agent.needs).sort((a, b) => a[1] - b[1]);
  const [key, value] = entries[0] ?? [];
  if (typeof value !== "number" || value >= 0.25) return undefined;
  return key.slice(0, 1).toUpperCase();
}
