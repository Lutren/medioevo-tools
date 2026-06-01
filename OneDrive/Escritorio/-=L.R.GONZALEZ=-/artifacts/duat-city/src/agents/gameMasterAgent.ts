import type { GameState } from "../game/gameTypes";
import { GEO_CONFIG } from "../core/geoConfig";

export type Quest = {
  id: string;
  title: string;
  description: string;
  targetPlane: string;
  completed: boolean;
};

export class GameMasterAgent {
  private quests: Quest[] = [];

  constructor() {
    this.quests.push({
      id: "q1",
      title: "Exploración Astral",
      description: "Llega a Ciudad Central en el Plano Astral.",
      targetPlane: "astral",
      completed: false,
    });
  }

  updateQuests(game: GameState): void {
    const currentPlane = game.context.activePlane;
    this.quests.forEach(q => {
      if (!q.completed && q.targetPlane === currentPlane) {
        q.completed = true;
        console.log(`Quest Completed: ${q.title} in plane ${currentPlane}`);
      }
    });
  }
}
