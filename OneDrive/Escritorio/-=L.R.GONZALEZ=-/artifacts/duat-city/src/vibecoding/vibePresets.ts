import type { VibeSceneConfig } from "./vibeTypes";

export const VIBE_PRESETS: Record<string, VibeSceneConfig> = {
  sunny_castle_lake: preset("sunny_castle_lake", "day", "clear", "pictorial_nature", "sun-lake", 0.02, 0.18, [], "lake", "clear civic lake", ["stone", "water", "grass", "gold"]),
  neon_rain_street: preset("neon_rain_street", "night", "rain", "cinematic_teal_amber", "neon-rain", 0.18, 0.9, ["rain", "smoke"], "street", "cyan amber rain market", ["brick", "water", "neon", "smoke", "metal"]),
  warm_interior_tavern: preset("warm_interior_tavern", "interior", "clear", "warm_interior", "torch-window", 0.04, 0.2, ["embers", "smoke"], "interior", "warm tavern interior", ["wood", "brick", "cloth", "fire", "skin"]),
  winter_tree_reflection: preset("winter_tree_reflection", "golden", "snow", "winter_reflection", "cold-reflection", 0.08, 0.3, ["snow"], "lake", "winter tree reflection", ["water", "grass", "wood", "stone"]),
  jungle_waterfall_ruin: preset("jungle_waterfall_ruin", "day", "jungle_mist", "pictorial_nature", "mist-ruin", 0.2, 0.8, ["smoke", "fireflies"], "ruin", "jungle waterfall ruin", ["water", "grass", "ruinMatter", "stone", "crystal"]),
  desert_skyline: preset("desert_skyline", "golden", "desert_haze", "medioevo_archeopunk", "low-sun-haze", 0.1, 0.05, ["dust"], "wide", "desert skyline", ["soil", "stone", "gold", "dust"]),
  archeopunk_city_night: preset("archeopunk_city_night", "night", "fog", "medioevo_archeopunk", "signal-neon", 0.16, 0.35, ["smoke"], "wide", "archeopunk city night", ["obsidian", "gold", "neon", "ruinMatter"]),
  observatory_light_burst: preset("observatory_light_burst", "night", "clear", "cinematic_teal_amber", "signal-burst", 0.08, 0.1, ["fireflies"], "wide", "observatory burst", ["crystal", "neon", "stone", "gold"]),
  eye_color_study: preset("eye_color_study", "interior", "clear", "cinematic_teal_amber", "color-study", 0.02, 0.05, [], "interior", "eye color study", ["skin", "glass", "crystal", "cloth"]),
  wheatfield_cloudscape: preset("wheatfield_cloudscape", "day", "fog", "pictorial_nature", "soft-clouds", 0.08, 0.25, ["dust"], "wide", "wheatfield cloudscape", ["grass", "soil", "wood", "air"]),
};

export function getVibePreset(id: string): VibeSceneConfig {
  return VIBE_PRESETS[id] ?? VIBE_PRESETS.neon_rain_street;
}

function preset(
  id: string,
  timeOfDay: VibeSceneConfig["timeOfDay"],
  weather: VibeSceneConfig["weather"],
  palette: string,
  lightProfile: string,
  fog: number,
  wetness: number,
  particles: VibeSceneConfig["particles"],
  cameraPreset: VibeSceneConfig["cameraPreset"],
  mood: string,
  materials: VibeSceneConfig["materials"],
): VibeSceneConfig {
  return {
    id,
    source: "preset",
    prompt: id.replace(/_/g, " "),
    timeOfDay,
    weather,
    palette,
    lightProfile,
    fog,
    wetness,
    particles,
    cameraPreset,
    density: id.includes("city") || id.includes("street") ? 0.78 : 0.48,
    mood,
    materials,
    visualTags: [timeOfDay, weather, palette, lightProfile],
  };
}
