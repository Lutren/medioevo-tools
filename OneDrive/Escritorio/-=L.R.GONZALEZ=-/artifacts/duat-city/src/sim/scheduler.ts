import type { Task, CityState } from "../core/types";
import { pick, uid, type RandomSource } from "../core/math";
import { assessNeeds, createTaskForNeed } from "./needs";
import { getActiveTaskForAgent } from "./tasks";
import { findNearestBuilding } from "./agents";
import { createLifeTaskForAgent } from "./agentLife";

export function scheduleTasks(state: CityState, rng?: RandomSource): CityState {
  let tasks = [...state.tasks];
  let agents = [...state.agents];

  for (let i = 0; i < agents.length; i++) {
    const agent = agents[i];
    const existing = getActiveTaskForAgent(tasks, agent.id);
    if (existing) continue;

    // Assess needs and create task
    const objectTask = createLifeTaskForAgent(agent, state, rng);
    if (objectTask) {
      tasks = [...tasks, objectTask];
      continue;
    }

    const assessments = assessNeeds(agent);
    if (assessments.length === 0) {
      // Idle: assign work/purpose task by role
      const prefs = ["work", "research", "explore"] as const;
      const taskType = pick([...prefs], rng);
      const building = state.buildings.find(b =>
        b.type === "workshop" || b.type === "archive" || b.type === "observatory"
      );
      if (building) {
        const task: Task = {
          id: uid(rng),
          type: taskType,
          title: `Idle ${taskType} (${agent.name})`,
          agentId: agent.id,
          targetBuildingId: building.id,
          progress: 0,
          status: "pending",
          R_delta: -0.01,
          Phi_delta: 0.01,
          evidence: [],
        };
        tasks = [...tasks, task];
      }
      continue;
    }

    const top = assessments[0];
    const targetBuilding = findNearestBuilding(agent, state.buildings, top.buildingType);
    const task = createTaskForNeed(agent, top, targetBuilding, rng);
    tasks = [...tasks, task];
  }

  return { ...state, tasks };
}

export function assignActiveTasks(state: CityState): CityState {
  const tasks = state.tasks.map(task => {
    if (task.status !== "pending") return task;
    // Activate pending tasks
    return { ...task, status: "active" as const };
  });
  return { ...state, tasks };
}
