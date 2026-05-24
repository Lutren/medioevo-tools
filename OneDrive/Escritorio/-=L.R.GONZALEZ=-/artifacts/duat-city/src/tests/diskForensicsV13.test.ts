import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { createAssetRecord } from "../forensics/localAssetScanner";
import { createZipEntryRecord } from "../forensics/zipInventory";
import { scanCodeCandidates } from "../forensics/codeCandidateScanner";

const manifestUrl = new URL("../../public/asset-manifest/assets_du_wabi_manifest_v1_3.json", import.meta.url);
const audioUrl = new URL("../../public/asset-manifest/audio_zip_manifest_v1_3.json", import.meta.url);
const physicsUrl = new URL("../../public/asset-manifest/physics_light_zip_manifest_v1_3.json", import.meta.url);
const brainUrl = new URL("../../public/asset-manifest/brain_os_zip_manifest_v1_3.json", import.meta.url);
const codeUrl = new URL("../../public/asset-manifest/code_candidates_v1_3.json", import.meta.url);

describe("disk forensics v1.3", () => {
  it("manifests parse and zips were inventoried without execution", () => {
    for (const url of [manifestUrl, audioUrl, physicsUrl, brainUrl, codeUrl]) {
      const manifest = JSON.parse(readFileSync(url, "utf8"));
      expect(manifest.fingerprint).toBe("DUAT-v1.3-GAME-OS-DISK-FORENSICS-LANGUAGE-CORTEX");
      expect(manifest.boundary.unknown_code_executed).toBe(false);
      expect(manifest.boundary.publication_allowed).toBe(false);
      expect(Array.isArray(manifest.records)).toBe(true);
    }
  });

  it("no copied asset lacks provenance", () => {
    const manifest = JSON.parse(readFileSync(manifestUrl, "utf8"));
    for (const record of manifest.records) {
      expect(record.path_original || record.original_path).toBeTruthy();
      expect(record.copy_status).not.toBe("copied_internal_review");
      expect(record.license_status ?? "unknown").not.toBe("reviewed");
    }
  });

  it("classifies sample asset and code candidates safely", () => {
    const asset = createAssetRecord("Assets Du WABI/neon-water-tile.png", 2048, "Assets Du WABI");
    expect(asset?.copy_status).toBe("not_copied");
    const zipRecord = createZipEntryRecord({ path: "src/audio/worklet.ts", size: 300 }, "audio.zip");
    const candidates = scanCodeCandidates([zipRecord]);
    expect(candidates[0].safe_to_execute).toBe(false);
    expect(candidates[0].integration_recommendation).toBe("adapt");
  });
});
