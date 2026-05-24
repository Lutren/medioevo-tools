import type { NarrativeLensId, SymbolicObject } from "./artDirectionTypes";

const BASE_SYMBOLS: Array<Omit<SymbolicObject, "id">> = [
  { label: "sealed witness lamp", material: "aged_brass", meaning: "testimony held behind a gate", placement: "foreground" },
  { label: "obsidian rain basin", material: "obsidian_glass", meaning: "reflection that may not be true", placement: "midground" },
  { label: "archive tablet", material: "old_paper_archive_tablet", meaning: "memory made operational", placement: "ui" },
  { label: "patinated key", material: "patinated_bronze", meaning: "permission and debt", placement: "inventory" },
  { label: "smoked crystal eye", material: "smoked_crystal", meaning: "broken perception", placement: "midground" },
  { label: "ritual amber shard", material: "ritual_amber", meaning: "warmth under judgement", placement: "foreground" },
  { label: "wet metal gutter", material: "rain_wet_metal", meaning: "city residue channel", placement: "foreground" },
  { label: "carbonized door beam", material: "carbonized_wood", meaning: "choice after damage", placement: "midground" },
  { label: "moss membrane seal", material: "moss_organic_membrane", meaning: "nature reclaiming protocol", placement: "background" },
  { label: "copper signal wire", material: "burnished_copper", meaning: "causal line across districts", placement: "background" },
  { label: "brass tube meter", material: "aged_brass", meaning: "measured duty", placement: "ui" },
  { label: "bioluminescent algae trace", material: "bioluminescent_algae", meaning: "life under archive stone", placement: "midground" },
  { label: "wet stone threshold", material: "wet_stone", meaning: "crossing into review", placement: "foreground" },
];

export function generateSymbolicObjects(lenses: NarrativeLensId[] = ["mythic_archive_lens"], count = 13): SymbolicObject[] {
  const safeCount = Math.max(1, Math.min(13, Math.floor(count)));
  return BASE_SYMBOLS.slice(0, safeCount).map((symbol, index) => ({
    ...symbol,
    id: `symbolic-object-${index + 1}`,
    lens: lenses[index % Math.max(1, lenses.length)],
  }));
}
