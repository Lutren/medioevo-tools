import type { GameState, FrequencySource } from "./gameTypes";
import { FREQUENCIES } from "./frequencies";
import { absorbFrequency } from "./gameState";

export function getNearbyFrequencySource(game: GameState, playerX: number, playerY: number, radius: number): FrequencySource | undefined {
  return game.frequencySources.find(source => {
    const dx = source.position.x - playerX;
    const dy = source.position.y - playerY;
    return Math.sqrt(dx * dx + dy * dy) <= radius;
  });
}

export function interactWithFrequencySource(game: GameState, source: FrequencySource): void {
  const frequency = FREQUENCIES[source.frequencyName];
  if (frequency) {
    absorbFrequency(game, frequency);
  }
}
