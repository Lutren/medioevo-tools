import { parseVibeCommand } from "../vibecoding/vibeCommandParser";
import type { VibeLanguageAction } from "./languageTypes";

export function parseVibeCommandToGameAction(text: string): VibeLanguageAction {
  const parsed = parseVibeCommand(text);
  const intents = parsed.parsedIntent;
  const action: VibeLanguageAction["action"] =
    /exporta.*rpg/i.test(text) ? "export_rpg" :
      /guarda/i.test(text) ? "save_scene" :
        intents.some(intent => intent.startsWith("scene:")) ? "apply_vibe" :
          parsed.scenePatch.materials?.length ? "place_material" :
            parsed.scenePatch.lights?.length ? "place_light" :
              "unknown";
  return {
    parsedIntent: intents,
    action,
    confidence: action === "unknown" ? 0.2 : 0.82,
    cloudUsed: false,
    externalApiUsed: false,
  };
}
