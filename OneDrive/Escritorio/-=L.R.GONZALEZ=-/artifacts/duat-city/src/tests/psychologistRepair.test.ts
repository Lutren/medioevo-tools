import { describe, expect, it } from "vitest";
import { assessDesvario, repairAgent, runPsychologistRepairCycle } from "../brain/psychologist";
import { createCity } from "../sim/city";
import { createAgent } from "../sim/agents";

describe("psychologist repair", () => {
  it("detects agents that are desvariando", () => {
    const city = createCity("desvario-detect");
    const agent = { ...city.agents[0], R: 0.8, gate: "BLOCK" as const };
    const assessment = assessDesvario(agent, city);
    expect(assessment.desvariando).toBe(true);
    expect(assessment.reasons).toContain("gate=BLOCK");
  });

  it("repairs needs, residue and gate with evidence", () => {
    const city = createCity("desvario-repair");
    const troubled = {
      ...city.agents[0],
      R: 0.8,
      gate: "BLOCK" as const,
      needs: { energy: 0, hunger: 0, social: 0.1, purpose: 0.1, safety: 0, curiosity: 0.1 },
    };
    const psychologist = createAgent("Psychologist", 1, 1);
    const repaired = repairAgent(troubled, { ...city, agents: [troubled, psychologist] }, psychologist);
    expect(repaired.agent.R).toBeLessThan(troubled.R);
    expect(repaired.agent.gate).not.toBe("BLOCK");
    expect(repaired.agent.needs.energy).toBeGreaterThan(troubled.needs.energy);
    expect(repaired.evidence.some(item => item.startsWith("truth_gate="))).toBe(true);
  });

  it("registers repair in witnesslog when psychologist is in the city", () => {
    const city = createCity("desvario-cycle");
    const troubled = { ...city.agents[0], R: 0.8, gate: "BLOCK" as const };
    const psychologist = createAgent("Psychologist", 2, 2);
    const repaired = runPsychologistRepairCycle({ ...city, agents: [troubled, psychologist], witnesslog: [] });
    expect(repaired.witnesslog.some(entry => entry.type === "psychologist_repair")).toBe(true);
    expect(repaired.agents[0].R).toBeLessThan(troubled.R);
  });
});
