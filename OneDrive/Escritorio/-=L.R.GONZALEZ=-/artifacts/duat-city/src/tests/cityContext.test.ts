import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { CLIMATE_OPTIONS, GEOGRAPHY_OPTIONS, selectCityContext } from "../sim/cityContext";

describe("city context selection", () => {
  it("starts with selectable climate and geography context", () => {
    const city = createCity("context-default");
    expect(city.context.schema).toBe("duat.city-context.v1");
    expect(CLIMATE_OPTIONS).toContain(city.context.climate);
    expect(GEOGRAPHY_OPTIONS).toContain(city.context.geography);
  });

  it("updates era, climate, geography and weather without changing city size", () => {
    const city = createCity("context-select");
    const next = selectCityContext(city, {
      era: "medieval",
      climate: "cold",
      geography: "mountain_gate",
      weather: "fog",
    });
    expect(next.width).toBe(city.width);
    expect(next.height).toBe(city.height);
    expect(next.context.era).toBe("medieval");
    expect(next.context.climate).toBe("cold");
    expect(next.context.geography).toBe("mountain_gate");
    expect(next.context.weather).toBe("fog");
  });
});
