import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createQuaternaryTimingDiagnosticsWorkpackDraft } from "../wabi/workpackDraft";

describe("quaternary Wabi design-only draft", () => {
  it("keeps execution disabled", () => {
    const draft = createQuaternaryTimingDiagnosticsWorkpackDraft(createCity());
    expect(draft.schema).toBe("wabi/duat-city/workpack-draft/v0.9-design");
    expect(draft.workpack_type).toBe("quaternary-timing-diagnostics");
    expect(draft.execution_allowed).toBe(false);
    expect(draft.sandbox_execution_allowed).toBe(false);
    expect(draft.real_apply_allowed).toBe(false);
    expect(draft.owner_review_required).toBe(false);
  });
});

