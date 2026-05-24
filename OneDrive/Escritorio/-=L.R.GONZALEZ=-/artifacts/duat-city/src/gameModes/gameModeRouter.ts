import type { CityState } from "../core/types";
import type { GameModeDefinition, GameModeId, GameModeState } from "./gameModeTypes";
import { createGameModeState } from "./gameModeState";

export const GAME_MODE_DEFINITIONS: GameModeDefinition[] = [
  { id: "duat_interface", label: "DUAT Interface", camera: "control_room", directAgentControl: false, description: "Central OSIT, agents, gates, witnesslog and handoff surface." },
  { id: "hormiguero", label: "Hormiguero", camera: "observer_zoom", directAgentControl: false, description: "Observer-only macro view with task routes, R/Phi and Q-state heatmaps." },
  { id: "agent_sims", label: "Agent Sims", camera: "follow_agent", directAgentControl: false, description: "Follow one agent, inspect needs, task, memory, gate and causal limits." },
  { id: "city_president", label: "City President", camera: "city_policy", directAgentControl: false, description: "Control city policy, zones, resources and buildings indirectly." },
  { id: "era_progression", label: "Era Progression", camera: "observer_zoom", directAgentControl: false, description: "Fictional evolutionary game mode that changes materials, language, audio, light and quests." },
  { id: "vs_arena", label: "VS Arena", camera: "arena", directAgentControl: true, description: "Original 2D/2.5D arena prototype using DUAT materials and light." },
  { id: "rpg", label: "RPG", camera: "isometric", directAgentControl: true, description: "Isometric city RPG with NPCs, factions, quests and dialogue." },
  { id: "metroidvania", label: "Metroidvania", camera: "side_view", directAgentControl: true, description: "Side-view exploration layer connected to city gates and quests." },
];

export function getGameModeDefinition(id: GameModeId): GameModeDefinition {
  return GAME_MODE_DEFINITIONS.find(mode => mode.id === id) ?? GAME_MODE_DEFINITIONS[0];
}

export function listGameModes(): GameModeDefinition[] {
  return [...GAME_MODE_DEFINITIONS];
}

export function switchGameMode(current: GameModeState | undefined, nextMode: GameModeId, city?: CityState): GameModeState {
  const base = current ? { ...current } : createGameModeState();
  const definition = getGameModeDefinition(nextMode);
  const selectedAgentId = base.selectedAgentId ?? city?.agents[0]?.id;
  return {
    ...base,
    previousMode: base.activeMode,
    activeMode: nextMode,
    selectedAgentId: nextMode === "agent_sims" ? selectedAgentId : base.selectedAgentId,
    followedAgentId: nextMode === "agent_sims" ? selectedAgentId : base.followedAgentId,
    observerOnly: !definition.directAgentControl && nextMode === "hormiguero",
    zoom: zoomForMode(nextMode),
    arena: nextMode === "vs_arena" ? { ...base.arena, active: true } : { ...base.arena, active: false },
    rpg: nextMode === "metroidvania"
      ? { ...base.rpg, currentLayer: "metroidvania" }
      : nextMode === "rpg"
        ? { ...base.rpg, currentLayer: "city_isometric" }
        : base.rpg,
    notes: [...base.notes, `Switched to ${definition.label}`].slice(-12),
  };
}

export function zoomForMode(mode: GameModeId): number {
  switch (mode) {
    case "hormiguero": return 0.42;
    case "agent_sims": return 2.4;
    case "city_president": return 0.9;
    case "vs_arena": return 1.7;
    case "metroidvania": return 1.8;
    case "rpg": return 1.35;
    case "era_progression": return 0.75;
    default: return 1;
  }
}

export function assertFiniteGameModeState(state: GameModeState): boolean {
  return [state.zoom, ...Object.values(state.policies), ...Object.values(state.resourcesDelta), ...Object.values(state.arena.score)].every(Number.isFinite);
}
