import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const reportUrl = new URL("../../docs/AUDIO_HEADED_QA_REPORT_v1_3_2.json", import.meta.url);

describe("audio headed QA v1.3.2", () => {
  it("keeps audio off by default and records headed/fallback status", () => {
    const report = JSON.parse(readFileSync(reportUrl, "utf8"));
    expect(report.schema).toBe("duat/audio-headed-qa/v1.3.2");
    expect(report.fingerprint).toBe("DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT");
    expect(report.audioOffByDefault).toBe(true);
    expect(report.previewRequiresEnableFlag).toBe(true);
    expect(report.focusStatus).toBeTruthy();
    expect(report.boundary.autoplay).toBe(false);
    expect(report.boundary.externalSamplesCopied).toBe(false);
    expect(report.boundary.cloudUsed).toBe(false);
    expect(report.boundary.wabiExecution).toBe(false);
  });
});
