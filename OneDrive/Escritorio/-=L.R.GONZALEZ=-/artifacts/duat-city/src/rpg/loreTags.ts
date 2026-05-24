import type { Tile } from "../core/types";

export function getLoreTag(tile: Tile): string {
  if (tile.fibmob.polarity === "void") {
    return tile.type === "ruin" ? "ruin-void-anomaly" : "void-saturation";
  }
  if (tile.fibmob.polarity === "negative") return "conflict-inversion";
  if (tile.type === "archive") return "knowledge-stable";
  if (tile.type === "observatory") return "signal-order";
  if (tile.type === "ruin") return "ruin-anomaly";
  if (tile.type === "garden") return "nature-renewal";
  if (tile.type === "market") return "trade-equilibrium";
  if (tile.type === "residential") return "community-order";
  return "stable-zone";
}

export function getRarityLabel(rarity: number): string {
  if (rarity < 0.01) return "legendary";
  if (rarity < 0.05) return "rare";
  if (rarity < 0.15) return "uncommon";
  return "common";
}
