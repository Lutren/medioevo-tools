import type { Tile } from "../core/types";
import { TILE_BORDER_COLORS, TILE_COLORS, heatmapColor } from "../render/palette";

export interface TileRenderOptions {
  x: number;
  y: number;
  size: number;
  showHeatmap: boolean;
  showFibmob: boolean;
  light: number;
}

export function drawIsoTile(ctx: CanvasRenderingContext2D, tile: Tile, opts: TileRenderOptions): void {
  const { x, y, size } = opts;
  const h = size * 0.5;
  const cx = x + size / 2;
  const cy = y + size / 2;
  const color = shade(TILE_COLORS[tile.type] ?? "#1a1f2e", opts.light);
  const border = TILE_BORDER_COLORS[tile.type] ?? "#252b3a";

  ctx.save();
  ctx.beginPath();
  ctx.moveTo(cx, cy - h * 0.44);
  ctx.lineTo(x + size, cy);
  ctx.lineTo(cx, cy + h * 0.44);
  ctx.lineTo(x, cy);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
  if (size > 7) {
    ctx.strokeStyle = border;
    ctx.lineWidth = 0.6;
    ctx.stroke();
  }
  if (opts.showHeatmap) {
    ctx.fillStyle = heatmapColor(tile.R, 0.32);
    ctx.fill();
  }
  if (opts.showFibmob && tile.fibmob.polarity !== "positive") {
    ctx.fillStyle = tile.fibmob.polarity === "void" ? "rgba(255,68,68,0.22)" : "rgba(255,209,102,0.14)";
    ctx.fill();
  }
  if (tile.type === "water" && size > 8) {
    ctx.strokeStyle = "rgba(116,220,255,0.45)";
    ctx.beginPath();
    ctx.moveTo(x + size * 0.25, cy);
    ctx.lineTo(x + size * 0.75, cy - h * 0.08);
    ctx.stroke();
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
