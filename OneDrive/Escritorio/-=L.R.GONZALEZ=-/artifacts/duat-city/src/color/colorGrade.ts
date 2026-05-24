import type { PaletteProfile, RGB, ToneMappingOptions } from "./colorTypes";
import { mixRgb } from "./colorSpace";
import { toneMapRgb } from "./toneMapping";

export function gradeRgb(rgb: RGB, palette: PaletteProfile, options: Partial<ToneMappingOptions> = {}): RGB {
  const toned = toneMapRgb(rgb, options);
  const tint = palette.colors[Math.min(1, palette.colors.length - 1)] ?? toned;
  const warmth = palette.temperature === "warm" ? 0.08 : palette.temperature === "cool" ? 0.06 : 0.04;
  return mixRgb(toned, tint, warmth);
}

export function colorHealth(colors: RGB[]): { R_color: number; Phi_color: number; finite: boolean } {
  const finite = colors.every(c => Number.isFinite(c.r) && Number.isFinite(c.g) && Number.isFinite(c.b));
  const outOfRange = colors.filter(c => c.r < 0 || c.r > 255 || c.g < 0 || c.g > 255 || c.b < 0 || c.b > 255).length;
  const diversity = new Set(colors.map(c => `${Math.round(c.r / 16)}:${Math.round(c.g / 16)}:${Math.round(c.b / 16)}`)).size;
  const R_color = finite ? Math.min(1, outOfRange / Math.max(1, colors.length) + (diversity < 3 ? 0.08 : 0)) : 1;
  return { R_color, Phi_color: Math.max(0, Math.min(1, 1 - R_color)), finite };
}
