import type { CityState, Gate } from "../core/types";
import type { GameModeState } from "../gameModes/gameModeTypes";
import type { LanguageMetrics } from "../language/languageTypes";
import type { AudioGameFeelSnapshot } from "../audio/audioTypes";
import type { OSITFormulaProfile } from "../osit/ositTypes";

export interface BrainSystemStatus {
  id: string;
  active: boolean;
  R: number;
  Phi_eff: number;
  gate: Gate;
  notes: string[];
}

export interface BrainRuntime {
  schema: "duat/brain-runtime/v1.3";
  tick: number;
  systems: {
    hippocampus: BrainSystemStatus;
    prefrontal: BrainSystemStatus;
    attention: BrainSystemStatus;
    crossModal: BrainSystemStatus;
    truthGate: BrainSystemStatus;
    languageCortex: BrainSystemStatus;
    audioGameFeel: BrainSystemStatus;
    ositFormulaLab: BrainSystemStatus;
    affect: BrainSystemStatus;
    social: BrainSystemStatus;
    cerebellum: BrainSystemStatus;
    residueDream: BrainSystemStatus;
    goalAlignment: BrainSystemStatus;
  };
  handoff: object;
  gameMode?: GameModeState;
  languageMetrics?: LanguageMetrics;
  audioGameFeel?: AudioGameFeelSnapshot;
  ositFormulaProfile?: OSITFormulaProfile;
  executionAllowed: false;
}

export interface BrainRuntimeInput {
  city: CityState;
  gameMode?: GameModeState;
  languageMetrics?: LanguageMetrics;
  audioGameFeel?: AudioGameFeelSnapshot;
  ositFormulaProfile?: OSITFormulaProfile;
}
