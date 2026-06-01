import type { CityState } from "../core/types";
import type { PlayableSceneState } from "../scene/sceneTypes";
import type { VibeCommandParseResult } from "../vibecoding/vibeCommandParser";
import type { AudioGameFeelSnapshot } from "../audio/audioTypes";

export type FrequencyType = {
  name: string;
  hz: number;
  effect: string;
  costPsi: number;
};

export type FrequencySource = {
  id: string;
  frequencyName: string;
  position: { x: number; y: number };
};

export type CraftingMaterial = {
  name: string;
  quantity: number;
};

export interface GameState {
  schema: "duat.game_state.v1_2";
  scene: PlayableSceneState;
  city: CityState;
  actors: CityState["agents"];
  quests: string[];
  resources: CityState["resources"];
  camera: { x: number; y: number; zoom: number };
  time: number;
  weather: PlayableSceneState["weather"];
  ositMetrics: {
    R_material: number;
    Phi_material: number;
    R_light: number;
    Phi_light: number;
    activeCells: number;
    skippedCells: number;
    materialEvents: number;
  };
  audioGameFeel: AudioGameFeelSnapshot;
  vibeHistory: VibeCommandParseResult[];
  handoff: object;
  coherencePsi: number;
  activeFrequencies: FrequencyType[];
  absorbedFrequencies: Record<string, FrequencyType>;
  frequencySources: FrequencySource[];
  inventory: CraftingMaterial[];
}
