import type { GameState } from "../game/gameTypes";

/**
 * BioAgent simulates small life forms (like crickets) 
 * that act as environmental diagnostic tools.
 */
export interface BioAgent {
  id: string;
  type: "cricket";
  position: { x: number; y: number };
  frequency: number; // Hz, derived from local temp
}

export function updateBioAgent(agent: BioAgent, localTemp: number): void {
  // Cricket frequency increases with temperature (Arrhenius-like relation)
  agent.frequency = 10 + (localTemp * 0.5); 
}

export function getEnvironmentalReport(agent: BioAgent): string {
  if (agent.frequency > 40) return "High activity: Environment is warm.";
  if (agent.frequency < 20) return "Low activity: Environment is cold.";
  return "Stable activity.";
}
