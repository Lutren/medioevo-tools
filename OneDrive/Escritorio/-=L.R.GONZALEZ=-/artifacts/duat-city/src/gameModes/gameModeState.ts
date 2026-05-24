import type { GameModeId, GameModeState } from "./gameModeTypes";

export function createGameModeState(activeMode: GameModeId = "duat_interface"): GameModeState {
  return {
    schema: "duat/game-mode-state/v1.3",
    activeMode,
    zoom: 1,
    observerOnly: activeMode === "hormiguero",
    activeEra: "duat_epoch",
    eraSecretUnlocked: false,
    policies: {},
    resourcesDelta: {},
    arena: { active: false, factions: ["archive", "forge"], score: { archive: 0, forge: 0 } },
    rpg: { currentLayer: "city_isometric" },
    gate: "APPROVE",
    notes: ["Game OS mode state is local and serializable."],
  };
}

export function cloneGameModeState(state: GameModeState): GameModeState {
  return JSON.parse(JSON.stringify(state)) as GameModeState;
}
