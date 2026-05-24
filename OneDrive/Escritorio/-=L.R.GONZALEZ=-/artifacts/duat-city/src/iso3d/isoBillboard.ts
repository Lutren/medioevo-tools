import type { IsoBillboard, IsoCamera, IsoLightSource, IsoVector3 } from "./isoTypes";
import { computeIsoDepth } from "./isoGrid";
import { sampleIsoLighting, shadeIsoColor } from "./isoLighting";

export interface BillboardInput {
  id: string;
  kind: IsoBillboard["kind"];
  label: string;
  position: IsoVector3;
  spriteKey?: string;
  tint?: string;
  width?: number;
  height?: number;
  selected?: boolean;
  hoverable?: boolean;
  metadata?: Record<string, string | number | boolean>;
}

export function createPixelBillboard(input: BillboardInput, lights: IsoLightSource[] = []): IsoBillboard {
  const brightness = sampleIsoLighting(input.position, lights);
  const tint = shadeIsoColor(input.tint ?? "#d7c49a", brightness);
  return {
    id: input.id,
    kind: input.kind,
    label: input.label,
    position: input.position,
    size: { x: finite(input.width, 18), y: finite(input.height, 28) },
    anchor: { x: 0.5, y: 1 },
    spriteKey: input.spriteKey ?? `procedural:${input.kind}`,
    tint,
    brightness: round(brightness),
    facesCamera: true,
    selected: Boolean(input.selected),
    hoverable: input.hoverable ?? true,
    depth: computeIsoDepth(input.position),
    fallback: true,
    metadata: input.metadata ?? {},
  };
}

export function orientBillboardToCamera(billboard: IsoBillboard, camera: IsoCamera): IsoBillboard {
  const dx = camera.position.x - billboard.position.x;
  const dy = camera.position.y - billboard.position.y;
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;
  return {
    ...billboard,
    facesCamera: true,
    metadata: { ...billboard.metadata, cameraFacingDegrees: round(Number.isFinite(angle) ? angle : 0) },
  };
}

export function createMissingAssetBillboard(id: string, position: IsoVector3): IsoBillboard {
  return createPixelBillboard({
    id,
    kind: "prop",
    label: "procedural fallback",
    position,
    spriteKey: "procedural:missing-safe",
    tint: "#c9b37d",
    width: 16,
    height: 16,
    metadata: { missingAssetFallback: true },
  });
}

function finite(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function round(value: number): number {
  return Number(value.toFixed(3));
}
