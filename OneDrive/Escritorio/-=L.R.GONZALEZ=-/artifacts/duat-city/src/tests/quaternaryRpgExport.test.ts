import { describe, expect, it } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { createCity } from "../sim/city";
import { tickEngine } from "../sim/engine";

describe("quaternary RPG export", () => {
  it("includes quaternary profile", () => {
    const world = exportRPGWorld(tickEngine(createCity()));
    expect(world.quaternary_profile).toBeDefined();
    expect(world.quaternary_profile?.counts).toBeDefined();
  });

  it("anomaly profile can create quest hook", () => {
    const state = tickEngine(createCity());
    const world = exportRPGWorld({
      ...state,
      quaternary: {
        ...state.quaternary!,
        counts: { "00": 0, "01": 4, "10": 0, "11": 0 },
        recent: [
          {
            sourceId: "building:ruin-gatehouse",
            sourceKind: "building",
            tick: state.tick,
            state: "01",
            meaning: "ABSENCE_SIGNIFICANT",
            action: "REVIEW",
            R_delta: 0.1,
            Phi_delta: -0.05,
            confidence: 0.4,
            reason: "missing signal",
            timing: {
              current: "01",
              previous: "01",
              dwellTicks: 2,
              transitions: 1,
              frequency: 0.2,
              period: null,
              permanence: 0.2,
              stability: 0.3,
              confidence: 0.4,
              residue: 0.4,
              windowSize: 8,
            },
          },
        ],
      },
    });
    expect(world.quests.some(quest => quest.title === "Investigate missing signal")).toBe(true);
  });
});

