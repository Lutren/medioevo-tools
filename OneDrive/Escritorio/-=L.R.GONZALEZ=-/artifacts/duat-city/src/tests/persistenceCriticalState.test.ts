import { describe, expect, it, vi } from "vitest";
import { createCity } from "../sim/city";
import { loadFromLocalStorage, saveToLocalStorage } from "../core/persistence";

describe("critical state persistence", () => {
  it("does not store CityState in localStorage", () => {
    const setItem = vi.fn();
    vi.stubGlobal("localStorage", { setItem, getItem: vi.fn(), removeItem: vi.fn() });
    saveToLocalStorage(createCity());
    expect(setItem).not.toHaveBeenCalled();
    expect(loadFromLocalStorage()).toBeNull();
    vi.unstubAllGlobals();
  });
});
