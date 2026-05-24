import type { PixelRealismConfig } from "../pixelRealism/renderPasses";
import { defaultPixelRealismConfig } from "../pixelRealism/renderPasses";
import type { VibeCompileResult, VibeSceneConfig } from "./vibeTypes";
import { parseVibePrompt } from "./vibeParser";
import { getVibePreset } from "./vibePresets";
import { compileSceneMood } from "../artDirection/sceneMoodCompiler";

export function compileVibeScene(input: string, source: "prompt" | "preset" = "prompt"): VibeCompileResult {
  if (source === "preset") {
    const config = getVibePreset(input);
    const art = compileSceneMood(config.mood + " " + config.visualTags.join(" "));
    const artConfig: VibeSceneConfig = {
      ...config,
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
    return { config: artConfig, warnings: [], parsedIntent: [`preset:${config.id}`, `time:${config.timeOfDay}`, `weather:${config.weather}`, `light:${config.lightProfile}`, ...art.parsedIntent], cloudUsed: false, externalApiUsed: false };
  }
  return parseVibePrompt(input);
}

export function vibeToPixelRealismConfig(scene: VibeSceneConfig, previous: PixelRealismConfig = defaultPixelRealismConfig()): PixelRealismConfig {
  return {
    ...previous,
    timeOfDay: scene.timeOfDay,
    weather: scene.weather,
    paletteProfile: scene.palette,
    lightProfile: scene.artDirection?.lightToken ?? scene.lightProfile,
    bloomAmount: scene.lightProfile.includes("neon") || scene.lightProfile.includes("burst") ? 0.52 : previous.bloomAmount,
    lightIntensity: scene.timeOfDay === "night" ? 1.22 : scene.timeOfDay === "interior" ? 1.1 : 1,
    dither: true,
    pixelScale: previous.pixelScale,
    vibePreset: scene.id,
    mood: scene.artDirection?.moodTags?.join(" ") ?? scene.mood,
  };
}
