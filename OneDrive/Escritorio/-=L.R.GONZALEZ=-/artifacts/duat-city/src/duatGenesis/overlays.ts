import type { DuatOverlayMode } from "./types";

export type OverlayKind = DuatOverlayMode;

/**
 * Render a DUAT Genesis field overlay into a canvas ImageData.
 * Each cell is drawn as a `scale x scale` block of the same color.
 * @param ctx Canvas 2D context
 * @param psi field values [0, 1]
 * @param gravity field values [0, 1]
 * @param light field values [0, 1]
 * @param width field width in cells
 * @param height field height in cells
 * @param overlay which overlay to draw
 * @param scale pixel size per cell (default 4)
 */
export function renderPsiOverlay(
  ctx: CanvasRenderingContext2D,
  psi: Float32Array,
  width: number,
  height: number,
  scale = 4,
): void {
  const img = ctx.createImageData(width * scale, height * scale);
  const data = img.data;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const v = psi[id] ?? 0;
      const [r, g, b] = psiToRgb(v);
      fillBlock(data, x, y, width, height, scale, r, g, b);
    }
  }
  ctx.putImageData(img, 0, 0);
}

export function renderGravityOverlay(
  ctx: CanvasRenderingContext2D,
  gravity: Float32Array,
  width: number,
  height: number,
  scale = 4,
): void {
  const img = ctx.createImageData(width * scale, height * scale);
  const data = img.data;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const v = gravity[id] ?? 0;
      const [r, g, b] = gravityToRgb(v);
      fillBlock(data, x, y, width, height, scale, r, g, b);
    }
  }
  ctx.putImageData(img, 0, 0);
}

export function renderLightOverlay(
  ctx: CanvasRenderingContext2D,
  light: Float32Array,
  width: number,
  height: number,
  scale = 4,
): void {
  const img = ctx.createImageData(width * scale, height * scale);
  const data = img.data;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const v = light[id] ?? 0;
      const [r, g, b] = lightToRgb(v);
      fillBlock(data, x, y, width, height, scale, r, g, b);
    }
  }
  ctx.putImageData(img, 0, 0);
}

export function renderObserverDeltaOverlay(
  ctx: CanvasRenderingContext2D,
  psi: Float32Array,
  observerA: { x: number; y: number; strength: number; saturation: number },
  observerB: { x: number; y: number; strength: number; saturation: number },
  width: number,
  height: number,
  scale = 4,
): void {
  const img = ctx.createImageData(width * scale, height * scale);
  const data = img.data;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const v = psi[id] ?? 0;
      const a = 1 - Math.exp(-v * (1 + observerA.saturation * 2.8));
      const b = 1 - Math.exp(-v * (1 + observerB.saturation * 2.8));
      const delta = Math.abs(a - b);
      const r = Math.round(delta * 230);
      const g = Math.round((1 - delta) * v * 190);
      const b_ = Math.round((delta + v) * 150);
      fillBlock(data, x, y, width, height, scale, r, g, b_);
    }
  }
  ctx.putImageData(img, 0, 0);
}

function psiToRgb(v: number): [number, number, number] {
  return [Math.round(v * 80 + v * v * 80), Math.round(v * 75 + (1 - v) * 60), Math.round(v * 70 + v * v * 120)];
}

function gravityToRgb(v: number): [number, number, number] {
  return [Math.round(v * 230), Math.round(v * v * 120), Math.round(v * 60)];
}

function lightToRgb(v: number): [number, number, number] {
  return [Math.round(v * 40), Math.round(v * 130), Math.round(v * 250)];
}

function fillBlock(
  data: Uint8ClampedArray,
  cx: number,
  cy: number,
  width: number,
  height: number,
  scale: number,
  r: number,
  g: number,
  b: number,
): void {
  for (let dy = 0; dy < scale; dy += 1) {
    for (let dx = 0; dx < scale; dx += 1) {
      const px = cx * scale + dx;
      const py = cy * scale + dy;
      const id = (py * (width * scale) + px) * 4;
      data[id] = r;
      data[id + 1] = g;
      data[id + 2] = b;
      data[id + 3] = 255;
    }
  }
}
