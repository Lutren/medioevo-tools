import { describe, expect, it } from "vitest";
import { decodeQState, encodeQState, qStateMeaning, qStateToIndex } from "../quaternary";

describe("quaternary qstate", () => {
  it("encodes and decodes all states", () => {
    expect(encodeQState(false, false)).toBe("00");
    expect(encodeQState(false, true)).toBe("01");
    expect(encodeQState(true, false)).toBe("10");
    expect(encodeQState(true, true)).toBe("11");
    expect(decodeQState("00")).toEqual({ presence: false, difference: false });
    expect(decodeQState("01")).toEqual({ presence: false, difference: true });
    expect(decodeQState("10")).toEqual({ presence: true, difference: false });
    expect(decodeQState("11")).toEqual({ presence: true, difference: true });
  });

  it("maps indexes in bit order", () => {
    expect(qStateToIndex("00")).toBe(0);
    expect(qStateToIndex("01")).toBe(1);
    expect(qStateToIndex("10")).toBe(2);
    expect(qStateToIndex("11")).toBe(3);
  });

  it("returns operational meanings", () => {
    expect(qStateMeaning("00")).toBe("SILENCE_STABLE");
    expect(qStateMeaning("01")).toBe("ABSENCE_SIGNIFICANT");
    expect(qStateMeaning("10")).toBe("PRESENCE_STABLE");
    expect(qStateMeaning("11")).toBe("EVENT_ACTIVE");
  });
});

