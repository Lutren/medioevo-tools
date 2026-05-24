import type { Agent } from "../core/types";
import { clamp, dist } from "../core/math";

const PROXIMITY_THRESHOLD = 2.5;

export function updateRelationships(agents: Agent[]): Agent[] {
  const updated = agents.map(a => ({ ...a, relationships: { ...a.relationships } }));

  for (let i = 0; i < updated.length; i++) {
    for (let j = i + 1; j < updated.length; j++) {
      const a = updated[i];
      const b = updated[j];
      const d = dist(a.x, a.y, b.x, b.y);

      if (d < PROXIMITY_THRESHOLD) {
        // Proximity increases relationships slightly
        const delta = 0.002 * (1 - d / PROXIMITY_THRESHOLD);
        updated[i].relationships[b.id] = clamp((updated[i].relationships[b.id] ?? 0) + delta, -1, 1);
        updated[j].relationships[a.id] = clamp((updated[j].relationships[a.id] ?? 0) + delta, -1, 1);
      }

      // Resource competition
      if (a.currentTaskId && b.currentTaskId && a.currentTaskId === b.currentTaskId) {
        updated[i].relationships[b.id] = clamp((updated[i].relationships[b.id] ?? 0) - 0.001, -1, 1);
        updated[j].relationships[a.id] = clamp((updated[j].relationships[a.id] ?? 0) - 0.001, -1, 1);
      }
    }
  }

  // Trust influences mood
  return updated.map(agent => {
    const rels = Object.values(agent.relationships);
    if (rels.length === 0) return agent;
    const avgRel = rels.reduce((s, r) => s + r, 0) / rels.length;
    const mood = clamp(agent.mood + avgRel * 0.001, 0, 1);
    const trust = clamp(agent.trust + avgRel * 0.0005, 0, 1);
    return { ...agent, mood, trust };
  });
}
