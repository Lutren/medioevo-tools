import { createCity } from "../sim/city";
import { applyVibeSceneToPlayableScene, createDefaultPlayableSceneState, makeAgentLoadState, placeSceneLight, placeSceneMaterial } from "../scene/sceneState";
import { compileVibeScene } from "../vibecoding/vibeSceneCompiler";
import { createAudioGameFeelSnapshot } from "./gameFeelAdapter";
import type { AudioBenchmarkDocument, AudioBenchmarkScenario } from "./audioTypes";

export const AUDIO_GAMEFEEL_BENCHMARK_SCENARIOS: AudioBenchmarkScenario[] = [
  { id: "baseline_city", label: "baseline city silent/off", materials: [], lights: [], agents: 12, expectedCueKinds: ["gate_approve"] },
  { id: "fire_smoke", label: "fire plus smoke material cue stack", materials: ["fire", "smoke"], lights: ["fire"], agents: 12, expectedCueKinds: ["material_fire", "material_smoke", "cosmology_fire_event"] },
  { id: "neon_rain", label: "neon rain street cues", materials: ["water", "neon", "smoke"], lights: ["neon"], agents: 12, expectedCueKinds: ["material_water", "material_neon", "light_neon"] },
  { id: "agent_stress", label: "agent needs and R cue budget", materials: [], lights: [], agents: 64, expectedCueKinds: ["agent_need"] },
  { id: "rpg_transition", label: "RPG gate transition cue set", materials: ["stone", "water"], lights: ["signal"], agents: 24, expectedCueKinds: ["light_signal"] },
  { id: "metroidvania_gate", label: "metroidvania gate and ruin anomaly", materials: ["fire", "neon"], lights: ["ruin_anomaly"], agents: 32, expectedCueKinds: ["light_ruin_anomaly", "cosmology_fire_event"] },
];

export function runAudioGameFeelBenchmark(iterationsPerScenario = 160): AudioBenchmarkDocument {
  const scenarios = AUDIO_GAMEFEEL_BENCHMARK_SCENARIOS.map(scenario => {
    const timings: number[] = [];
    let cueCount = 0;
    let R_audio = 0;
    let Phi_audio = 1;
    for (let i = 0; i < iterationsPerScenario; i++) {
      const state = createBenchmarkState(scenario);
      const start = now();
      const snapshot = createAudioGameFeelSnapshot(state);
      timings.push(now() - start);
      cueCount = snapshot.metrics.cueCount;
      R_audio = snapshot.metrics.R_audio;
      Phi_audio = snapshot.metrics.Phi_audio;
    }
    const sorted = timings.slice().sort((a, b) => a - b);
    const avgMapMs = timings.reduce((sum, value) => sum + value, 0) / Math.max(1, timings.length);
    const p95MapMs = sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95))] ?? avgMapMs;
    return {
      scenario: scenario.id,
      label: scenario.label,
      avgMapMs: round3(avgMapMs),
      p95MapMs: round3(p95MapMs),
      cueCount,
      R_audio,
      Phi_audio,
      proceduralOnly: true as const,
      finite: [avgMapMs, p95MapMs, cueCount, R_audio, Phi_audio].every(Number.isFinite),
    };
  });
  return {
    schema: "duat/audio-gamefeel-benchmark/v1.3.1",
    fingerprint: "DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY",
    generatedAt: new Date().toISOString(),
    iterationsPerScenario,
    browserAudioUsed: false,
    scenarios,
    notes: [
      "Pure mapping benchmark: no AudioContext, no samples, no cloud.",
      "Audio remains off by default until a local user gesture enables browser synthesis.",
    ],
  };
}

function createBenchmarkState(scenario: AudioBenchmarkScenario) {
  let city = makeAgentLoadState(createCity(), scenario.agents);
  if (scenario.id === "agent_stress") {
    city = {
      ...city,
      agents: city.agents.map((agent, index) => ({
        ...agent,
        R: Math.min(1, agent.R + 0.22),
        needs: { ...agent.needs, energy: index % 2 === 0 ? 0.18 : agent.needs.energy, safety: index % 3 === 0 ? 0.2 : agent.needs.safety },
      })),
    };
  }
  let scene = createDefaultPlayableSceneState();
  if (scenario.id === "neon_rain") {
    scene = applyVibeSceneToPlayableScene(scene, compileVibeScene("neon_rain_street", "preset").config, city.width, city.height);
  }
  const cx = Math.floor(city.width / 2);
  const cy = Math.floor(city.height / 2);
  scenario.materials.forEach((material, index) => {
    scene = placeSceneMaterial(scene, cx + index - 2, cy + index, material as never);
  });
  scenario.lights.forEach((light, index) => {
    scene = placeSceneLight(scene, cx + index - 1, cy - 1, light as never);
  });
  return { ...city, playableScene: scene };
}

function now(): number {
  return typeof performance !== "undefined" && typeof performance.now === "function" ? performance.now() : Date.now();
}

function round3(value: number): number {
  return Number(Number.isFinite(value) ? value.toFixed(3) : "0");
}
