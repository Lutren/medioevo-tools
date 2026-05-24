import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const physicsUrl = new URL("../../public/asset-manifest/physics_light_zip_manifest_v1_3.json", import.meta.url);

describe("physics/light zip integration v1.3", () => {
  it("candidates are scored, not executed, and selected data is finite", () => {
    const manifest = JSON.parse(readFileSync(physicsUrl, "utf8"));
    expect(manifest.records.length).toBeGreaterThan(0);
    for (const record of manifest.records) {
      expect(record.notes).toMatch(/not executed/i);
      expect(["adapt", "reference_only", "review_required", "reject"]).toContain(record.integration_recommendation);
      expect(Number.isFinite(record.size)).toBe(true);
    }
  });
});
