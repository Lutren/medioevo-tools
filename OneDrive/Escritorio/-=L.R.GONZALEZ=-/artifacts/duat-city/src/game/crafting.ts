import type { GameState } from "./gameTypes";

export function addMaterial(game: GameState, materialName: string, quantity: number): void {
  const existing = game.inventory.find(m => m.name === materialName);
  if (existing) {
    existing.quantity += quantity;
  } else {
    game.inventory.push({ name: materialName, quantity });
  }
}

export function hasMaterials(game: GameState, requirements: Record<string, number>): boolean {
  return Object.entries(requirements).every(([name, qty]) => {
    const item = game.inventory.find(m => m.name === name);
    return item !== undefined && item.quantity >= qty;
  });
}

export function craftItem(game: GameState, requirements: Record<string, number>, resultItemName: string): boolean {
  if (!hasMaterials(game, requirements)) return false;

  Object.entries(requirements).forEach(([name, qty]) => {
    const item = game.inventory.find(m => m.name === name)!;
    item.quantity -= qty;
  });

  addMaterial(game, resultItemName, 1);
  return true;
}
