import type { Agent } from "../core/types";
import { clamp } from "../core/math";

export interface SkillPack {
  id: string;
  label: string;
  brainSystems: string[];
  roleAffinity: string[];
}

export const SKILL_PACKS: SkillPack[] = [
  { id: "curator", label: "Curator", brainSystems: ["truth_gate", "hippocampus"], roleAffinity: ["Archivist", "Observer", "Storykeeper"] },
  { id: "debugger", label: "Debugger", brainSystems: ["prefrontal", "attention"], roleAffinity: ["Engineer", "Builder", "Artisan"] },
  { id: "psychologist", label: "Psychologist", brainSystems: ["affect", "social", "residue_dream"], roleAffinity: ["Psychologist", "Medic", "Teacher"] },
  { id: "field_medic", label: "Field Medic", brainSystems: ["affect", "goal_alignment"], roleAffinity: ["Medic", "Scout", "Gatekeeper"] },
  { id: "signal_cartographer", label: "Signal Cartographer", brainSystems: ["attention", "cross_modal"], roleAffinity: ["Observer", "Courier", "Trader"] },
];

export function getSkillPack(id: string): SkillPack | undefined {
  return SKILL_PACKS.find(pack => pack.id === id);
}

export function defaultSkillPackForRole(role: string): string {
  return SKILL_PACKS.find(pack => pack.roleAffinity.includes(role))?.id ?? "curator";
}

export function installSkillPack(agent: Agent, packId: string): Agent {
  const pack = getSkillPack(packId);
  if (!pack || agent.skills.includes(pack.id)) return agent;
  return {
    ...agent,
    skills: [...agent.skills, pack.id],
    Phi_eff: clamp(agent.Phi_eff + 0.04, 0, 1),
    memory: [...agent.memory, `Installed skill pack: ${pack.label}`].slice(-10),
  };
}
