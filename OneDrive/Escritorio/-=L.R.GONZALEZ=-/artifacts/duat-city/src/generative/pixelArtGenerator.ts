import { getStyleProfile } from "../style/styleProfiles";

export interface PixelArtBitmap {
  width: number;
  height: number;
  seed: number;
  palette: string[];
  pixels: string[];
}

export function generatePixelArtBitmap(width: number, height: number, seed = 1, styleProfile = "archeopunk_city_rain", motif = "tile"): PixelArtBitmap {
  const profile = getStyleProfile(styleProfile);
  const rand = mulberry32(seed + hashString(motif) + profile.proceduralSeed);
  const palette = profile.palette;
  const pixels: string[] = [];
  for (let y = 0; y < height; y++) {
    let row = "";
    for (let x = 0; x < width; x++) {
      const edge = x === 0 || y === 0 || x === width - 1 || y === height - 1;
      const diagonal = Math.abs((x / Math.max(1, width)) - (y / Math.max(1, height))) < 0.08;
      const noise = rand();
      const index = edge ? 1 : diagonal ? 2 : Math.floor(noise * palette.length);
      row += String.fromCharCode(65 + (index % Math.min(26, palette.length)));
    }
    pixels.push(row);
  }
  return { width, height, seed, palette, pixels };
}

export function pixelArtHash(bitmap: PixelArtBitmap): string {
  return `${bitmap.width}x${bitmap.height}:${bitmap.seed}:${hashString(bitmap.pixels.join("|"))}`;
}

export function mulberry32(seed: number): () => number {
  let t = seed >>> 0;
  return () => {
    t += 0x6D2B79F5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

export function hashString(value: string): number {
  let hash = 2166136261;
  for (let i = 0; i < value.length; i++) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}
