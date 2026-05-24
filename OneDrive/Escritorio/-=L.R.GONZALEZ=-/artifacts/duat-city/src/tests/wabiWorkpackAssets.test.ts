import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import {
  createAssetAllowlistWorkpackDraft,
  createPixelFieldBenchmarkWorkpackDraft,
  createRPGVisualExportWorkpackDraft,
  createVisualAtlasIntegrationWorkpackDraft,
} from "../wabi/workpackDraft";

describe("Wabi asset/visual workpacks v0.7", () => {
  it("keep execution disabled and require owner review where needed", () => {
    const state = createCity();
    const drafts = [
      createAssetAllowlistWorkpackDraft(state),
      createVisualAtlasIntegrationWorkpackDraft(state),
      createPixelFieldBenchmarkWorkpackDraft(state),
      createRPGVisualExportWorkpackDraft(state),
    ];

    for (const draft of drafts) {
      expect(draft.schema).toBe("wabi/duat-city/workpack-draft/v0.7-design");
      expect(draft.execution_allowed).toBe(false);
      expect(draft.sandbox_execution_allowed).toBe(false);
      expect(draft.real_apply_allowed).toBe(false);
      expect(draft.rollback_plan.length).toBeGreaterThan(0);
      expect((draft.target_files ?? draft.suggested_files).length).toBeGreaterThan(0);
    }

    expect(createAssetAllowlistWorkpackDraft(state).owner_review_required).toBe(true);
  });
});
