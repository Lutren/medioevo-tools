import type { CompositionRule, NarrativeLensId, SymbolicObject } from "./artDirectionTypes";
import { generateSymbolicObjects } from "./symbolicObjectGrammar";

export const COMPOSITION_RULES: CompositionRule[] = [
  { id: "foreground_frame", layer: "foreground", description: "Use pipes, arches, branches, doors or UI frames to anchor the first read.", weight: 0.78 },
  { id: "midground_action", layer: "midground", description: "Keep agents, machines, rituals or buildings in the clearest action band.", weight: 0.84 },
  { id: "background_depth", layer: "background", description: "Reserve towers, city rain, mist and ruins for scale and historical pressure.", weight: 0.72 },
  { id: "light_path", layer: "reading_path", description: "Light should guide attention before UI labels do.", weight: 0.9 },
  { id: "symbolic_object_13", layer: "hierarchy", description: "Each authored scene can carry thirteen symbolic objects without equal saturation.", weight: 0.66 },
  { id: "hierarchy_not_all_equal", layer: "hierarchy", description: "Avoid giving every surface maximum contrast, glow and detail.", weight: 0.88 },
];

export interface CompositionPlan {
  rules: CompositionRule[];
  symbolicObjects: SymbolicObject[];
  saturationBudget: number;
  readingPath: string[];
}

export function buildCompositionPlan(lenses: NarrativeLensId[] = ["mythic_archive_lens"]): CompositionPlan {
  return {
    rules: COMPOSITION_RULES,
    symbolicObjects: generateSymbolicObjects(lenses, 13),
    saturationBudget: 0.68,
    readingPath: ["foreground_frame", "symbolic_object", "midground_action", "light_path", "background_depth"],
  };
}
