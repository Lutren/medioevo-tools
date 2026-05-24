import type { Agent, CityState, Gate, ResourceKey, TileType } from "../core/types";

export type GameModeId =
  | "duat_interface"
  | "hormiguero"
  | "agent_sims"
  | "city_president"
  | "era_progression"
  | "vs_arena"
  | "rpg"
  | "metroidvania";

export type EraId =
  | "unicellularidad"
  | "multicelularidad"
  | "prehistoria"
  | "primeros_cavernicolas"
  | "agricultura"
  | "ciudad_antigua"
  | "medieval"
  | "industrial"
  | "cyber_archeopunk"
  | "duat_epoch";

export interface GameModeDefinition {
  id: GameModeId;
  label: string;
  camera: "control_room" | "observer_zoom" | "follow_agent" | "city_policy" | "side_view" | "arena" | "isometric";
  directAgentControl: boolean;
  description: string;
}

export interface HeatmapMetric {
  id: string;
  x: number;
  y: number;
  R: number;
  Phi_eff: number;
  qState: "00" | "01" | "10" | "11";
}

export interface GameModeState {
  schema: "duat/game-mode-state/v1.3";
  activeMode: GameModeId;
  previousMode?: GameModeId;
  selectedAgentId?: string;
  followedAgentId?: string;
  zoom: number;
  observerOnly: boolean;
  activeEra: EraId;
  eraSecretUnlocked: boolean;
  policies: Record<string, number>;
  resourcesDelta: Partial<Record<ResourceKey, number>>;
  arena: {
    active: boolean;
    factions: string[];
    score: Record<string, number>;
  };
  rpg: {
    currentLayer: "city_isometric" | "metroidvania";
    activeQuestId?: string;
    transitionGate?: string;
  };
  gate: Gate;
  notes: string[];
}

export interface AgentSimsView {
  agent?: Agent;
  causalKnowledge: string[];
  decisionSuggestion: string;
  omniscienceBlocked: true;
}

export interface CityPolicyPatch {
  policy: "housing" | "food" | "knowledge" | "safety" | "signal";
  delta: number;
}

export interface EraDefinition {
  id: EraId;
  label: string;
  materialBias: TileType[];
  languageTone: string;
  audioMotif: string;
  lightProfile: string;
  questBias: string[];
  uiSkin: string;
}
