import type { GameState } from "./gameTypes";
import { FREQUENCIES } from "./frequencies";
import { absorbFrequency, triggerFrequency } from "./gameState";

/**
 * Functional hook for player to try and absorb a frequency from an environmental source.
 */
export function attemptAbsorption(game: GameState, frequencyKey: keyof typeof FREQUENCIES): void {
  const frequency = FREQUENCIES[frequencyKey];
  if (frequency) {
    absorbFrequency(game, frequency);
  }
}

/**
 * Functional hook for player to trigger an absorbed frequency.
 */
export function attemptTrigger(game: GameState, frequencyKey: keyof typeof FREQUENCIES): boolean {
  const frequency = FREQUENCIES[frequencyKey];
  if (frequency) {
    return triggerFrequency(game, frequency.name);
  }
  return false;
}
