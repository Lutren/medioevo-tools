import type { RGB, ToneMappingOptions } from "./colorTypes";
import { DEFAULT_TONE_MAPPING } from "./colorTypes";
import { clamp01, clamp255, rgbToHsl, hslToRgb } from "./colorSpace";

export function toneMapRgb(rgb: RGB, options: Partial<ToneMappingOptions> = {}): RGB {
  const opt = { ...DEFAULT_TONE_MAPPING, ...options };
  const exposure = Math.max(0, opt.exposure);
  const gamma = Math.max(0.1, opt.gamma);
  const contrast = Math.max(0, opt.contrast);
  const rolloff = clamp01(opt.highlightRolloff);
  const mapChannel = (value: number) => {
    let v = clamp01(value / 255);
    v = 1 - Math.exp(-v * exposure);
    v = v < 0.5 ? v + opt.shadowLift * (1 - v * 2) : v;
    v = v > rolloff ? rolloff + (v - rolloff) * 0.55 : v;
    v = (v - 0.5) * contrast + 0.5;
    v = Math.pow(clamp01(v), 1 / gamma);
    return clamp255(v * 255);
  };
  const mapped = { r: mapChannel(rgb.r), g: mapChannel(rgb.g), b: mapChannel(rgb.b) };
  if (opt.saturation === 1) return mapped;
  const hsl = rgbToHsl(mapped);
  return hslToRgb({ ...hsl, s: clamp01(hsl.s * opt.saturation) });
}

export function bloomMask(rgb: RGB, threshold = DEFAULT_TONE_MAPPING.bloomThreshold): number {
  const luminance = (0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b) / 255;
  return clamp01((luminance - threshold) / Math.max(0.001, 1 - threshold));
}
