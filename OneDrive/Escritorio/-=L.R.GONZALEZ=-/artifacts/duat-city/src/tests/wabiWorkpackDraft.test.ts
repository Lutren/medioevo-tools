import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import {
  createAssetWorkpackDraft,
  createGraphicsUpgradeWorkpackDraft,
  createPhysicsFieldWorkpackDraft,
  createRPGExportWorkpackDraft,
} from "../wabi/workpackDraft";

describe("Wabi v0.6 workpack drafts", () => {
  it("keep execution disabled and include rollback/targets", () => {
    const state = createCity();
    const drafts = [
      createAssetWorkpackDraft(state),
      createGraphicsUpgradeWorkpackDraft(state),
      createPhysicsFieldWorkpackDraft(state),
      createRPGExportWorkpackDraft(state),
    ];
    for (const draft of drafts) {
      expect(draft.execution_allowed).toBe(false);
      expect(draft.real_apply_allowed).toBe(false);
      expect(draft.rollback_plan.length).toBeGreaterThan(0);
      expect((draft.target_files ?? draft.suggested_files).length).toBeGreaterThan(0);
    }
  });
});
