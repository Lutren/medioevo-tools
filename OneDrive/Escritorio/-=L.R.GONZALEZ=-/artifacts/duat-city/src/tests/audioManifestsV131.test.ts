import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const audioUrl = new URL("../../public/asset-manifest/audio_gamefeel_manifest_v1_3_1.json", import.meta.url);
const agentsUrl = new URL("../../public/asset-manifest/agents_gamefeel_manifest_v1_3_1.json", import.meta.url);
const assetsUrl = new URL("../../public/asset-manifest/assets_gamefeel_manifest_v1_3_1.json", import.meta.url);

describe("audio/game-feel manifests v1.3.1", () => {
  it("keeps audio, agent and asset manifests internal and non-public", () => {
    const manifests = [audioUrl, agentsUrl, assetsUrl].map(url => JSON.parse(readFileSync(url, "utf8")));
    expect(manifests.every(manifest => manifest.fingerprint === "DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY")).toBe(true);
    expect(JSON.stringify(manifests)).not.toMatch(/publicationAllowed\"\\s*:\\s*true|externalSamplesCopied\"\\s*:\\s*true|wabiExecutionAllowed\"\\s*:\\s*true/);
    expect(manifests[0].boundary.requiresUserGesture).toBe(true);
    expect(manifests[2].boundary.newAssetsCopied).toBe(false);
  });
});
