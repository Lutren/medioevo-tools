import type { StyleProfile } from "../style/styleTypes";
import { getStyleProfile } from "../style/styleProfiles";
import { generateProceduralAgent } from "./proceduralAgentGenerator";
import { generateProceduralBuilding } from "./proceduralBuildingGenerator";
import { generateProceduralProp } from "./proceduralPropGenerator";
import { generateProceduralTile } from "./proceduralTileGenerator";
import { generateProceduralUi } from "./proceduralUiGenerator";
import type { PixelArtBitmap } from "./pixelArtGenerator";

export interface GenerativeSceneComposition {
  schema: "duat.generative_scene.v1_2";
  styleProfile: StyleProfile;
  seed: number;
  elements: Record<string, PixelArtBitmap>;
}

export function composeGenerativeScene(styleProfileId = "archeopunk_city_rain", seed = 1): GenerativeSceneComposition {
  const styleProfile = getStyleProfile(styleProfileId);
  return {
    schema: "duat.generative_scene.v1_2",
    styleProfile,
    seed,
    elements: {
      wet_street_tile: generateProceduralTile("wet_street", seed + 1, styleProfileId),
      canal_edge: generateProceduralTile("canal_edge", seed + 2, styleProfileId),
      bridge_segment: generateProceduralTile("bridge_segment", seed + 3, styleProfileId),
      archive_building: generateProceduralBuilding("archive", seed + 4, styleProfileId),
      forge_building: generateProceduralBuilding("forge", seed + 5, styleProfileId),
      bronze_lamp_post: generateProceduralProp("bronze_lamp_post", seed + 6, styleProfileId),
      terminal_frame: generateProceduralUi("terminal_frame", seed + 7),
      r_phi_gauge: generateProceduralUi("r_phi_gauge", seed + 8),
      action_gate_icons: generateProceduralUi("action_gate_icons", seed + 9),
      q_state_glyphs: generateProceduralUi("q_state_glyphs", seed + 10),
      agent: generateProceduralAgent("small_agent_silhouette", seed + 11, styleProfileId),
    },
  };
}
