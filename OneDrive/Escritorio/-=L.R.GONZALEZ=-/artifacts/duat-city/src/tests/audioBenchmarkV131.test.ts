import { describe, expect, it } from "vitest";
import { AUDIO_GAMEFEEL_BENCHMARK_SCENARIOS, runAudioGameFeelBenchmark } from "../audio/audioBenchmark";

describe("audio/game-feel benchmark v1.3.1", () => {
  it("emits a complete finite benchmark schema without browser audio", () => {
    const doc = runAudioGameFeelBenchmark(4);
    expect(doc.schema).toBe("duat/audio-gamefeel-benchmark/v1.3.1");
    expect(doc.browserAudioUsed).toBe(false);
    expect(doc.scenarios).toHaveLength(AUDIO_GAMEFEEL_BENCHMARK_SCENARIOS.length);
    expect(doc.scenarios.every(result => result.finite && result.proceduralOnly)).toBe(true);
    expect(doc.scenarios.every(result => Number.isFinite(result.avgMapMs) && Number.isFinite(result.p95MapMs))).toBe(true);
  });
});
