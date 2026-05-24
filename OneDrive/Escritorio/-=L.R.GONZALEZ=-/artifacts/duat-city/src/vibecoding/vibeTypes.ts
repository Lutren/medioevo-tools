import type { PixelMaterial } from "../physicsField/pixelTypes";
import type { TimeOfDay, WeatherMode } from "../pixelRealism/renderPasses";
import type { LightCanonName, NarrativeLensId } from "../artDirection/artDirectionTypes";

export interface VibeSceneConfig {
  id: string;
  source: "preset" | "prompt";
  prompt: string;
  timeOfDay: TimeOfDay;
  weather: WeatherMode;
  palette: string;
  lightProfile: string;
  fog: number;
  wetness: number;
  particles: Array<"rain" | "snow" | "smoke" | "dust" | "fireflies" | "embers">;
  cameraPreset: "wide" | "street" | "interior" | "ruin" | "lake";
  density: number;
  mood: string;
  materials: PixelMaterial[];
  visualTags: string[];
  artDirection?: {
    lightCanon: LightCanonName;
    lightToken: string;
    narrativeLenses: NarrativeLensId[];
    narrativeTokens: string[];
    materialDetailProfile: string;
    moodTags: string[];
    publicBoundaryNote: string;
  };
}

export interface VibeCompileResult {
  config: VibeSceneConfig;
  warnings: string[];
  parsedIntent: string[];
  cloudUsed: false;
  externalApiUsed: false;
}
