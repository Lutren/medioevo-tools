import { describe, expect, it } from "vitest";
import { stepPixelField } from "../physicsField/cellularPhysics";
import { createPixelField, getCell, setCellMutable } from "../physicsField/pixelField";

describe("pixel field QA v0.7", () => {
  it("water falls, smoke rises, fire emits smoke/light and inactive cells skip", () => {
    let field = createPixelField(10, 10, "air");
    setCellMutable(field, 2, 2, "water", true);
    setCellMutable(field, 4, 7, "smoke", true);
    setCellMutable(field, 7, 5, "fire", true);

    const result = stepPixelField(field);
    expect(getCell(result.field, 2, 3)?.material).toBe("water");
    const smokeRows = result.field.cells
      .map((cell, index) => ({ cell, y: Math.floor(index / result.field.width) }))
      .filter(entry => entry.cell.material === "smoke")
      .map(entry => entry.y);
    expect(Math.min(...smokeRows)).toBeLessThan(7);
    expect(result.field.cells.some(cell => cell.material === "light" || cell.light > 0)).toBe(true);
    expect(result.metrics.skippedCells).toBeGreaterThan(0);
  });
});
