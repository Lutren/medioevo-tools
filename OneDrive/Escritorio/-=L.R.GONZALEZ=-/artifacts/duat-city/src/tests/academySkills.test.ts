import { describe, expect, it } from "vitest";
import { saveCityToJson, loadCityFromJson } from "../core/persistence";
import { installSkillPack } from "../brain/skillPacks";
import { createAgent, restoreNeedAtBuilding } from "../sim/agents";
import { createCity } from "../sim/city";

describe("academy skill packs", () => {
  it("installs a role-affinity skill when agent visits academy", () => {
    const agent = createAgent("Engineer", 0, 0);
    const trained = restoreNeedAtBuilding(agent, "academy");
    expect(trained.skills).toContain("debugger");
    expect(trained.memory.some(entry => entry.includes("Installed skill pack"))).toBe(true);
  });

  it("does not duplicate skill packs", () => {
    const agent = createAgent("Medic", 0, 0);
    const once = installSkillPack(agent, "field_medic");
    const twice = installSkillPack(once, "field_medic");
    expect(twice.skills.filter(skill => skill === "field_medic")).toHaveLength(1);
  });

  it("persists installed skills in city JSON", () => {
    const city = createCity("academy-persist");
    const agents = city.agents.map((agent, index) => index === 0 ? installSkillPack(agent, "curator") : agent);
    const loaded = loadCityFromJson(saveCityToJson({ ...city, agents }));
    expect(loaded?.agents[0].skills).toContain("curator");
  });
});
