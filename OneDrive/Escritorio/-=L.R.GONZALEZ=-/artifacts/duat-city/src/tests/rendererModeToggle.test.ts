import { describe, expect, it } from "vitest";
import { resolveRendererMode } from "../components/RendererModeToggle";

describe("renderer mode toggle v1.3.2", () => {
  it("preserves Canvas fallback and enables Iso3D only by flag", () => {
    const canvas = resolveRendererMode("canvas", false);
    expect(canvas.canvasFallback).toBe(true);
    expect(canvas.isoEnabled).toBe(false);
    const iso = resolveRendererMode("iso3d", true);
    expect(iso.isoEnabled).toBe(true);
    expect(iso.canvasFallback).toBe(false);
  });
});
