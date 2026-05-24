import type { Agent } from "../core/types";
import type { PlayableSceneState } from "../scene/sceneTypes";

export function applyMaterialGameplayToAgents(agents: Agent[], scene: PlayableSceneState): Agent[] {
  const fireCells = new Set(scene.materials.filter(cell => cell.material === "fire").map(cell => `${cell.x},${cell.y}`));
  const waterCells = new Set(scene.materials.filter(cell => cell.material === "water").map(cell => `${cell.x},${cell.y}`));
  return agents.map(agent => {
    const key = `${Math.round(agent.x)},${Math.round(agent.y)}`;
    if (fireCells.has(key)) {
      return { ...agent, x: agent.x - 1, R: Math.min(1, agent.R + 0.08), memory: [...agent.memory.slice(-5), "Avoided fire hazard"] };
    }
    if (waterCells.has(key)) {
      return { ...agent, mood: Math.max(0, agent.mood - 0.02), Phi_eff: Math.max(0, agent.Phi_eff - 0.01) };
    }
    return agent;
  });
}
