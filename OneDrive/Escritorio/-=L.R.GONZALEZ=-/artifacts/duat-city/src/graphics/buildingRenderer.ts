import type { Building } from "../core/types";
import type { ViewMode } from "./types";
import type { SpriteResolver } from "./spriteResolver";
import { GATE_COLORS, TILE_COLORS, TILE_LABELS } from "../render/palette";
import { drawBlobShadow, shadowDirection } from "./shadowEngine";
import { loadSprite } from "./spriteLoader";

export interface BuildingRenderOptions {
  x: number;
  y: number;
  size: number;
  tick: number;
  selected: boolean;
  light: number;
  spriteResolver?: SpriteResolver;
  viewMode?: ViewMode;
}

export function drawBuilding(ctx: CanvasRenderingContext2D, building: Building, opts: BuildingRenderOptions): void {
  const { x, y, size } = opts;
  const beautiful = opts.viewMode === "BEAUTIFUL";
  const height = Math.max(5, size * ((beautiful ? 0.44 : 0.36) + building.level * 0.10));
  const base = TILE_COLORS[building.type] ?? "#444";
  const shadow = shadowDirection({ tick: opts.tick, height: building.level + 1 });
  drawBlobShadow(ctx, x + size / 2 + shadow.x * size, y + size * 0.72 + shadow.y * size, size * 0.42, size * 0.15, beautiful ? shadow.alpha * 0.82 : shadow.alpha * 0.62);

  ctx.save();
  const bx = x + size * 0.22;
  const by = y + size * 0.24;
  const bw = size * 0.56;
  const bh = size * (beautiful ? 0.50 : 0.46);

  ctx.fillStyle = shade(base, opts.light * 0.88);
  ctx.fillRect(bx, by, bw, bh);
  ctx.fillStyle = shade(base, opts.light * 1.14);
  ctx.beginPath();
  ctx.moveTo(bx, by);
  ctx.lineTo(bx + bw / 2, by - height * 0.45);
  ctx.lineTo(bx + bw, by);
  ctx.closePath();
  ctx.fill();

  ctx.strokeStyle = beautiful ? "rgba(244,251,255,0.28)" : GATE_COLORS[building.gate] ?? "rgba(255,255,255,0.35)";
  ctx.lineWidth = opts.selected ? 2 : 1;
  ctx.strokeRect(bx, by, bw, bh);

  if (size >= 12) {
    const sprite = opts.spriteResolver?.resolve(`building/${building.type}`);
    const img = sprite ? loadSprite(sprite) : undefined;
    if (img) {
      const iconSize = Math.max(8, size * 0.34);
      ctx.drawImage(img, x + size / 2 - iconSize / 2, y + size * 0.37 - iconSize / 2, iconSize, iconSize);
    } else {
      ctx.fillStyle = "rgba(244,251,255,0.82)";
      ctx.font = `${Math.max(7, size * 0.28)}px monospace`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(TILE_LABELS[building.type] ?? "", x + size / 2, y + size * 0.48);
    }
  }

  if (opts.selected) {
    ctx.strokeStyle = "#f4fbff";
    ctx.strokeRect(bx - 2, by - height * 0.45 - 2, bw + 4, bh + height * 0.45 + 4);
  }
  ctx.restore();
}

function shade(hex: string, light: number): string {
  const normalized = Math.max(0.2, Math.min(1.35, light));
  const n = Number.parseInt(hex.slice(1), 16);
  const r = Math.max(0, Math.min(255, Math.round(((n >> 16) & 255) * normalized)));
  const g = Math.max(0, Math.min(255, Math.round(((n >> 8) & 255) * normalized)));
  const b = Math.max(0, Math.min(255, Math.round((n & 255) * normalized)));
  return `rgb(${r},${g},${b})`;
}
