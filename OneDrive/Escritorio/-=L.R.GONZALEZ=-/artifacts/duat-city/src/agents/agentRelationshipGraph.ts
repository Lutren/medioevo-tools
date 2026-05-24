import type { Agent, CityState } from "../core/types";

export interface AgentRelationshipNode {
  id: string;
  name: string;
  role: string;
  x: number;
  y: number;
  R: number;
  Phi_eff: number;
  mood: number;
  criticalNeed: number;
  selected: boolean;
}

export interface AgentRelationshipEdge {
  from: string;
  to: string;
  weight: number;
  kind: "declared" | "proximity" | "task";
}

export interface AgentLifeDashboard {
  selectedAgentId?: string;
  selectedAgentName?: string;
  task: string;
  memory: string[];
  weakestNeed: string;
  weakestNeedValue: number;
  R: number;
  Phi_eff: number;
  mood: number;
  vibe: string;
  audioMoodTag: "calm" | "working" | "strained" | "blocked";
}

export interface AgentRelationshipGraph {
  schema: "duat/agent-life-graph/v1.3.1";
  nodes: AgentRelationshipNode[];
  edges: AgentRelationshipEdge[];
  dashboard: AgentLifeDashboard;
  metrics: {
    nodeCount: number;
    edgeCount: number;
    avgR: number;
    avgPhi: number;
    isolatedAgents: number;
    noNaN: boolean;
  };
}

export function buildAgentRelationshipGraph(state: CityState, selectedId?: string | null): AgentRelationshipGraph {
  const agents = state.agents.slice(0, 24);
  const nodes = agents.map(agent => toNode(agent, selectedId === agent.id));
  const declaredEdges = buildDeclaredEdges(agents);
  const proximityEdges = declaredEdges.length > 0 ? [] : buildProximityEdges(agents);
  const taskEdges = buildTaskEdges(agents);
  const edges = dedupeEdges([...declaredEdges, ...proximityEdges, ...taskEdges]).slice(0, 48);
  const selected = agents.find(agent => agent.id === selectedId) ?? agents[0];
  const avgR = average(nodes.map(node => node.R));
  const avgPhi = average(nodes.map(node => node.Phi_eff));
  const connected = new Set(edges.flatMap(edge => [edge.from, edge.to]));
  return {
    schema: "duat/agent-life-graph/v1.3.1",
    nodes,
    edges,
    dashboard: createAgentLifeDashboard(state, selected),
    metrics: {
      nodeCount: nodes.length,
      edgeCount: edges.length,
      avgR,
      avgPhi,
      isolatedAgents: nodes.filter(node => !connected.has(node.id)).length,
      noNaN: nodes.every(node => [node.x, node.y, node.R, node.Phi_eff, node.mood, node.criticalNeed].every(Number.isFinite))
        && edges.every(edge => Number.isFinite(edge.weight))
        && [avgR, avgPhi].every(Number.isFinite),
    },
  };
}

export function createAgentLifeDashboard(state: CityState, agent?: Agent): AgentLifeDashboard {
  if (!agent) {
    return {
      task: "none",
      memory: [],
      weakestNeed: "none",
      weakestNeedValue: 1,
      R: 0,
      Phi_eff: 1,
      mood: 1,
      vibe: state.playableScene?.activeVibe?.id ?? "none",
      audioMoodTag: "calm",
    };
  }
  const needs = Object.entries(agent.needs).sort((a, b) => a[1] - b[1]);
  const weakest = needs[0] ?? ["none", 1];
  const audioMoodTag = agent.gate === "BLOCK"
    ? "blocked"
    : agent.R > 0.34 || weakest[1] < 0.28
      ? "strained"
      : agent.currentTaskId
        ? "working"
        : "calm";
  return {
    selectedAgentId: agent.id,
    selectedAgentName: agent.name,
    task: agent.currentTaskId ?? "idle",
    memory: agent.memory.slice(-4),
    weakestNeed: weakest[0],
    weakestNeedValue: round3(weakest[1]),
    R: round3(agent.R),
    Phi_eff: round3(agent.Phi_eff),
    mood: round3(agent.mood),
    vibe: state.playableScene?.activeVibe?.id ?? "none",
    audioMoodTag,
  };
}

function toNode(agent: Agent, selected: boolean): AgentRelationshipNode {
  return {
    id: agent.id,
    name: agent.name,
    role: agent.role,
    x: round3(agent.x),
    y: round3(agent.y),
    R: round3(agent.R),
    Phi_eff: round3(agent.Phi_eff),
    mood: round3(agent.mood),
    criticalNeed: round3(Math.min(...Object.values(agent.needs))),
    selected,
  };
}

function buildDeclaredEdges(agents: Agent[]): AgentRelationshipEdge[] {
  const ids = new Set(agents.map(agent => agent.id));
  const edges: AgentRelationshipEdge[] = [];
  for (const agent of agents) {
    for (const [otherId, value] of Object.entries(agent.relationships)) {
      if (!ids.has(otherId) || Math.abs(value) < 0.05) continue;
      edges.push({ from: agent.id, to: otherId, weight: round3(value), kind: "declared" });
    }
  }
  return edges;
}

function buildProximityEdges(agents: Agent[]): AgentRelationshipEdge[] {
  const edges: AgentRelationshipEdge[] = [];
  for (const agent of agents) {
    const nearest = agents
      .filter(other => other.id !== agent.id)
      .map(other => ({ other, d: distance(agent, other) }))
      .sort((a, b) => a.d - b.d)[0];
    if (nearest && nearest.d <= 8) {
      edges.push({ from: agent.id, to: nearest.other.id, weight: round3(1 / Math.max(1, nearest.d)), kind: "proximity" });
    }
  }
  return edges;
}

function buildTaskEdges(agents: Agent[]): AgentRelationshipEdge[] {
  const byTask = new Map<string, Agent[]>();
  for (const agent of agents) {
    if (!agent.currentTaskId) continue;
    byTask.set(agent.currentTaskId, [...(byTask.get(agent.currentTaskId) ?? []), agent]);
  }
  const edges: AgentRelationshipEdge[] = [];
  for (const group of byTask.values()) {
    for (let i = 1; i < group.length; i++) {
      edges.push({ from: group[0].id, to: group[i].id, weight: 0.5, kind: "task" });
    }
  }
  return edges;
}

function dedupeEdges(edges: AgentRelationshipEdge[]): AgentRelationshipEdge[] {
  const byKey = new Map<string, AgentRelationshipEdge>();
  for (const edge of edges) {
    const key = [edge.from, edge.to].sort().join("::");
    const existing = byKey.get(key);
    if (!existing || Math.abs(edge.weight) > Math.abs(existing.weight)) byKey.set(key, edge);
  }
  return Array.from(byKey.values());
}

function distance(a: Agent, b: Agent): number {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function average(values: number[]): number {
  if (values.length === 0) return 0;
  return round3(values.reduce((sum, value) => sum + value, 0) / values.length);
}

function round3(value: number): number {
  return Number(Number.isFinite(value) ? value.toFixed(3) : "0");
}
