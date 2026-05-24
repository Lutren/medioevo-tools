import type { StyleProfile } from "./styleTypes";

export const STYLE_PROFILES: Record<string, StyleProfile> = {
  duat_operational_terminal: profile("duat_operational_terminal", ["#091113", "#1bd4c2", "#d6b36a", "#233238"], ["operational", "diegetic-ui"], ["screen-glow"], ["obsidian", "brass"], 1201),
  archeopunk_city_rain: profile("archeopunk_city_rain", ["#10171b", "#5d6f75", "#b77a45", "#23d6e6", "#f0b35a"], ["rain", "city", "archeopunk"], ["side-neon", "wet-bounce"], ["wet_stone", "rain_wet_metal"], 1202),
  forbidden_archive: profile("forbidden_archive", ["#0d1117", "#24465a", "#9b7a3f", "#d7c28a"], ["archive", "forbidden", "mythic"], ["window-slit", "dust"], ["old_paper_archive_tablet", "aged_brass"], 1203),
  central_forge: profile("central_forge", ["#17100c", "#ff7a2f", "#b46a32", "#6d7782"], ["forge", "fire", "work"], ["fire-core", "ember"], ["burnished_copper", "carbonized_wood"], 1204),
  biomechanical_garden: profile("biomechanical_garden", ["#0c1711", "#38d9a9", "#587a46", "#7b748f"], ["garden", "bioluminescent", "organic-machine"], ["algae-glow"], ["bioluminescent_algae", "moss_organic_membrane"], 1205),
  underground_market: profile("underground_market", ["#120d16", "#ff6ec7", "#22e8ff", "#ffb23f"], ["market", "smoke", "crowd"], ["pink-neon", "amber-fire"], ["rain_wet_metal", "ritual_amber"], 1206),
  neon_rain_street: profile("neon_rain_street", ["#071015", "#22e8ff", "#ffb45c", "#586068"], ["night", "rain", "neon"], ["cyan-neon", "water-reflection"], ["wet_stone", "rain_wet_metal"], 1207),
  warm_interior_tavern: profile("warm_interior_tavern", ["#1b120c", "#ffd79a", "#9b5a34", "#40535a"], ["interior", "warm", "conversation"], ["window-soft", "torch"], ["aged_brass", "carbonized_wood"], 1208),
  wet_isometric_city: profile("wet_isometric_city", ["#11181c", "#586068", "#b46a32", "#22e8ff"], ["isometric", "wet", "city"], ["wet-bounce"], ["wet_stone", "burnished_copper"], 1209),
  qstate_debug_glyphs: profile("qstate_debug_glyphs", ["#05080a", "#44ff99", "#ffee66", "#ff5577", "#66aaff"], ["debug", "qstate", "glyphs"], ["flat-diagnostic"], ["obsidian_glass"], 1210),
};

export function getStyleProfile(id: string): StyleProfile {
  return STYLE_PROFILES[id] ?? STYLE_PROFILES.archeopunk_city_rain;
}

export function listStyleProfiles(): StyleProfile[] {
  return Object.values(STYLE_PROFILES);
}

function profile(id: string, palette: string[], moodTags: string[], lightTags: string[], materialBias: string[], proceduralSeed: number): StyleProfile {
  return { id, palette, moodTags, lightTags, materialBias, proceduralSeed };
}
