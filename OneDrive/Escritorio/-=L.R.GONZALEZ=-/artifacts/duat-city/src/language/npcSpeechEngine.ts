import type { CityState } from "../core/types";
import { compileEpistemicStatement, languageGate } from "./epistemicDialogue";
import type { AgentLike, NpcUtterance } from "./languageTypes";

export function generateNpcUtterance(agent: AgentLike, worldState: CityState, mode = "duat_interface"): NpcUtterance {
  const task = worldState.tasks.find(item => item.id === agent.currentTaskId);
  const memory = agent.memory.slice(-1)[0];
  const evidence = [
    `agent:${agent.id}`,
    task ? `task:${task.id}` : "",
    memory ? "memory:recent" : "",
  ].filter(Boolean);
  const base = compileEpistemicStatement(
    `${agent.name} reports from ${agent.role}: ${task ? task.title : "no active task"}. ${memory ? `Last memory: ${memory}.` : "Memory is locally empty."}`,
    evidence,
  );
  const gated = languageGate(base);
  return {
    ...gated,
    agentId: agent.id,
    role: agent.role,
    mood: finite(agent.mood),
    mode,
  };
}

function finite(value: number): number {
  return Number.isFinite(value) ? Number(value.toFixed(3)) : 0;
}
