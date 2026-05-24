import type { Agent } from "../core/types";
import type { RPGQuest } from "../rpg/rpgTypes";
import { compileEpistemicStatement } from "./epistemicDialogue";
import type { QuestDialogue } from "./languageTypes";

export function generateQuestDialogue(quest: RPGQuest, lens: string, agent?: Agent): QuestDialogue {
  const speaker = agent ? `${agent.name} (${agent.role})` : "DUAT narrator";
  return {
    questId: quest.id,
    lens,
    lines: [
      compileEpistemicStatement(`${speaker}: ${quest.hook}`, [`quest:${quest.id}`]),
      compileEpistemicStatement(`Reward forecast: ${quest.reward}`, [`quest:${quest.id}:reward`]),
      compileEpistemicStatement(`Unknown outcome remains gated by player evidence?`),
    ],
  };
}
