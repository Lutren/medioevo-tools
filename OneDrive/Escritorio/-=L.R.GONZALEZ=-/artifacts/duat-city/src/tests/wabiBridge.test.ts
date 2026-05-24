import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { getWabiMcpStatus } from "../wabi/mcpDesignBridge";
import { createWorkpackDraftFromCity } from "../wabi/workpackDraft";
import { toWabiHandoff } from "../wabi/wabiHandoff";

describe("Wabi MCP design-only bridge", () => {
  it("status is design-only and execution disabled", () => {
    const status = getWabiMcpStatus();
    expect(status.version).toBe("v0.5-design");
    expect(status.gated_write_enabled).toBe(false);
    expect(status.execution_allowed).toBe(false);
    expect(status.real_apply_allowed).toBe(false);
  });

  it("workpack draft has rollback", () => {
    const draft = createWorkpackDraftFromCity(createCity());
    expect(draft.rollback_plan.length).toBeGreaterThan(0);
  });

  it("handoff schema is valid and non-executing", () => {
    const handoff = toWabiHandoff({ state: createCity() });
    expect(handoff.schema).toBe("wabi/duat-city/handoff/v0.5-design");
    expect(handoff.execution_allowed).toBe(false);
    expect(handoff.next_safe_action).toBe("prepare-only review; no execution");
  });
});
