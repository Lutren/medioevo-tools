import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createGameModeState } from "../gameModes/gameModeState";
import { applyCityPolicy } from "../gameModes/cityPresidentMode";

describe("city president mode v1.3", () => {
  it("applies policy indirectly and updates resources/agents", () => {
    const city = createCity();
    const before = city.resources.knowledge;
    const result = applyCityPolicy(createGameModeState("city_president"), city, { policy: "knowledge", delta: 0.5 });
    expect(result.city.resources.knowledge).toBeGreaterThan(before);
    expect(result.mode.policies.knowledge).toBeGreaterThan(0);
    expect(result.city.agents[0].trust).toBeGreaterThanOrEqual(city.agents[0].trust);
  });
});
