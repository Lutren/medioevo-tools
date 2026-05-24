import type { HSL, HSV, OKLab, RGB } from "./colorTypes";

export function clamp01(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(1, value));
}

export function clamp255(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(255, Math.round(value)));
}

export function safeRgb(input: RGB): RGB {
  return { r: clamp255(input.r), g: clamp255(input.g), b: clamp255(input.b) };
}

export function rgbToHex(rgb: RGB): string {
  const c = safeRgb(rgb);
  return `#${toHex(c.r)}${toHex(c.g)}${toHex(c.b)}`;
}

export function hexToRgb(hex: string): RGB {
  const clean = hex.replace("#", "").trim();
  const normalized = clean.length === 3
    ? clean.split("").map(ch => `${ch}${ch}`).join("")
    : clean.padEnd(6, "0").slice(0, 6);
  const n = Number.parseInt(normalized, 16);
  if (!Number.isFinite(n)) return { r: 0, g: 0, b: 0 };
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
}

export function srgbChannelToLinear(value: number): number {
  const c = clamp01(value / 255);
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

export function linearChannelToSrgb(value: number): number {
  const c = clamp01(value);
  const srgb = c <= 0.0031308 ? c * 12.92 : 1.055 * Math.pow(c, 1 / 2.4) - 0.055;
  return clamp255(srgb * 255);
}

export function rgbToLinearRgb(rgb: RGB): RGB {
  return {
    r: srgbChannelToLinear(rgb.r),
    g: srgbChannelToLinear(rgb.g),
    b: srgbChannelToLinear(rgb.b),
  };
}

export function linearRgbToRgb(rgb: RGB): RGB {
  return {
    r: linearChannelToSrgb(rgb.r),
    g: linearChannelToSrgb(rgb.g),
    b: linearChannelToSrgb(rgb.b),
  };
}

export function rgbToHsl(rgb: RGB): HSL {
  const r = clamp01(rgb.r / 255);
  const g = clamp01(rgb.g / 255);
  const b = clamp01(rgb.b / 255);
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const l = (max + min) / 2;
  const d = max - min;
  if (d === 0) return { h: 0, s: 0, l };
  const s = d / (1 - Math.abs(2 * l - 1));
  let h = 0;
  if (max === r) h = 60 * (((g - b) / d) % 6);
  else if (max === g) h = 60 * ((b - r) / d + 2);
  else h = 60 * ((r - g) / d + 4);
  return { h: normalizeHue(h), s: clamp01(s), l: clamp01(l) };
}

export function hslToRgb(hsl: HSL): RGB {
  const h = normalizeHue(hsl.h);
  const s = clamp01(hsl.s);
  const l = clamp01(hsl.l);
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = l - c / 2;
  let rp = 0;
  let gp = 0;
  let bp = 0;
  if (h < 60) [rp, gp, bp] = [c, x, 0];
  else if (h < 120) [rp, gp, bp] = [x, c, 0];
  else if (h < 180) [rp, gp, bp] = [0, c, x];
  else if (h < 240) [rp, gp, bp] = [0, x, c];
  else if (h < 300) [rp, gp, bp] = [x, 0, c];
  else [rp, gp, bp] = [c, 0, x];
  return safeRgb({ r: (rp + m) * 255, g: (gp + m) * 255, b: (bp + m) * 255 });
}

export function rgbToHsv(rgb: RGB): HSV {
  const r = clamp01(rgb.r / 255);
  const g = clamp01(rgb.g / 255);
  const b = clamp01(rgb.b / 255);
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const d = max - min;
  let h = 0;
  if (d !== 0) {
    if (max === r) h = 60 * (((g - b) / d) % 6);
    else if (max === g) h = 60 * ((b - r) / d + 2);
    else h = 60 * ((r - g) / d + 4);
  }
  return { h: normalizeHue(h), s: max === 0 ? 0 : d / max, v: max };
}

export function hsvToRgb(hsv: HSV): RGB {
  const h = normalizeHue(hsv.h);
  const s = clamp01(hsv.s);
  const v = clamp01(hsv.v);
  const c = v * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = v - c;
  let rp = 0;
  let gp = 0;
  let bp = 0;
  if (h < 60) [rp, gp, bp] = [c, x, 0];
  else if (h < 120) [rp, gp, bp] = [x, c, 0];
  else if (h < 180) [rp, gp, bp] = [0, c, x];
  else if (h < 240) [rp, gp, bp] = [0, x, c];
  else if (h < 300) [rp, gp, bp] = [x, 0, c];
  else [rp, gp, bp] = [c, 0, x];
  return safeRgb({ r: (rp + m) * 255, g: (gp + m) * 255, b: (bp + m) * 255 });
}

export function rgbToOKLab(rgb: RGB): OKLab {
  const lrgb = rgbToLinearRgb(rgb);
  const l = 0.4122214708 * lrgb.r + 0.5363325363 * lrgb.g + 0.0514459929 * lrgb.b;
  const m = 0.2119034982 * lrgb.r + 0.6806995451 * lrgb.g + 0.1073969566 * lrgb.b;
  const s = 0.0883024619 * lrgb.r + 0.2817188376 * lrgb.g + 0.6299787005 * lrgb.b;
  const l_ = Math.cbrt(Math.max(0, l));
  const m_ = Math.cbrt(Math.max(0, m));
  const s_ = Math.cbrt(Math.max(0, s));
  return {
    L: 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
    a: 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
    b: 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
  };
}

export function okLabToRgb(lab: OKLab): RGB {
  const l_ = lab.L + 0.3963377774 * lab.a + 0.2158037573 * lab.b;
  const m_ = lab.L - 0.1055613458 * lab.a - 0.0638541728 * lab.b;
  const s_ = lab.L - 0.0894841775 * lab.a - 1.2914855480 * lab.b;
  const l = l_ * l_ * l_;
  const m = m_ * m_ * m_;
  const s = s_ * s_ * s_;
  return linearRgbToRgb({
    r: +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    g: -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    b: -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
  });
}

export function mixRgb(a: RGB, b: RGB, t: number): RGB {
  const k = clamp01(t);
  return safeRgb({
    r: a.r + (b.r - a.r) * k,
    g: a.g + (b.g - a.g) * k,
    b: a.b + (b.b - a.b) * k,
  });
}

export function normalizeHue(hue: number): number {
  if (!Number.isFinite(hue)) return 0;
  return ((hue % 360) + 360) % 360;
}

function toHex(value: number): string {
  return clamp255(value).toString(16).padStart(2, "0");
}
