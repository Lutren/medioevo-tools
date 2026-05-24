import { describe, expect, it } from "vitest";
import { createIsoCamera, focusIsoCamera, panIsoCamera, zoomIsoCamera } from "../iso3d/isoCamera";

describe("Iso3D camera v1.3.2", () => {
  it("produces finite camera presets and zoom/pan values", () => {
    for (const mode of ["CITY", "AGENT", "RPG", "OSIT", "HORMIGUERO", "PRESIDENT"] as const) {
      const camera = createIsoCamera(mode);
      expect(Number.isFinite(camera.zoom)).toBe(true);
      expect(Number.isFinite(camera.position.z)).toBe(true);
      const zoomed = zoomIsoCamera(camera, 0.25);
      const panned = panIsoCamera(zoomed, { x: 4, y: -2 });
      const focused = focusIsoCamera(panned, { x: 1, y: 2, z: 3 }, 1.5);
      expect(focused.zoom).toBeGreaterThan(0);
      expect(Number.isFinite(focused.target.x)).toBe(true);
    }
  });
});
