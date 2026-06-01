import type { GameState } from "./gameTypes";

export type DialogueNode = {
  id: string;
  speaker: string;
  text: string;
  options: { text: string; nextNodeId: string }[];
};

export class DialogueService {
  private activeDialogue: DialogueNode | null = null;

  startDialogue(startNode: DialogueNode): void {
    this.activeDialogue = startNode;
  }

  selectOption(optionIndex: number): void {
    if (this.activeDialogue && this.activeDialogue.options[optionIndex]) {
      // Transition logic would go here
      console.log("Option selected:", this.activeDialogue.options[optionIndex].text);
    }
  }

  getActiveNode(): DialogueNode | null {
    return this.activeDialogue;
  }
}
