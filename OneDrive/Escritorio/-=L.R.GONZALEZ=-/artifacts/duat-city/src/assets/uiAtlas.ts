import { createAssetAtlasV2 } from "./assetAtlasV2";

export function createUiAtlas(styleProfile = "duat_operational_terminal") {
  return createAssetAtlasV2([
    { domain: "ui", type: "terminal_frame" },
    { domain: "ui", type: "r_phi_gauge" },
    { domain: "ui", type: "tube_meter" },
    { domain: "ui", type: "action_gate_icons" },
    { domain: "ui", type: "q_state_glyphs" },
  ], styleProfile);
}
