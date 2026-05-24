import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createDefaultPlayableSceneState, placeSceneLight, placeSceneMaterial } from "../scene/sceneState";
import { createAudioGameFeelSnapshot, isAudioSnapshotFinite } from "../audio/gameFeelAdapter";

describe("audio/game-feel adapter v1.3.1", () => {
  it("is off by default and requires user gesture", () => {
    const snapshot = createAudioGameFeelSnapshot(createCity());
    expect(snapshot.enabled).toBe(false);
    expect(snapshot.requiresUserGesture).toBe(true);
    expect(snapshot.boundary.proceduralOnly).toBe(true);
    expect(snapshot.boundary.externalSamplesCopied).toBe(false);
    expect(snapshot.boundary.wabiExecutionAllowed).toBe(false);
  });

  it("maps playable materials and lights into deterministic cues", () => {
    let scene = createDefaultPlayableSceneState();
    scene = placeSceneMaterial(scene, 10, 10, "fire");
    scene = placeSceneMaterial(scene, 11, 10, "smoke");
    scene = placeSceneMaterial(scene, 12, 10, "neon");
    scene = placeSceneLight(scene, 12, 9, "neon");
    const state = { ...createCity(), playableScene: scene };
    const a = createAudioGameFeelSnapshot(state);
    const b = createAudioGameFeelSnapshot(state);
    const kinds = a.cues.map(cue => cue.kind);
    expect(kinds).toContain("material_fire");
    expect(kinds).toContain("material_smoke");
    expect(kinds).toContain("material_neon");
    expect(kinds).toContain("light_neon");
    expect(kinds).toContain("cosmology_fire_event");
    expect(a.metrics.deterministicHash).toBe(b.metrics.deterministicHash);
    expect(isAudioSnapshotFinite(a)).toBe(true);
  });

  it("keeps audio metrics finite under high agent counts", () => {
    const state = createCity();
    const stressed = {
      ...state,
      agents: state.agents.map(agent => ({
        ...agent,
        R: 0.52,
        needs: { ...agent.needs, energy: 0.12, safety: 0.18 },
      })),
    };
    const snapshot = createAudioGameFeelSnapshot(stressed);
    expect(snapshot.metrics.agentCues).toBeGreaterThan(0);
    expect(snapshot.metrics.finite).toBe(true);
    expect(snapshot.metrics.R_audio).toBeGreaterThanOrEqual(0);
    expect(snapshot.metrics.Phi_audio).toBeLessThanOrEqual(1);
  });
});
