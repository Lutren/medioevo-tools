import { describe, expect, it } from "vitest";
import { QuaternarySensorBank } from "../quaternary";

describe("quaternary sensor bank", () => {
  it("persists source state", () => {
    const bank = new QuaternarySensorBank({ windowSize: 8 });
    bank.evaluate({ sourceId: "agent:a", sourceKind: "agent", tick: 1, presence: true, difference: false });
    bank.evaluate({ sourceId: "agent:a", sourceKind: "agent", tick: 2, presence: true, difference: false });
    expect(bank.get("agent:a")?.getStats().dwellTicks).toBe(2);
  });

  it("keeps multiple sources independent", () => {
    const bank = new QuaternarySensorBank({ windowSize: 8 });
    bank.evaluate({ sourceId: "agent:a", sourceKind: "agent", tick: 1, presence: true, difference: false });
    bank.evaluate({ sourceId: "agent:b", sourceKind: "agent", tick: 1, presence: false, difference: true });
    expect(bank.get("agent:a")?.getStats().current).toBe("10");
    expect(bank.get("agent:b")?.getStats().current).toBe("01");
  });

  it("reset works per source and globally", () => {
    const bank = new QuaternarySensorBank({ windowSize: 8 });
    bank.evaluate({ sourceId: "a", sourceKind: "system", tick: 1, presence: true, difference: true });
    bank.evaluate({ sourceId: "b", sourceKind: "system", tick: 1, presence: true, difference: false });
    bank.reset("a");
    expect(bank.get("a")).toBeUndefined();
    expect(bank.get("b")).toBeDefined();
    bank.reset();
    expect(bank.get("b")).toBeUndefined();
  });
});

