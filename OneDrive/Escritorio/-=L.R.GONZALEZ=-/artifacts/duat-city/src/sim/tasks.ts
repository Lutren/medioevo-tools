import type { Task, Agent, Building } from "../core/types";
import { uid, pick, seededRandom, type RandomSource } from "../core/math";

const EVIDENCE_POOL: Record<string, string[]> = {
  eat: ["Agent restored hunger", "Food consumed from market", "Social interaction at market"],
  rest: ["Agent recovered energy", "Residential rest cycle completed", "Sleep pattern normal"],
  work: ["Materials produced", "Work task completed", "Production quota met"],
  research: ["Knowledge archived", "Research entry logged", "Discovery catalogued"],
  archive: ["Handoff document created", "Evidence stored", "Archive entry v{tick} added"],
  heal: ["Health restored", "Clinic treatment completed", "Safety restored"],
  build: ["Structure reinforced", "Build task complete", "Materials consumed"],
  trade: ["Trade completed", "Resources exchanged", "Market equilibrium maintained"],
  teach: ["Teaching session done", "Knowledge transferred", "Curriculum module completed"],
  explore: ["Zone explored", "Signal detected", "Anomaly logged"],
  quest: ["Quest progress", "Encounter resolved", "RPG hook generated"],
  handoff: ["Handoff JSON exported", "DUAT state serialized", "Open loops logged"],
};

export function createTask(
  type: Task["type"],
  agentId: string,
  targetBuildingId?: string,
  targetTileId?: number,
  rng?: RandomSource
): Task {
  const labels: Record<Task["type"], string> = {
    eat: "Find food",
    rest: "Rest",
    work: "Work",
    research: "Research",
    archive: "Archive data",
    heal: "Heal",
    build: "Build",
    trade: "Trade",
    teach: "Teach",
    explore: "Explore",
    quest: "Quest",
    handoff: "Export handoff",
  };
  return {
    id: uid(rng),
    type,
    title: labels[type],
    agentId,
    targetBuildingId,
    targetTileId,
    progress: 0,
    status: "pending",
    R_delta: -0.03,
    Phi_delta: 0.02,
    evidence: [],
  };
}

export function stepTask(
  task: Task,
  agent: Agent,
  building: Building | undefined,
  tick: number,
  rng?: RandomSource
): { task: Task; done: boolean } {
  if (task.status !== "active") return { task, done: false };
  const random = rng ?? seededRandom(`task:${tick}:${task.id}:${agent.id}`);

  const speed = agent.gate === "BLOCK" ? 0.002 : agent.gate === "REVIEW" ? 0.006 : 0.012;
  const newProgress = Math.min(1, task.progress + speed);

  if (newProgress >= 1) {
    const pool = EVIDENCE_POOL[task.type] ?? ["Task completed"];
    const evidence = pick(pool, random).replace("{tick}", String(tick));
    return {
      task: { ...task, progress: 1, status: "done", evidence: [...task.evidence, evidence] },
      done: true,
    };
  }

  // Random failure at low completion when blocked
  if (agent.gate === "BLOCK" && random() < 0.002) {
    return { task: { ...task, status: "failed" }, done: true };
  }

  return { task: { ...task, progress: newProgress }, done: false };
}

export function activateTask(task: Task): Task {
  return { ...task, status: "active" };
}

export function blockTask(task: Task): Task {
  return { ...task, status: "blocked" };
}

export function getActiveTaskForAgent(tasks: Task[], agentId: string): Task | undefined {
  return tasks.find(t => t.agentId === agentId && (t.status === "active" || t.status === "pending"));
}

export function cleanupTasks(tasks: Task[]): Task[] {
  // Keep pending/active + last 50 done/failed
  const live = tasks.filter(t => t.status === "pending" || t.status === "active");
  const finished = tasks.filter(t => t.status === "done" || t.status === "failed").slice(-50);
  const blocked = tasks.filter(t => t.status === "blocked");
  return [...live, ...finished, ...blocked];
}
