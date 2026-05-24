import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createBrainRuntime } from "../brain/brainRuntime";

describe("brain runtime audio/game-feel integration v1.3.1", () => {
  it("connects audio game-feel while execution remains disabled", () => {
    const runtime = createBrainRuntime({ city: createCity() });
    expect(runtime.executionAllowed).toBe(false);
    expect(runtime.audioGameFeel?.enabled).toBe(false);
    expect(runtime.systems.audioGameFeel.active).toBe(true);
    expect(Number.isFinite(runtime.systems.audioGameFeel.R)).toBe(true);
    expect(Number.isFinite(runtime.systems.audioGameFeel.Phi_eff)).toBe(true);
  });
});
