import { describe, expect, it } from "vitest";
import { createIsoCamera } from "../iso3d/isoCamera";
import { createMissingAssetBillboard, createPixelBillboard, orientBillboardToCamera } from "../iso3d/isoBillboard";
import { createIsoGrid } from "../iso3d/isoGrid";
import { createIsoLightSources } from "../iso3d/isoLighting";
import { createCity } from "../sim/city";

describe("Iso3D billboards v1.3.2", () => {
  it("faces camera and uses procedural fallback for missing assets", () => {
    const city = createCity();
    const grid = createIsoGrid(city.width, city.height);
    const lights = createIsoLightSources(city, grid, "vermeer");
    const billboard = createPixelBillboard({
      id: "agent-test",
      kind: "agent",
      label: "Agent",
      position: { x: 0, y: 0, z: 10 },
      spriteKey: "procedural:agent:test",
    }, lights);
    const faced = orientBillboardToCamera(billboard, createIsoCamera("AGENT"));
    expect(faced.facesCamera).toBe(true);
    expect(Number.isFinite(faced.brightness)).toBe(true);
    const missing = createMissingAssetBillboard("missing", { x: 1, y: 2, z: 0 });
    expect(missing.fallback).toBe(true);
    expect(missing.spriteKey).toContain("procedural");
  });
});
