import { parseVibeCommand } from "../vibecoding/vibeCommandParser";
import { tickGame } from "./gameLoop";
import { createGameState } from "./gameState";
import type { GameState } from "./gameTypes";

export function createGameSceneFromCommand(command: string): GameState {
  const game = createGameState();
  return tickGame(game, parseVibeCommand(command));
}
