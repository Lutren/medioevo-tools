export type LightCanonName =
  | "balanced_medioevo"
  | "caravaggio_chiaroscuro"
  | "vermeer_interior_light"
  | "van_eyck_detail_light";

export interface LightCanonProfile {
  name: LightCanonName;
  publicToken: string;
  contrast: number;
  backgroundDarkness: number;
  lateralLight: number;
  shadowDepth: number;
  interiorSoftness: number;
  detailBoost: number;
  reflectionBoost: number;
  uses: string[];
}

export interface ArtDirectedScene {
  lightProfile?: string;
  contrast?: number;
  backgroundDarkness?: number;
  shadowStrength?: number;
  detailDensity?: number;
  materialReflection?: number;
  atmosphere?: number;
  moodTags?: string[];
  [key: string]: unknown;
}

export interface MaterialDetailProfile {
  id: string;
  baseColor: string;
  roughness: number;
  reflectance: number;
  opacity: number;
  emissive: number;
  wetnessResponse: number;
  detailDensity: number;
  symbolicWeight: number;
}

export interface CompositionRule {
  id: string;
  layer: "foreground" | "midground" | "background" | "reading_path" | "hierarchy";
  description: string;
  weight: number;
}

export type NarrativeLensId =
  | "systems_logic_lens"
  | "moral_conflict_lens"
  | "stoic_duty_lens"
  | "surveillance_dystopia_lens"
  | "perception_break_lens"
  | "mythic_archive_lens"
  | "absurd_trial_lens"
  | "will_and_void_lens"
  | "knowledge_dialogue_lens"
  | "power_knowledge_lens";

export interface NarrativeLens {
  id: NarrativeLensId;
  internalToken: string;
  themes: string[];
  uses: string[];
  publicBoundaryNote: string;
}

export interface CompiledNarrativeLens {
  id: NarrativeLensId;
  internalToken: string;
  moodTags: string[];
  questTone: string;
  publicBoundaryNote: string;
}

export interface SceneMoodCompileResult {
  lightCanon: LightCanonName;
  lightToken: string;
  narrativeLenses: NarrativeLensId[];
  narrativeTokens: string[];
  moodTags: string[];
  materialDetailProfile: string;
  warnings: string[];
  parsedIntent: string[];
  publicBoundaryNote: string;
}

export interface SymbolicObject {
  id: string;
  label: string;
  material: string;
  meaning: string;
  placement: "foreground" | "midground" | "background" | "ui" | "inventory";
  lens?: NarrativeLensId;
}
