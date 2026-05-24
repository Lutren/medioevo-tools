import { describe, expect, it } from "vitest";
import { generateTheaterAgentProfile } from "../generative/proceduralAgentGenerator";
import { BUILDING_DEFS } from "../sim/buildings";

describe("theater agent profile", () => {
  it("generates a complete deterministic profile ready for academy", () => {
    const a = generateTheaterAgentProfile("Teacher", 42);
    const b = generateTheaterAgentProfile("Teacher", 42);
    expect(a).toEqual(b);
    expect(a.schema).toBe("duat.theater-agent-profile.v1");
    expect(a.role).toBe("Teacher");
    expect(a.lineage.grandparents).toHaveLength(2);
    expect(a.originStory).toContain("Teacher");
    expect(a.sprite.width).toBe(8);
    expect(a.readyForAcademy).toBe(true);
  });

  it("registers theater as a functional building", () => {
    expect(BUILDING_DEFS.theater?.label).toBe("Theater");
    expect(BUILDING_DEFS.theater?.produces.culture).toBeGreaterThan(0);
  });
});
