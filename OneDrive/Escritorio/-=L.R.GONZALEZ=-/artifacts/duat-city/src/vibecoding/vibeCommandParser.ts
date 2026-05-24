import { compileSceneMood } from "../artDirection/sceneMoodCompiler";
import { inferStyleProfileFromPrompt } from "../style/styleAnalyzer";
import type { VibeScenePatch } from "./vibeSceneActions";

export interface VibeCommandParseResult {
  parsedIntent: string[];
  scenePatch: VibeScenePatch;
  warnings: string[];
  preview: string;
  cloudUsed: false;
  externalApiUsed: false;
}

export function parseVibeCommand(command: string): VibeCommandParseResult {
  const text = normalize(command);
  const patch: VibeScenePatch = { materials: [], lights: [], buildings: [], quests: [], styleProfile: inferStyleProfileFromPrompt(text) };
  const intent: string[] = [`style:${patch.styleProfile}`];
  if (has(text, ["calle lluviosa", "lluvia", "rain", "neon"])) {
    patch.weather = "rain";
    patch.timeOfDay = "night";
    patch.vibePreset = "neon_rain_street";
    patch.materials?.push({ x: 21, y: 19, material: "water" }, { x: 22, y: 19, material: "neon" });
    patch.lights?.push({ x: 22, y: 18, kind: "neon" });
    intent.push("scene:neon_rain_street");
  }
  if (has(text, ["archivo prohibido", "archivo"])) {
    patch.vibePreset = "forbidden_archive";
    patch.buildings?.push("archive");
    patch.lights?.push({ x: 24, y: 14, kind: "window" });
    intent.push("scene:forbidden_archive");
  }
  if (has(text, ["forja", "forge", "fuego naranja"])) {
    patch.vibePreset = "central_forge";
    patch.buildings?.push("forge");
    patch.materials?.push({ x: 24, y: 17, material: "fire" }, { x: 24, y: 16, material: "smoke" });
    patch.lights?.push({ x: 24, y: 17, kind: "fire" });
    intent.push("scene:central_forge");
  }
  if (has(text, ["jardin bio", "biomecan", "bioluminiscencia"])) {
    patch.vibePreset = "biomechanical_garden";
    patch.materials?.push({ x: 21, y: 18, material: "water" }, { x: 23, y: 18, material: "neon" });
    patch.lights?.push({ x: 23, y: 18, kind: "magic" });
    intent.push("scene:biomechanical_garden");
  }
  if (has(text, ["mercado subterraneo", "mercado", "luces rosas"])) {
    patch.vibePreset = "underground_market";
    patch.buildings?.push("market");
    patch.materials?.push({ x: 25, y: 18, material: "smoke" }, { x: 26, y: 18, material: "neon" });
    patch.lights?.push({ x: 26, y: 17, kind: "neon" });
    intent.push("scene:underground_market");
  }
  if (has(text, ["coloca un puente", "puente"])) intent.push("build:bridge_segment");
  if (has(text, ["lampara de bronce", "lámpara de bronce"])) intent.push("prop:bronze_lamp_post");
  if (has(text, ["pon agua", "canal"])) patch.materials?.push({ x: 20, y: 20, material: "water" });
  if (has(text, ["agrega humo", "humo"])) patch.materials?.push({ x: 24, y: 15, material: "smoke" });
  if (has(text, ["enciende fuego", "fuego"])) patch.materials?.push({ x: 24, y: 17, material: "fire" });
  if (has(text, ["coloca agentes", "agentes"])) patch.agents = 8;
  if (has(text, ["crea una mision", "misión", "ruina"])) patch.quests?.push("investigate ruin signal");
  if (has(text, ["activa lluvia"])) patch.weather = "rain";
  if (has(text, ["cambia a noche", "noche"])) patch.timeOfDay = "night";
  const art = compileSceneMood(command);
  intent.push(...art.parsedIntent);
  return {
    parsedIntent: Array.from(new Set(intent)),
    scenePatch: patch,
    warnings: art.warnings,
    preview: `MEDIOEVO original patch: ${[patch.vibePreset, patch.styleProfile, patch.timeOfDay, patch.weather].filter(Boolean).join(" / ")}`,
    cloudUsed: false,
    externalApiUsed: false,
  };
}

function normalize(value: string): string {
  return value.toLowerCase().replace(/[áà]/g, "a").replace(/[éè]/g, "e").replace(/[íì]/g, "i").replace(/[óò]/g, "o").replace(/[úùü]/g, "u");
}

function has(text: string, words: string[]): boolean {
  return words.some(word => text.includes(normalize(word)));
}
