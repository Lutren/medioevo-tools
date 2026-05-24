import { describe, expect, it } from "vitest";
import { ditherAndQuantize, orderedDither, quantizeToPalette } from "../color/dither";

describe("pixel dithering v1.0", () => {
  it("is deterministic", () => {
    const a = orderedDither({ r: 120, g: 130, b: 140 }, 7, 11, { matrix: "bayer4", strength: 12 });
    const b = orderedDither({ r: 120, g: 130, b: 140 }, 7, 11, { matrix: "bayer4", strength: 12 });
    expect(a).toEqual(b);
  });

  it("limits colors to the palette", () => {
    const palette = [{ r: 0, g: 0, b: 0 }, { r: 255, g: 200, b: 120 }, { r: 40, g: 220, b: 255 }];
    const q = quantizeToPalette({ r: 240, g: 190, b: 110 }, palette);
    const d = ditherAndQuantize({ r: 38, g: 210, b: 250 }, 2, 3, palette);
    expect(palette).toContainEqual(q);
    expect(palette).toContainEqual(d);
  });
});
