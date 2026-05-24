import { describe, expect, it } from "vitest";
import { createLightGrid } from "../light/lightGrid";
import { applyLightBudget, lightBudgetForPreset, lightUpdateBucket, shouldDropLowIntensityCell } from "../light/lightBudget";
import { computeLightMetrics } from "../light/lightMetrics";

describe("light budget v1.1.1", () => {
  it("caps active cells deterministically", () => {
    const grid = createLightGrid(80, 45, { r: 120, g: 120, b: 120 });
    const budget = { ...lightBudgetForPreset("LOW"), activeLightCellCap: 120 };
    applyLightBudget(grid, budget);
    const metrics = computeLightMetrics(grid);
    expect(metrics.activeLightCells).toBeLessThanOrEqual(120);
  });

  it("respects preset quality budgets", () => {
    expect(lightBudgetForPreset("LOW").activeLightCellCap).toBeLessThan(lightBudgetForPreset("HIGH").activeLightCellCap);
    expect(lightBudgetForPreset("BEAUTIFUL").maxBouncePasses).toBeGreaterThanOrEqual(lightBudgetForPreset("HIGH").maxBouncePasses);
  });

  it("early exits low intensity cells", () => {
    const budget = lightBudgetForPreset("MEDIUM");
    expect(shouldDropLowIntensityCell(budget.intensityThreshold / 2, budget)).toBe(true);
    expect(shouldDropLowIntensityCell(budget.intensityThreshold + 0.2, budget)).toBe(false);
  });

  it("cadence bucket is deterministic and finite", () => {
    const budget = lightBudgetForPreset("HIGH");
    expect(lightUpdateBucket(0, budget)).toBe(0);
    expect(lightUpdateBucket(11, budget)).toBe(0);
    expect(lightUpdateBucket(12, budget)).toBe(1);
    expect(Number.isFinite(lightUpdateBucket(120, budget))).toBe(true);
  });
});
