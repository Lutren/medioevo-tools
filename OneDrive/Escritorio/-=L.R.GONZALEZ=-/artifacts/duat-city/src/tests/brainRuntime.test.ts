import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createBrainRuntime } from "../brain/brainRuntime";
import { createHippocampusHandoff } from "../brain/hippocampusHandoff";
import { evaluatePrefrontalActionGate } from "../brain/prefrontalActionGate";
import { filterAttentionGhostEvent } from "../brain/attentionGhostGate";
import { runTruthGate } from "../brain/truthGate";

describe("brain runtime v1.3", () => {
  it("stores handoff and keeps execution disabled", () => {
    const city = createCity();
    const runtime = createBrainRuntime({ city });
    expect(runtime.executionAllowed).toBe(false);
    expect(createHippocampusHandoff(city).handoff).toBeTruthy();
  });

  it("blocks unsafe actions, filters noisy events and runs truth gate", () => {
    expect(evaluatePrefrontalActionGate({ action: "deploy", risk: 0.1 }).gate).toBe("BLOCK");
    expect(filterAttentionGhostEvent({ id: "noise", R: 0.8, signal: 0.1 }).accepted).toBe(false);
    expect(runTruthGate(["tests", "typecheck"]).gate).toBe("APPROVE");
  });
});
