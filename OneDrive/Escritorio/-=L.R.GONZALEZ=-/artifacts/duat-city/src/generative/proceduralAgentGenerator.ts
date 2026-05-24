import type { PixelArtBitmap } from "./pixelArtGenerator";
import { generatePixelArtBitmap } from "./pixelArtGenerator";
import type { AgentNeeds } from "../core/types";
import { randBetween, seededRandom } from "../core/math";
import { generateAgentLineage, generateOriginStory } from "./agentLineageGenerator";

export function generateProceduralAgent(role = "small_agent_silhouette", seed = 1, styleProfile = "archeopunk_city_rain"): PixelArtBitmap {
  return generatePixelArtBitmap(8, 12, seed, styleProfile, `agent:${role}`);
}

export interface ProceduralAgentProfile {
  schema: "duat.theater-agent-profile.v1";
  role: string;
  needs: AgentNeeds;
  lineage: ReturnType<typeof generateAgentLineage>;
  originStory: string;
  sprite: PixelArtBitmap;
  skills: string[];
  readyForAcademy: true;
}

export function generateTheaterAgentProfile(role = "Observer", seed = 1, styleProfile = "archeopunk_city_rain"): ProceduralAgentProfile {
  const rng = seededRandom(`theater:${role}:${seed}`);
  const lineage = generateAgentLineage(role, rng);
  const needs: AgentNeeds = {
    energy: randBetween(0.62, 0.94, rng),
    hunger: randBetween(0.58, 0.92, rng),
    social: randBetween(0.5, 0.9, rng),
    purpose: randBetween(0.55, 0.95, rng),
    safety: randBetween(0.64, 0.96, rng),
    curiosity: randBetween(0.55, 0.98, rng),
  };
  return {
    schema: "duat.theater-agent-profile.v1",
    role,
    needs,
    lineage,
    originStory: generateOriginStory(role, lineage),
    sprite: generateProceduralAgent(role, seed, styleProfile),
    skills: [],
    readyForAcademy: true,
  };
}
