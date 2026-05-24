import type { DitherOptions, RGB } from "./colorTypes";
import { clamp255 } from "./colorSpace";

export const BAYER_4 = [
  [0, 8, 2, 10],
  [12, 4, 14, 6],
  [3, 11, 1, 9],
  [15, 7, 13, 5],
];

export const BAYER_8 = [
  [0, 48, 12, 60, 3, 51, 15, 63],
  [32, 16, 44, 28, 35, 19, 47, 31],
  [8, 56, 4, 52, 11, 59, 7, 55],
  [40, 24, 36, 20, 43, 27, 39, 23],
  [2, 50, 14, 62, 1, 49, 13, 61],
  [34, 18, 46, 30, 33, 17, 45, 29],
  [10, 58, 6, 54, 9, 57, 5, 53],
  [42, 26, 38, 22, 41, 25, 37, 21],
];

export function orderedDither(rgb: RGB, x: number, y: number, options: Partial<DitherOptions> = {}): RGB {
  const matrix = options.matrix === "bayer8" ? BAYER_8 : BAYER_4;
  const n = matrix.length;
  const max = n * n;
  const threshold = (matrix[Math.abs(y) % n][Math.abs(x) % n] + 0.5) / max - 0.5;
  const strength = options.strength ?? 16;
  const offset = threshold * strength;
  return {
    r: clamp255(rgb.r + offset),
    g: clamp255(rgb.g + offset),
    b: clamp255(rgb.b + offset),
  };
}

export function quantizeToPalette(rgb: RGB, palette: RGB[]): RGB {
  if (palette.length === 0) return rgb;
  let best = palette[0];
  let bestDistance = Number.POSITIVE_INFINITY;
  for (const candidate of palette) {
    const d = squaredDistance(rgb, candidate);
    if (d < bestDistance) {
      bestDistance = d;
      best = candidate;
    }
  }
  return { ...best };
}

export function ditherAndQuantize(rgb: RGB, x: number, y: number, palette: RGB[], options: Partial<DitherOptions> = {}): RGB {
  return quantizeToPalette(orderedDither(rgb, x, y, options), palette);
}

function squaredDistance(a: RGB, b: RGB): number {
  return (a.r - b.r) ** 2 + (a.g - b.g) ** 2 + (a.b - b.b) ** 2;
}
