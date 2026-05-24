import type { Agent, CityEvent, CityState, Gate } from "../core/types";
import type { NarrativeLensId } from "../artDirection/artDirectionTypes";

export type EpistemicClass = "CERTEZA" | "INFERENCIA" | "INCOGNITA" | "BLOQUEO";

export interface EpistemicStatement {
  classification: EpistemicClass;
  text: string;
  evidence: string[];
  unsupportedClaims: number;
  gate: Gate;
}

export interface LanguageMetrics {
  R_language: number;
  Phi_language: number;
  ambiguity: number;
  unsupported_claims: number;
  repetition: number;
  narrative_coherence: number;
}

export interface NpcUtterance extends EpistemicStatement {
  agentId: string;
  role: string;
  mood: number;
  mode: string;
}

export interface QuestDialogue {
  questId: string;
  lens: NarrativeLensId | string;
  lines: EpistemicStatement[];
}

export interface SourceCard {
  schema: "duat/source-card/v1.3";
  id: string;
  title: string;
  eventType: string;
  evidence: string[];
  R: number;
  Phi_eff: number;
  gate: Gate;
}

export interface LanguageWorldState {
  city: CityState;
  recentEvents?: CityEvent[];
}

export interface VibeLanguageAction {
  parsedIntent: string[];
  action: "apply_vibe" | "place_material" | "place_light" | "switch_mode" | "export_rpg" | "save_scene" | "unknown";
  confidence: number;
  cloudUsed: false;
  externalApiUsed: false;
}

export type AgentLike = Pick<Agent, "id" | "name" | "role" | "mood" | "R" | "Phi_eff" | "gate" | "memory" | "currentTaskId">;
