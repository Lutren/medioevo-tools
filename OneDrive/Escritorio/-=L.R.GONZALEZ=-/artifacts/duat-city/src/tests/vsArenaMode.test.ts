import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createVsArenaState, tickVsArena } from "../gameModes/vsArenaMode";

describe("vs arena mode v1.3", () => {
  it("initializes two fighters and ticks without NaN", () => {
    const arena = tickVsArena(createVsArenaState(createCity()));
    expect(arena.fighters.length).toBe(2);
    expect(arena.fighters.every(fighter => Number.isFinite(fighter.x) && Number.isFinite(fighter.R))).toBe(true);
  });
});
