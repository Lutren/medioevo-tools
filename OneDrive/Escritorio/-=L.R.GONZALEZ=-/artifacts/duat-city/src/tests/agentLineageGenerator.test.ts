import { describe, expect, it } from "vitest";
import { seededRandom } from "../core/math";
import { generateAgentLineage, generateOriginStory } from "../generative/agentLineageGenerator";
import { createAgent } from "../sim/agents";

describe("agent lineage generator", () => {
  it("generates deterministic two-generation lineage", () => {
    const a = generateAgentLineage("Observer", seededRandom("lineage-seed"));
    const b = generateAgentLineage("Observer", seededRandom("lineage-seed"));
    expect(a).toEqual(b);
    expect(a.grandparents).toHaveLength(2);
    expect(a.parents).toHaveLength(2);
    expect(a.parents[0].profession).toBeTruthy();
    expect(a.parents[0].originEra).toBeTruthy();
    expect(a.parents[0].formativeEvent).toBeTruthy();
  });

  it("createAgent carries lineage and origin story", () => {
    const agent = createAgent("Archivist", 4, 5, seededRandom("agent-lineage"));
    expect(agent.lineage.schema).toBe("duat.agent-lineage.v1");
    expect(agent.originStory).toBe(generateOriginStory(agent.role, agent.lineage));
  });
});
