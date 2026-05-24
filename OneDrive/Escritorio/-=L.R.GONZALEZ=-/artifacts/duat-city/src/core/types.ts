import type { PhysicsMetrics } from "../physics/types";
import type { GraphicsMetrics } from "../graphics/types";
import type { FieldMetrics, PhysicsFieldSummary } from "../physicsField/pixelTypes";
import type { QuaternaryStateSummary } from "../quaternary/types";
import type { PixelRealismMetrics } from "../pixelRealism/pixelRealismMetrics";
import type { PlayableSceneState } from "../scene/sceneTypes";

export type Mode = "CITY" | "AGENT" | "RPG" | "OSIT";
export type Gate = "APPROVE" | "REVIEW" | "BLOCK";
export type Regime = "OPTIMO" | "FUNCIONAL" | "CARGADO" | "SATURADO";
export type Direction = "EXPAND" | "HOLD" | "COMPRESS";
export type ClimateType = "temperate" | "arid" | "rainy" | "cold" | "tropical" | "industrial_smog";
export type GeographyType = "river_delta" | "mountain_gate" | "forest_edge" | "coastal_ruins" | "desert_crossing" | "dense_city";

export type TileType =
  | "empty"
  | "road"
  | "plaza"
  | "residential"
  | "workshop"
  | "archive"
  | "observatory"
  | "market"
  | "clinic"
  | "academy"
  | "theater"
  | "temple"
  | "garden"
  | "ruin"
  | "gatehouse"
  | "water"
  | "forest"
  | "stone"
  | "wall";

export type ResourceKey =
  | "food"
  | "materials"
  | "knowledge"
  | "trust"
  | "signal"
  | "energy"
  | "culture";

export interface FibmobData {
  mu: number;
  lodFactor: number;
  polarity: "positive" | "negative" | "void";
  rarity: number;
}

export interface Tile {
  id: number;
  x: number;
  y: number;
  type: TileType;
  buildingId?: string;
  zoneId?: string;
  fibmob: FibmobData;
  R: number;
  Phi_eff: number;
}

export interface Building {
  id: string;
  type: TileType;
  name: string;
  x: number;
  y: number;
  level: number;
  workers: string[];
  residents: string[];
  storage: Partial<Record<ResourceKey, number>>;
  R: number;
  Phi_eff: number;
  gate: Gate;
}

export interface AgentNeeds {
  energy: number;
  hunger: number;
  social: number;
  purpose: number;
  safety: number;
  curiosity: number;
}

export interface AgentLineagePerson {
  name: string;
  profession: string;
  originEra: string;
  formativeEvent: string;
}

export interface AgentLineage {
  schema: "duat.agent-lineage.v1";
  grandparents: [AgentLineagePerson, AgentLineagePerson];
  parents: [AgentLineagePerson, AgentLineagePerson];
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  x: number;
  y: number;
  homeId?: string;
  workplaceId?: string;
  currentTaskId?: string;
  needs: AgentNeeds;
  mood: number;
  trust: number;
  R: number;
  Phi_eff: number;
  gate: Gate;
  lineage: AgentLineage;
  originStory: string;
  skills: string[];
  memory: string[];
  relationships: Record<string, number>;
  inventory: Partial<Record<ResourceKey, number>>;
}

export interface ObjectDef {
  id: string;
  name: string;
  category: "rest" | "food" | "work" | "archive" | "health" | "learning" | "garden" | "ritual" | "ruin" | "gate";
  buildingTypes: TileType[];
  effects: Partial<Record<keyof AgentNeeds, number>> & {
    resource_delta?: Partial<Record<ResourceKey, number>>;
    R_delta?: number;
    Phi_delta?: number;
  };
  sprite: string;
}

export interface CityObject {
  id: string;
  defId: string;
  name: string;
  buildingId: string;
  x: number;
  y: number;
  occupiedBy?: string;
  R: number;
  Phi_eff: number;
}

export interface District {
  id: string;
  name: string;
  tileIds: number[];
  zoning: "mixed" | "residential" | "productive" | "civic" | "ruin" | "green";
  growth: number;
  maintenance: number;
  risk: number;
}

export interface CityContext {
  schema: "duat.city-context.v1";
  era: string;
  climate: ClimateType;
  geography: GeographyType;
  weather: "clear" | "rain" | "fog" | "storm" | "heatwave" | "ashfall";
  notes: string[];
}

export type TaskType =
  | "eat"
  | "rest"
  | "work"
  | "research"
  | "archive"
  | "heal"
  | "build"
  | "trade"
  | "teach"
  | "explore"
  | "quest"
  | "handoff";

export type TaskStatus = "pending" | "active" | "done" | "failed" | "blocked";

export interface Task {
  id: string;
  type: TaskType;
  title: string;
  agentId?: string;
  targetBuildingId?: string;
  targetTileId?: number;
  progress: number;
  status: TaskStatus;
  R_delta: number;
  Phi_delta: number;
  evidence: string[];
}

export type EventType = "need" | "task" | "building" | "resource" | "risk" | "rpg" | "system";

export interface CityEvent {
  id: string;
  tick: number;
  type: EventType;
  title: string;
  detail: string;
  R_delta: number;
  gate: Gate;
}

export interface WitnessEntry {
  id: string;
  tick: number;
  type: string;
  summary: string;
  evidence: string[];
  R: number;
  Phi_eff: number;
  gate: Gate;
}

export interface CityState {
  width: number;
  height: number;
  tick: number;
  tiles: Tile[];
  buildings: Building[];
  agents: Agent[];
  tasks: Task[];
  objects: CityObject[];
  districts: District[];
  context: CityContext;
  resources: Record<ResourceKey, number>;
  events: CityEvent[];
  witnesslog: WitnessEntry[];
  R: number;
  Phi_eff: number;
  regime: Regime;
  gate: Gate;
  physicsMetrics?: PhysicsMetrics;
  graphicsMetrics?: GraphicsMetrics;
  pixelRealism?: PixelRealismMetrics;
  fieldMetrics?: FieldMetrics;
  fieldSummary?: PhysicsFieldSummary;
  quaternary?: QuaternaryStateSummary;
  playableScene?: PlayableSceneState;
}

export interface Handoff {
  schema: string;
  tick: number;
  R: number;
  Phi_eff: number;
  regime: string;
  gate: string;
  city: {
    agents: number;
    buildings: number;
    resources: Record<ResourceKey, number>;
  };
  active_tasks: string[];
  risks: string[];
  rpg_export_ready: boolean;
  next_action: string;
  open_loops: string[];
  quaternary_timing?: {
    R: number;
    Phi_eff: number;
    gate: Gate;
    counts: QuaternaryStateSummary["counts"];
    avgFrequency: number;
    avgPermanence: number;
    avgStability: number;
    next_action: string;
  };
  pixel_realism?: PixelRealismMetrics;
  audio_gamefeel?: {
    enabled: boolean;
    R_audio: number;
    Phi_audio: number;
    cueCount: number;
    proceduralOnly: true;
    requiresUserGesture: true;
    externalSamplesCopied: false;
    publicationAllowed: false;
  };
}
