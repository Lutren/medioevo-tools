import type { GameState } from "./gameTypes";

export function saveGameState(game: GameState): string {
  return JSON.stringify(game, null, 2);
}

export function loadGameState(json: string): GameState | undefined {
  try {
    const parsed = JSON.parse(json) as GameState;
    if (parsed.schema !== "duat.game_state.v1_2") return undefined;
    return parsed;
  } catch {
    return undefined;
  }
}
