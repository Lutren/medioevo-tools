import type { CityState } from "../core/types";
import { computeRegime, computeGate, computePhiEff } from "../core/metrics";
import { clamp, seededRandom, type RandomSource } from "../core/math";
import { tickBuilding } from "./buildings";
import { applyResourceDelta } from "./resources";
import { decayNeeds, updateAgentMetrics, moveAgentToward, restoreNeedAtBuilding, addMemory } from "./agents";
import { stepTask, cleanupTasks, getActiveTaskForAgent } from "./tasks";
import { scheduleTasks, assignActiveTasks } from "./scheduler";
import { updateRelationships } from "./relationships";
import { generateTickEvents } from "./events";
import { computeGlobalR } from "./city";
import { getBuildingById } from "./buildings";
import { addWitnessEntry } from "../core/witnesslog";
import { stepAgentPhysics } from "../physics/agentPhysicsAdapter";
import { stepCityField } from "../physicsField/fieldRendererAdapter";
import { evaluateCityQuaternary } from "./quaternaryAdapter";
import { runPsychologistRepairCycle } from "../brain/psychologist";

const AGENT_SPEED = 1.8;

export interface TickEngineOptions {
  enableAgentPhysics?: boolean;
  enablePhysicsCollisions?: boolean;
  enablePixelField?: boolean;
  physicsDt?: number;
  rng?: RandomSource;
  seed?: string | number;
}

export function tickEngine(state: CityState, options: TickEngineOptions = {}): CityState {
  const previousState = state;
  let s = { ...state, tick: state.tick + 1 };
  const rng = options.rng ?? seededRandom(options.seed ?? replaySeedForState(state));

  // 1. Building production
  let resources = { ...s.resources };
  let buildings = s.buildings.map(b => {
    const { building, resourceDelta } = tickBuilding(b, resources);
    resources = applyResourceDelta(resources, resourceDelta);
    return building;
  });
  s = { ...s, buildings, resources };

  // 2. Schedule new tasks
  s = scheduleTasks(s, rng);
  s = assignActiveTasks(s);

  // 3. Agent update loop
  let agents = s.agents.map(agent => decayNeeds(agent, 1));
  let tasks = [...s.tasks];

  agents = agents.map(agent => {
    const task = getActiveTaskForAgent(tasks, agent.id);
    if (!task) return updateAgentMetrics(agent);

    const targetBuilding = task.targetBuildingId
      ? getBuildingById(s.buildings, task.targetBuildingId)
      : undefined;

    // Move toward target
    let updatedAgent = agent;
    if (targetBuilding) {
      const arrived = Math.abs(agent.x - targetBuilding.x) < 0.3 && Math.abs(agent.y - targetBuilding.y) < 0.3;
      if (!arrived && !options.enableAgentPhysics) {
        updatedAgent = moveAgentToward(agent, targetBuilding.x, targetBuilding.y, AGENT_SPEED, 1);
      } else if (!arrived) {
        updatedAgent = { ...updatedAgent, currentTaskId: task.id };
      } else {
        // At building: restore needs and step task
        updatedAgent = restoreNeedAtBuilding(agent, targetBuilding.type);
        const { task: updatedTask, done } = stepTask(task, updatedAgent, targetBuilding, s.tick, rng);
        const taskIdx = tasks.findIndex(t => t.id === task.id);
        if (taskIdx !== -1) tasks[taskIdx] = updatedTask;

        if (done) {
          updatedAgent = {
            ...updatedAgent,
            currentTaskId: undefined,
            R: clamp(updatedAgent.R + updatedTask.R_delta, 0, 1),
          };
          if (updatedTask.status === "done") {
            updatedAgent = addMemory(updatedAgent, `Completed: ${updatedTask.title}`);
          }
        } else {
          updatedAgent = { ...updatedAgent, currentTaskId: task.id };
        }
      }
    } else {
      // No building target — step task in place
      const { task: updatedTask, done } = stepTask(task, updatedAgent, undefined, s.tick, rng);
      const taskIdx = tasks.findIndex(t => t.id === task.id);
      if (taskIdx !== -1) tasks[taskIdx] = updatedTask;
      if (done) updatedAgent = { ...updatedAgent, currentTaskId: undefined };
      else updatedAgent = { ...updatedAgent, currentTaskId: task.id };
    }

    return updateAgentMetrics(updatedAgent);
  });

  s = { ...s, agents, tasks };

  if (options.enableAgentPhysics) {
    const physics = stepAgentPhysics(s, undefined, options.physicsDt ?? 0.05, options.enablePhysicsCollisions ?? true);
    agents = physics.state.agents;
    s = { ...s, agents, physicsMetrics: physics.metrics };
  }

  if (options.enablePixelField !== false) {
    const field = stepCityField(s);
    s = { ...s, ...field };
  }

  // 4. Relationships
  agents = updateRelationships(agents);

  s = { ...s, agents, tasks: cleanupTasks(tasks) };

  s = runPsychologistRepairCycle(s);
  agents = s.agents;

  // 5. Global R / Phi_eff
  const R = computeGlobalR(s);
  const avgMood = agents.reduce((acc, a) => acc + a.mood, 0) / Math.max(1, agents.length);
  const avgTrust = agents.reduce((acc, a) => acc + a.trust, 0) / Math.max(1, agents.length);
  const Phi_eff = computePhiEff(R, avgMood, avgTrust);
  const regime = computeRegime(R, Phi_eff);
  const gate = computeGate(R);

  s = { ...s, R, Phi_eff, regime, gate };

  // 5b. Quaternary timing diagnostics. This augments city metrics without
  // replacing the base city R/Phi_eff values used by the existing sim.
  const quaternary = evaluateCityQuaternary(s, previousState, s.tick);
  s = { ...s, quaternary: quaternary.summary };
  if (shouldLogQuaternaryWitness(s, previousState)) {
    s = addWitnessEntry(
      s,
      "quaternary_timing_gate",
      `Quaternary gate ${quaternary.summary.gate}: Rq=${quaternary.summary.R.toFixed(3)} Phiq=${quaternary.summary.Phi_eff.toFixed(3)}`,
      [
        `counts=${JSON.stringify(quaternary.summary.counts)}`,
        `top_anomalies=${quaternary.summary.topAnomalies.slice(0, 3).join("|") || "none"}`,
        `top_unstable=${quaternary.summary.topUnstable.slice(0, 3).join("|") || "none"}`,
      ],
    );
  }

  // 6. Events
  const newEvents = generateTickEvents(s, rng);
  const events = [...s.events, ...newEvents].slice(-100);
  s = { ...s, events };

  // 7. Witness log (periodic)
  if (s.tick % 25 === 0) {
    s = addWitnessEntry(s, "tick", `Tick ${s.tick}: R=${R.toFixed(3)} Phi=${Phi_eff.toFixed(3)} regime=${regime}`, [`gate=${gate}`, `agents=${agents.length}`, `buildings=${s.buildings.length}`]);
  }

  return s;
}

function replaySeedForState(state: CityState): string {
  return [
    "duat-city-tick",
    state.tick,
    state.width,
    state.height,
    state.agents.length,
    state.buildings.length,
    state.tasks.length,
    state.events.length,
    state.R.toFixed(6),
    state.Phi_eff.toFixed(6),
  ].join(":");
}

function shouldLogQuaternaryWitness(state: CityState, previousState: CityState): boolean {
  const q = state.quaternary;
  if (!q) return false;
  const previousGate = previousState.quaternary?.gate ?? "APPROVE";
  const gateCrossed = q.gate !== "APPROVE" && q.gate !== previousGate;
  const highAbsence = q.counts["01"] >= 3 && q.anomalyRate > 0.08;
  const unstable = q.avgFrequency > 0.45 || q.topUnstable.length >= 3;
  if (!gateCrossed && !highAbsence && !unstable) return false;
  const recent = state.witnesslog
    .filter(entry => entry.type === "quaternary_timing_gate")
    .slice(-1)[0];
  return !recent || state.tick - recent.tick >= 12;
}
