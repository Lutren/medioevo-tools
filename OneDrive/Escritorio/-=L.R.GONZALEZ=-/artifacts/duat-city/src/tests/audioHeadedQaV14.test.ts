import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const reportUrl = new URL("../../docs/AUDIO_HEADED_QA_v1_4.json", import.meta.url);

describe("audio headed QA v1.4", () => {
  it("records off-by-default audio and procedural preview fallback without claiming human audibility", () => {
    const report = JSON.parse(readFileSync(reportUrl, "utf8"));
    expect(report.schema).toBe("duat/audio-headed-qa/v1.4");
    expect(report.fingerprint).toBe("DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL");
    expect(report.audioOffByDefault).toBe(true);
    expect(report.browserAudioAvailable).toBe(true);
    expect(report.enableClicked).toBe(true);
    expect(report.previewClicked).toBe(true);
    expect(report.proceduralPreviewConfirmed).toBe(true);
    expect(report.audibleConfirmedByHuman).toBe(false);
  });
});
