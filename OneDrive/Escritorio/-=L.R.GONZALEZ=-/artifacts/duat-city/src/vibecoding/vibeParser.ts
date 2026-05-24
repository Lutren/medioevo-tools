import type { PixelMaterial } from "../physicsField/pixelTypes";
import type { VibeCompileResult, VibeSceneConfig } from "./vibeTypes";
import { getVibePreset } from "./vibePresets";
import { sanitizeVibePrompt } from "./vibeSafety";
import { compileSceneMood } from "../artDirection/sceneMoodCompiler";

export function parseVibePrompt(prompt: string): VibeCompileResult {
  const sanitized = sanitizeVibePrompt(prompt);
  const text = sanitized.prompt.toLowerCase();
  const art = compileSceneMood(sanitized.prompt);
  const preset = inferPreset(text);
  const base = { ...getVibePreset(preset), source: "prompt" as const, prompt: sanitized.prompt };
  const config: VibeSceneConfig = {
    ...base,
    timeOfDay: inferTimeOfDay(text, base.timeOfDay),
    weather: inferWeather(text, base.weather),
    palette: inferPalette(text, base.palette),
    lightProfile: inferLightProfile(text, base.lightProfile),
    fog: inferFog(text, base.fog),
    wetness: inferWetness(text, base.wetness),
    particles: inferParticles(text, base.particles),
    cameraPreset: inferCamera(text, base.cameraPreset),
    density: inferDensity(text, base.density),
    mood: inferMood(text, base.mood),
    materials: inferMaterials(text, base.materials),
    visualTags: Array.from(new Set([...base.visualTags, ...keywords(text), ...art.moodTags])),
    artDirection: {
      lightCanon: art.lightCanon,
      lightToken: art.lightToken,
      narrativeLenses: art.narrativeLenses,
      narrativeTokens: art.narrativeTokens,
      materialDetailProfile: art.materialDetailProfile,
      moodTags: art.moodTags,
      publicBoundaryNote: art.publicBoundaryNote,
    },
  };
  return {
    config,
    warnings: [...sanitized.warnings, ...art.warnings],
    parsedIntent: Array.from(new Set([...explainParsedIntent(text, config), ...art.parsedIntent])),
    cloudUsed: false,
    externalApiUsed: false,
  };
}

function inferPreset(text: string): string {
  if (has(text, ["archeopunk", "atardecer", "sunset"])) return "archeopunk_city_night";
  if (has(text, ["neon", "lluv", "rain", "charco", "street", "calle"])) return "neon_rain_street";
  if (has(text, ["tavern", "taberna", "interior", "calido", "warm"])) return "warm_interior_tavern";
  if (has(text, ["bosque", "forest", "winter", "snow", "nieve", "reflection", "reflejo"])) return "winter_tree_reflection";
  if (has(text, ["jungle", "selva", "waterfall", "cascada", "ruin"])) return "jungle_waterfall_ruin";
  if (has(text, ["desert", "desierto", "skyline"])) return "desert_skyline";
  if (has(text, ["observatory", "observatorio", "burst"])) return "observatory_light_burst";
  if (has(text, ["wheat", "trigo", "cloud"])) return "wheatfield_cloudscape";
  return "sunny_castle_lake";
}

function inferTimeOfDay(text: string, fallback: VibeSceneConfig["timeOfDay"]): VibeSceneConfig["timeOfDay"] {
  if (has(text, ["night", "noche", "neon"])) return "night";
  if (has(text, ["interior", "tavern", "taberna"])) return "interior";
  if (has(text, ["sunset", "golden", "atardecer"])) return "golden";
  if (has(text, ["dawn", "amanecer"])) return "dawn";
  if (has(text, ["day", "dia", "sol"])) return "day";
  return fallback;
}

function inferWeather(text: string, fallback: VibeSceneConfig["weather"]): VibeSceneConfig["weather"] {
  if (has(text, ["rain", "lluv", "charco"])) return "rain";
  if (has(text, ["snow", "nieve", "winter"])) return "snow";
  if (has(text, ["fog", "niebla", "mist", "humo"])) return "fog";
  if (has(text, ["jungle", "selva"])) return "jungle_mist";
  if (has(text, ["desert", "desierto", "haze"])) return "desert_haze";
  return fallback;
}

function inferPalette(text: string, fallback: string): string {
  if (has(text, ["warm", "calid", "tavern", "interior", "amber"])) return "warm_interior";
  if (has(text, ["teal", "cyan", "cian", "neon"])) return "cinematic_teal_amber";
  if (has(text, ["winter", "snow", "nieve"])) return "winter_reflection";
  if (has(text, ["jungle", "selva", "nature", "naturaleza"])) return "pictorial_nature";
  if (has(text, ["archeopunk", "ruin", "gold", "oro"])) return "medioevo_archeopunk";
  return fallback;
}

function inferLightProfile(text: string, fallback: string): string {
  if (has(text, ["neon", "cyan", "cian"])) return "neon-cyan-amber";
  if (has(text, ["torch", "fire", "fuego", "tavern", "taberna"])) return "torch-window";
  if (has(text, ["reflection", "reflejo", "water", "agua"])) return "water-reflection";
  if (has(text, ["ruin", "crystal", "anomaly", "anomalia"])) return "ruin-anomaly";
  return fallback;
}

function inferFog(text: string, fallback: number): number {
  if (has(text, ["mas niebla", "más niebla", "more fog"])) return 0.28;
  if (has(text, ["smoke", "humo", "fog", "niebla", "mist"])) return 0.2;
  if (has(text, ["clear", "limpio"])) return 0.02;
  return fallback;
}

function inferWetness(text: string, fallback: number): number {
  if (has(text, ["rain", "lluv", "charco", "wet", "mojado"])) return 0.92;
  if (has(text, ["reflejo", "reflection"])) return Math.max(fallback, 0.72);
  if (has(text, ["desert", "dry", "seco"])) return 0.04;
  return fallback;
}

function inferParticles(text: string, fallback: VibeSceneConfig["particles"]): VibeSceneConfig["particles"] {
  const set = new Set(fallback);
  if (has(text, ["rain", "lluv"])) set.add("rain");
  if (has(text, ["snow", "nieve"])) set.add("snow");
  if (has(text, ["smoke", "humo"])) set.add("smoke");
  if (has(text, ["dust", "polvo", "desert"])) set.add("dust");
  if (has(text, ["ember", "brasa", "fire"])) set.add("embers");
  return Array.from(set);
}

function inferCamera(text: string, fallback: VibeSceneConfig["cameraPreset"]): VibeSceneConfig["cameraPreset"] {
  if (has(text, ["street", "calle", "market", "mercado"])) return "street";
  if (has(text, ["interior", "tavern", "taberna"])) return "interior";
  if (has(text, ["lake", "lago", "reflection", "reflejo"])) return "lake";
  if (has(text, ["ruin", "ruina"])) return "ruin";
  return fallback;
}

function inferDensity(text: string, fallback: number): number {
  if (has(text, ["crowd", "dense", "denso", "market", "mercado"])) return 0.86;
  if (has(text, ["empty", "solo", "quiet"])) return 0.32;
  return fallback;
}

function inferMood(text: string, fallback: string): string {
  if (has(text, ["cinematic", "cinematograf", "dramatic"])) return "cinematic dramatic";
  if (has(text, ["warm", "calid"])) return "warm calm";
  if (has(text, ["mystery", "misterio", "anomaly"])) return "mystery anomaly";
  return fallback;
}

function inferMaterials(text: string, fallback: PixelMaterial[]): PixelMaterial[] {
  const set = new Set<PixelMaterial>(fallback);
  if (has(text, ["water", "agua", "charco", "rain"])) set.add("water");
  if (has(text, ["reflejo", "reflection"])) set.add("water");
  if (has(text, ["smoke", "humo"])) set.add("smoke");
  if (has(text, ["fire", "fuego", "torch"])) set.add("fire");
  if (has(text, ["neon", "cyan", "cian"])) set.add("neon");
  if (has(text, ["ruin", "ruina"])) set.add("ruinMatter");
  if (has(text, ["metal"])) set.add("metal");
  if (has(text, ["glass", "vidrio"])) set.add("glass");
  return Array.from(set);
}

function keywords(text: string): string[] {
  const pairs = [
    ["rain", ["rain", "lluv"]],
    ["neon", ["neon"]],
    ["interior", ["interior", "taberna", "tavern"]],
    ["ruin", ["ruin", "ruina"]],
    ["water", ["water", "agua", "reflejo", "reflection"]],
    ["smoke", ["smoke", "humo"]],
    ["warm", ["warm", "calid", "ambar", "amber"]],
    ["night", ["night", "noche"]],
    ["jungle", ["jungle", "selva"]],
    ["desert", ["desert", "desierto"]],
    ["winter", ["winter", "snow", "nieve", "bosque"]],
    ["sunset", ["sunset", "atardecer"]],
    ["beautiful", ["bonito", "beautiful"]],
    ["less-debug", ["menos debug", "less debug"]],
  ] as const;
  return pairs.filter(([, words]) => has(text, [...words])).map(([label]) => label);
}

function has(text: string, words: string[]): boolean {
  return words.some(word => text.includes(word));
}

function explainParsedIntent(text: string, config: VibeSceneConfig): string[] {
  const intent = [
    `preset:${config.id}`,
    `time:${config.timeOfDay}`,
    `weather:${config.weather}`,
    `palette:${config.palette}`,
    `light:${config.lightProfile}`,
  ];
  if (has(text, ["menos debug", "less debug", "mas bonito", "más bonito", "beautiful", "bonito"])) intent.push("ui:prefer_beautiful_less_debug");
  if (has(text, ["reflejo", "reflection", "agua", "water"])) intent.push("material:water_reflection");
  if (has(text, ["fuego", "fire", "mercado", "market"])) intent.push("material:fire_market");
  if (has(text, ["humo", "smoke", "niebla", "fog"])) intent.push("atmosphere:scatter");
  return Array.from(new Set(intent));
}
