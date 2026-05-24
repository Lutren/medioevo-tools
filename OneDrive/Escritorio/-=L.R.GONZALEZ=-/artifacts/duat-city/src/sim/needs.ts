import type { Agent, Task, Building, TaskType } from "../core/types";
import { uid, type RandomSource } from "../core/math";
import { ROLE_TASK_PREFS } from "./agents";

const NEED_THRESHOLD = 0.3;

export interface NeedAssessment {
  needKey: keyof Agent["needs"];
  taskType: TaskType;
  buildingType: string;
  priority: number;
}

export function assessNeeds(agent: Agent): NeedAssessment[] {
  const needs = agent.needs;
  const assessments: NeedAssessment[] = [];

  if (needs.hunger < NEED_THRESHOLD) {
    assessments.push({ needKey: "hunger", taskType: "eat", buildingType: "market", priority: (NEED_THRESHOLD - needs.hunger) * 10 });
    assessments.push({ needKey: "hunger", taskType: "eat", buildingType: "garden", priority: (NEED_THRESHOLD - needs.hunger) * 8 });
  }
  if (needs.energy < NEED_THRESHOLD) {
    assessments.push({ needKey: "energy", taskType: "rest", buildingType: "residential", priority: (NEED_THRESHOLD - needs.energy) * 9 });
  }
  if (needs.safety < NEED_THRESHOLD) {
    assessments.push({ needKey: "safety", taskType: "heal", buildingType: "clinic", priority: (NEED_THRESHOLD - needs.safety) * 8 });
  }
  if (needs.social < NEED_THRESHOLD) {
    assessments.push({ needKey: "social", taskType: "eat", buildingType: "plaza", priority: (NEED_THRESHOLD - needs.social) * 6 });
  }
  if (needs.curiosity < NEED_THRESHOLD) {
    assessments.push({ needKey: "curiosity", taskType: "research", buildingType: "archive", priority: (NEED_THRESHOLD - needs.curiosity) * 5 });
    assessments.push({ needKey: "curiosity", taskType: "explore", buildingType: "observatory", priority: (NEED_THRESHOLD - needs.curiosity) * 4 });
  }
  if (needs.purpose < NEED_THRESHOLD) {
    const prefs = ROLE_TASK_PREFS[agent.role as keyof typeof ROLE_TASK_PREFS] ?? ["work"];
    const taskType = prefs[0] as TaskType;
    assessments.push({ needKey: "purpose", taskType, buildingType: "workshop", priority: (NEED_THRESHOLD - needs.purpose) * 7 });
  }

  return assessments.sort((a, b) => b.priority - a.priority);
}

export function createTaskForNeed(
  agent: Agent,
  assessment: NeedAssessment,
  targetBuilding: Building | undefined,
  rng?: RandomSource
): Task {
  const labels: Record<TaskType, string> = {
    eat: "Eat & rest",
    rest: "Sleep/recover",
    work: "Work shift",
    research: "Research session",
    archive: "Archive data",
    heal: "Seek healing",
    build: "Build/repair",
    trade: "Market trade",
    teach: "Teaching session",
    explore: "Exploration",
    quest: "Quest task",
    handoff: "Generate handoff",
  };

  return {
    id: uid(rng),
    type: assessment.taskType,
    title: `${labels[assessment.taskType]} (${agent.name})`,
    agentId: agent.id,
    targetBuildingId: targetBuilding?.id,
    targetTileId: targetBuilding ? targetBuilding.y * 48 + targetBuilding.x : undefined,
    progress: 0,
    status: "pending",
    R_delta: -0.03,
    Phi_delta: 0.02,
    evidence: [],
  };
}
