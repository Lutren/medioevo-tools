import type { Agent, CityState } from "../core/types";
import { addWitnessEntry } from "../core/witnesslog";
import { clamp } from "../core/math";
import { computeAgentGate, computePhiEff } from "../core/metrics";
import { compileResidueDreamCycle } from "./residueDreamCycle";
import { runTruthGate } from "./truthGate";

export interface DesvarioAssessment {
  desvariando: boolean;
  reasons: string[];
}

export function assessDesvario(agent: Agent, city: CityState): DesvarioAssessment {
  const failedLoops = city.tasks.filter(task => task.agentId === agent.id && task.status === "failed").length;
  const blockedLoops = city.tasks.filter(task => task.agentId === agent.id && task.status === "blocked").length;
  const zeroNeeds = Object.values(agent.needs).filter(value => value <= 0.05).length;
  const reasons = [
    agent.R >= 0.55 ? `R=${agent.R.toFixed(3)}` : "",
    agent.gate === "BLOCK" ? "gate=BLOCK" : "",
    zeroNeeds >= 2 ? `zero_needs=${zeroNeeds}` : "",
    failedLoops >= 3 ? `failed_loops=${failedLoops}` : "",
    blockedLoops >= 2 ? `blocked_loops=${blockedLoops}` : "",
  ].filter(Boolean);
  return { desvariando: reasons.length > 0, reasons };
}

export function repairAgent(agent: Agent, city: CityState, psychologist?: Agent): { agent: Agent; evidence: string[] } {
  const assessment = assessDesvario(agent, city);
  if (!assessment.desvariando) return { agent, evidence: [] };

  const residue = compileResidueDreamCycle(city);
  const truth = runTruthGate(["tests", "typecheck"]);
  const needs: Agent["needs"] = {
    energy: clamp(agent.needs.energy + 0.18, 0, 1),
    hunger: clamp(agent.needs.hunger + 0.18, 0, 1),
    social: clamp(agent.needs.social + 0.18, 0, 1),
    purpose: clamp(agent.needs.purpose + 0.18, 0, 1),
    safety: clamp(agent.needs.safety + 0.18, 0, 1),
    curiosity: clamp(agent.needs.curiosity + 0.18, 0, 1),
  };
  const R = clamp(Math.min(agent.R, 0.42) - 0.16, 0, 1);
  const mood = clamp(agent.mood + 0.08, 0, 1);
  const trust = clamp(agent.trust + 0.06, 0, 1);
  const Phi_eff = computePhiEff(R, mood, trust);
  const gate = computeAgentGate(R);
  const therapist = psychologist ? ` by ${psychologist.name}` : "";
  return {
    agent: {
      ...agent,
      needs,
      mood,
      trust,
      R,
      Phi_eff,
      gate,
      memory: [...agent.memory, `Psychologist repair cycle${therapist}: ${assessment.reasons.join(", ")}`].slice(-10),
    },
    evidence: [
      `desvario=${assessment.reasons.join("|")}`,
      `truth_gate=${truth.gate}`,
      `residue_inputs=${residue.residueInputs.length}`,
      `psychologist=${psychologist?.id ?? "system"}`,
    ],
  };
}

export function runPsychologistRepairCycle(city: CityState): CityState {
  const psychologist = city.agents.find(agent => agent.role === "Psychologist");
  if (!psychologist) return city;

  const target = city.agents.find(agent => agent.id !== psychologist.id && assessDesvario(agent, city).desvariando);
  if (!target) return city;

  const repaired = repairAgent(target, city, psychologist);
  if (repaired.evidence.length === 0) return city;

  const agents = city.agents.map(agent => agent.id === target.id ? repaired.agent : agent);
  const next = { ...city, agents };
  return addWitnessEntry(
    next,
    "psychologist_repair",
    `Psychologist repaired ${target.name}`,
    repaired.evidence,
  );
}
