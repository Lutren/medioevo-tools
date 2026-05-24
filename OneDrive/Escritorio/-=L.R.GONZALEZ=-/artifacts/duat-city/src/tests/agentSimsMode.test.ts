import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { selectAgentSimsView } from "../gameModes/agentSimsMode";

describe("agent sims mode v1.3", () => {
  it("selects/follows an agent and respects causal knowledge boundary", () => {
    const city = createCity();
    const view = selectAgentSimsView(city, city.agents[0].id);
    expect(view.agent?.id).toBe(city.agents[0].id);
    expect(view.decisionSuggestion.length).toBeGreaterThan(0);
    expect(view.omniscienceBlocked).toBe(true);
    expect(view.causalKnowledge.join(" ")).not.toMatch(/all secrets|omniscient/i);
  });
});
