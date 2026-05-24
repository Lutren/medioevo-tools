import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { assertFiniteGameModeState, listGameModes, switchGameMode } from "../gameModes/gameModeRouter";
import { createGameModeState } from "../gameModes/gameModeState";

describe("game mode router v1.3", () => {
  it("registers all modes and preserves finite state while switching", () => {
    const city = createCity();
    const ids = listGameModes().map(mode => mode.id);
    expect(ids).toEqual(["duat_interface", "hormiguero", "agent_sims", "city_president", "era_progression", "vs_arena", "rpg", "metroidvania"]);
    let state = createGameModeState();
    for (const id of ids) state = switchGameMode(state, id, city);
    expect(state.activeMode).toBe("metroidvania");
    expect(assertFiniteGameModeState(state)).toBe(true);
  });
});
