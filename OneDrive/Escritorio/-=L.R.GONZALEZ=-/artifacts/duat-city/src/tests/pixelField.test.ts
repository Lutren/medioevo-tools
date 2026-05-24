import { describe, expect, it } from "vitest";
import { stepPixelField } from "../physicsField/cellularPhysics";
import { computeFieldMetrics } from "../physicsField/fieldMetrics";
import { createPixelField, getCell, setCellMutable } from "../physicsField/pixelField";

describe("pixel physics field", () => {
  it("water falls", () => {
    const field = createPixelField(8, 8, "air");
    setCellMutable(field, 3, 2, "water", true);
    const result = stepPixelField(field);
    expect(getCell(result.field, 3, 3)?.material).toBe("water");
  });

  it("smoke rises", () => {
    const field = createPixelField(8, 8, "air");
    setCellMutable(field, 4, 5, "smoke", true);
    const result = stepPixelField(field);
    const smokeIndex = result.field.cells.findIndex(cell => cell.material === "smoke");
    expect(Math.floor(smokeIndex / result.field.width)).toBeLessThan(5);
  });

  it("fire creates smoke", () => {
    const field = createPixelField(8, 8, "air");
    setCellMutable(field, 2, 3, "fire", true);
    const result = stepPixelField(field);
    const smokeCount = result.field.cells.filter(cell => cell.material === "smoke").length;
    expect(smokeCount).toBeGreaterThan(0);
  });

  it("inactive cells are skipped and values are finite", () => {
    const field = createPixelField(8, 8, "air");
    const result = stepPixelField(field);
    expect(result.metrics.updatedCells).toBe(0);
    expect(result.metrics.skippedCells).toBeGreaterThan(0);
    for (const value of Object.values(result.metrics)) {
      expect(Number.isFinite(value)).toBe(true);
    }
  });

  it("R_field rises with unresolved active cells", () => {
    const calm = createPixelField(8, 8, "air");
    const loaded = createPixelField(8, 8, "air");
    for (let x = 0; x < 8; x++) setCellMutable(loaded, x, 7, "water", true);
    const calmMetrics = computeFieldMetrics(calm, 0, 0);
    const loadedMetrics = computeFieldMetrics(loaded, 0, 8);
    expect(loadedMetrics.R_field).toBeGreaterThan(calmMetrics.R_field);
  });
});
