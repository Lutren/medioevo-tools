import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { buildAgentRelationshipGraph, createAgentLifeDashboard } from "../agents/agentRelationshipGraph";

describe("agent life dashboard v1.3.1", () => {
  it("builds a finite relationship graph", () => {
    const city = createCity();
    const graph = buildAgentRelationshipGraph(city, city.agents[0]?.id);
    expect(graph.schema).toBe("duat/agent-life-graph/v1.3.1");
    expect(graph.nodes.length).toBeGreaterThan(0);
    expect(graph.edges.length).toBeGreaterThan(0);
    expect(graph.metrics.noNaN).toBe(true);
  });

  it("summarizes selected agent needs, task, memory and mood tag", () => {
    const city = createCity();
    const agent = { ...city.agents[0], currentTaskId: "task-test", memory: ["saw neon rain"], needs: { ...city.agents[0].needs, safety: 0.2 } };
    const dashboard = createAgentLifeDashboard(city, agent);
    expect(dashboard.selectedAgentName).toBe(agent.name);
    expect(dashboard.task).toBe("task-test");
    expect(dashboard.memory).toContain("saw neon rain");
    expect(dashboard.weakestNeed).toBe("safety");
    expect(["calm", "working", "strained", "blocked"]).toContain(dashboard.audioMoodTag);
  });
});
