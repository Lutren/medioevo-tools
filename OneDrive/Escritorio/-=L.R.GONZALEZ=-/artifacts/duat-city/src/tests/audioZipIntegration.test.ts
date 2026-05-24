import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const audioUrl = new URL("../../public/asset-manifest/audio_zip_manifest_v1_3.json", import.meta.url);

describe("audio zip integration v1.3", () => {
  it("audio candidate manifest is valid and no unknown license is approved", () => {
    const manifest = JSON.parse(readFileSync(audioUrl, "utf8"));
    expect(manifest.boundary.unknown_code_executed).toBe(false);
    expect(JSON.stringify(manifest)).not.toMatch(/auto-download|publication_allowed\"\\s*:\\s*true/i);
    for (const record of manifest.records) {
      expect(record.copy_status).toBe("staged_metadata_only");
      expect(record.integration_recommendation).not.toBe("adopt");
    }
  });
});
