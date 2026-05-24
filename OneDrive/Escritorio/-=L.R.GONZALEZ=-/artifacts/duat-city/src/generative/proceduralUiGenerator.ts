import type { PixelArtBitmap } from "./pixelArtGenerator";
import { generatePixelArtBitmap } from "./pixelArtGenerator";

export type ProceduralUiKind = "terminal_frame" | "r_phi_gauge" | "tube_meter" | "action_gate_icons" | "q_state_glyphs";

export function generateProceduralUi(kind: ProceduralUiKind, seed = 1, styleProfile = "duat_operational_terminal"): PixelArtBitmap {
  const width = kind === "terminal_frame" ? 32 : 16;
  return generatePixelArtBitmap(width, 12, seed, styleProfile, `ui:${kind}`);
}
