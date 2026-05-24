import type { CityState } from "../core/types";
import type { AgentSimsView } from "./gameModeTypes";

export function selectAgentSimsView(state: CityState, agentId?: string): AgentSimsView {
  const agent = state.agents.find(a => a.id === agentId) ?? state.agents[0];
  if (!agent) {
    return { causalKnowledge: ["No agent selected."], decisionSuggestion: "Wait for a visible agent.", omniscienceBlocked: true };
  }
  const workplace = state.buildings.find(b => b.id === agent.workplaceId);
  const currentTask = state.tasks.find(task => task.id === agent.currentTaskId);
  const needs = Object.entries(agent.needs).sort((a, b) => a[1] - b[1])[0];
  return {
    agent,
    causalKnowledge: [
      `Agent knows current task: ${currentTask?.title ?? "none"}.`,
      `Agent remembers: ${agent.memory.slice(-1)[0] ?? "no recent memory"}.`,
      `Agent workplace signal: ${workplace?.name ?? "unknown locally"}.`,
    ],
    decisionSuggestion: needs && needs[1] < 0.35 ? `Route toward ${needs[0]} recovery.` : "Let the agent continue its current task.",
    omniscienceBlocked: true,
  };
}
