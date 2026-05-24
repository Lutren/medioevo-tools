import type { HarmonyKind, RGB } from "./colorTypes";
import { hslToRgb, normalizeHue, rgbToHsl } from "./colorSpace";

export function harmony(base: RGB, kind: HarmonyKind): RGB[] {
  const hsl = rgbToHsl(base);
  const emit = (offset: number, s = hsl.s, l = hsl.l) => hslToRgb({ h: normalizeHue(hsl.h + offset), s, l });
  switch (kind) {
    case "complementary":
      return [base, emit(180), emit(180, hsl.s * 0.7, Math.min(1, hsl.l + 0.18))];
    case "analogous":
      return [emit(-28), base, emit(28), emit(46, hsl.s * 0.8, hsl.l)];
    case "triadic":
      return [base, emit(120), emit(240)];
    case "split-complementary":
      return [base, emit(150), emit(210)];
    case "monochrome":
      return [
        emit(0, hsl.s * 0.9, Math.max(0.08, hsl.l * 0.45)),
        emit(0, hsl.s, hsl.l),
        emit(0, hsl.s * 0.7, Math.min(0.96, hsl.l + 0.28)),
      ];
    case "cinematic-teal-amber":
      return [
        { r: 10, g: 35, b: 44 },
        { r: 17, g: 161, b: 166 },
        { r: 246, g: 154, b: 68 },
        { r: 255, g: 226, b: 154 },
      ];
    case "medioevo-archeopunk":
      return [
        { r: 15, g: 18, b: 22 },
        { r: 92, g: 79, b: 61 },
        { r: 198, g: 151, b: 80 },
        { r: 31, g: 207, b: 214 },
        { r: 119, g: 47, b: 184 },
      ];
  }
}
