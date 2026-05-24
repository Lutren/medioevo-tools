import type { HarmonyKind, PaletteProfile, RGB } from "./colorTypes";
import { harmony } from "./harmony";

export const PALETTE_PROFILES: Record<string, PaletteProfile> = {
  cinematic_teal_amber: {
    id: "cinematic_teal_amber",
    name: "Cinematic teal/amber",
    colors: harmony({ r: 36, g: 178, b: 190 }, "cinematic-teal-amber"),
    tags: ["night", "neon", "cinema"],
    temperature: "mixed",
  },
  medioevo_archeopunk: {
    id: "medioevo_archeopunk",
    name: "MEDIOEVO archeopunk",
    colors: harmony({ r: 198, g: 151, b: 80 }, "medioevo-archeopunk"),
    tags: ["ruin", "bronze", "signal"],
    temperature: "mixed",
  },
  warm_interior: {
    id: "warm_interior",
    name: "Warm interior",
    colors: [
      { r: 42, g: 24, b: 18 },
      { r: 119, g: 61, b: 32 },
      { r: 220, g: 138, b: 73 },
      { r: 255, g: 211, b: 142 },
    ],
    tags: ["interior", "torch", "tavern"],
    temperature: "warm",
  },
  pictorial_nature: {
    id: "pictorial_nature",
    name: "Pictorial nature",
    colors: [
      { r: 24, g: 52, b: 44 },
      { r: 55, g: 115, b: 67 },
      { r: 132, g: 169, b: 92 },
      { r: 211, g: 190, b: 118 },
    ],
    tags: ["nature", "jungle", "water"],
    temperature: "mixed",
  },
  winter_reflection: {
    id: "winter_reflection",
    name: "Winter reflection",
    colors: [
      { r: 18, g: 32, b: 51 },
      { r: 73, g: 113, b: 145 },
      { r: 181, g: 210, b: 220 },
      { r: 242, g: 240, b: 220 },
    ],
    tags: ["winter", "reflection", "lake"],
    temperature: "cool",
  },
};

export function generatePalette(base: RGB, kind: HarmonyKind): PaletteProfile {
  return {
    id: kind,
    name: kind.replace(/-/g, " "),
    colors: harmony(base, kind),
    tags: [kind],
    temperature: kind.includes("amber") || kind.includes("archeopunk") ? "mixed" : "cool",
  };
}

export function getPaletteProfile(id: string): PaletteProfile {
  return PALETTE_PROFILES[id] ?? PALETTE_PROFILES.medioevo_archeopunk;
}

export function paletteToCss(profile: PaletteProfile): string[] {
  return profile.colors.map(c => `rgb(${c.r}, ${c.g}, ${c.b})`);
}
