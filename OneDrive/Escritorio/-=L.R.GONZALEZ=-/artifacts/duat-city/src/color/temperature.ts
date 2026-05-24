import type { RGB } from "./colorTypes";
import { clamp255, mixRgb, safeRgb } from "./colorSpace";

export function kelvinToRgb(kelvin: number): RGB {
  const k = Math.max(1000, Math.min(40000, kelvin)) / 100;
  let r: number;
  let g: number;
  let b: number;
  if (k <= 66) {
    r = 255;
    g = 99.4708025861 * Math.log(k) - 161.1195681661;
    b = k <= 19 ? 0 : 138.5177312231 * Math.log(k - 10) - 305.0447927307;
  } else {
    r = 329.698727446 * Math.pow(k - 60, -0.1332047592);
    g = 288.1221695283 * Math.pow(k - 60, -0.0755148492);
    b = 255;
  }
  return { r: clamp255(r), g: clamp255(g), b: clamp255(b) };
}

export function blendLightTemperature(base: RGB, kelvin: number, amount: number): RGB {
  return mixRgb(base, kelvinToRgb(kelvin), amount);
}

export function dayNightPalette(hour: number): { ambient: RGB; key: RGB; fill: RGB; name: string } {
  const h = ((hour % 24) + 24) % 24;
  if (h >= 6 && h < 10) {
    return { name: "morning", ambient: kelvinToRgb(5200), key: kelvinToRgb(4300), fill: safeRgb({ r: 120, g: 170, b: 210 }) };
  }
  if (h >= 10 && h < 17) {
    return { name: "day", ambient: kelvinToRgb(6500), key: kelvinToRgb(5800), fill: safeRgb({ r: 170, g: 205, b: 235 }) };
  }
  if (h >= 17 && h < 20) {
    return { name: "golden", ambient: kelvinToRgb(4200), key: kelvinToRgb(3000), fill: safeRgb({ r: 95, g: 130, b: 185 }) };
  }
  return { name: "night", ambient: safeRgb({ r: 26, g: 40, b: 68 }), key: kelvinToRgb(7400), fill: kelvinToRgb(2200) };
}
