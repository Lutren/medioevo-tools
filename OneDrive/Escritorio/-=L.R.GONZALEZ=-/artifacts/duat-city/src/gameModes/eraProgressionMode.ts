import type { EraDefinition, EraId } from "./gameModeTypes";

export const ERA_DEFINITIONS: EraDefinition[] = [
  { id: "unicellularidad", label: "Unicellularidad", materialBias: ["water"], languageTone: "impulse", audioMotif: "low pulse", lightProfile: "diffuse primordial", questBias: ["stabilize first membrane"], uiSkin: "organic minimal" },
  { id: "multicelularidad", label: "Multicelularidad", materialBias: ["water", "forest"], languageTone: "coordination", audioMotif: "layered pulse", lightProfile: "soft growth", questBias: ["coordinate cells"], uiSkin: "cluster organic" },
  { id: "prehistoria", label: "Prehistoria", materialBias: ["stone", "forest"], languageTone: "gesture", audioMotif: "stone and wind", lightProfile: "fire cave", questBias: ["secure shelter"], uiSkin: "raw marks" },
  { id: "primeros_cavernicolas", label: "Primeros cavernicolas", materialBias: ["stone", "forest"], languageTone: "symbol", audioMotif: "bone rhythm", lightProfile: "torch", questBias: ["share first sign"], uiSkin: "wall glyph" },
  { id: "agricultura", label: "Agricultura", materialBias: ["garden", "water"], languageTone: "calendar", audioMotif: "field rhythm", lightProfile: "sun field", questBias: ["protect harvest"], uiSkin: "woven grid" },
  { id: "ciudad_antigua", label: "Ciudad antigua", materialBias: ["plaza", "temple"], languageTone: "law", audioMotif: "stone city", lightProfile: "ritual sun", questBias: ["codify gate"], uiSkin: "tablet civic" },
  { id: "medieval", label: "Medieval", materialBias: ["wall", "market"], languageTone: "oath", audioMotif: "bell and forge", lightProfile: "warm interior", questBias: ["hold the gate"], uiSkin: "brass parchment" },
  { id: "industrial", label: "Industrial", materialBias: ["workshop", "road"], languageTone: "protocol", audioMotif: "machine pulse", lightProfile: "smoke amber", questBias: ["repair pressure line"], uiSkin: "iron console" },
  { id: "cyber_archeopunk", label: "Cyber/archeopunk", materialBias: ["archive", "observatory"], languageTone: "signal", audioMotif: "neon relay", lightProfile: "cyan amber rain", questBias: ["decode surveillance signal"], uiSkin: "DUAT terminal" },
  { id: "duat_epoch", label: "DUAT epoch", materialBias: ["gatehouse", "ruin"], languageTone: "epistemic", audioMotif: "gate resonance", lightProfile: "chiaroscuro signal", questBias: ["externalize handoff"], uiSkin: "OSIT diegetic" },
];

export function getEraDefinition(id: EraId): EraDefinition {
  return ERA_DEFINITIONS.find(era => era.id === id) ?? ERA_DEFINITIONS[ERA_DEFINITIONS.length - 1];
}

export function listEras(secretUnlocked = false): EraDefinition[] {
  return secretUnlocked ? [...ERA_DEFINITIONS] : ERA_DEFINITIONS.filter(era => era.id !== "duat_epoch");
}

export function compileEraConfig(id: EraId, secretUnlocked = false) {
  const era = getEraDefinition(id);
  return {
    era,
    secretModeAvailable: secretUnlocked,
    changes: {
      materials: era.materialBias,
      language: era.languageTone,
      audio: era.audioMotif,
      light: era.lightProfile,
      quests: era.questBias,
      ui: era.uiSkin,
    },
    historicalClaim: false,
    boundary: "fictional evolutionary game mode",
  };
}
