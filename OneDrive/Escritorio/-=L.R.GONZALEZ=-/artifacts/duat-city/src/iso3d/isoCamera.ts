import type { Mode } from "../core/types";
import type { IsoCamera, IsoVector3 } from "./isoTypes";

export function createIsoCamera(mode: Mode | "HORMIGUERO" | "PRESIDENT" | "METROIDVANIA" = "CITY"): IsoCamera {
  const presets: Record<string, Pick<IsoCamera, "position" | "target" | "zoom" | "yaw" | "pitch">> = {
    CITY: { position: { x: 0, y: -360, z: 280 }, target: { x: 0, y: 0, z: 0 }, zoom: 1, yaw: 45, pitch: 35 },
    AGENT: { position: { x: 0, y: -120, z: 90 }, target: { x: 0, y: 0, z: 16 }, zoom: 2.4, yaw: 45, pitch: 28 },
    RPG: { position: { x: 0, y: -260, z: 180 }, target: { x: 0, y: 0, z: 0 }, zoom: 1.35, yaw: 45, pitch: 32 },
    OSIT: { position: { x: 0, y: -420, z: 330 }, target: { x: 0, y: 0, z: 0 }, zoom: 0.82, yaw: 45, pitch: 38 },
    HORMIGUERO: { position: { x: 0, y: -650, z: 520 }, target: { x: 0, y: 0, z: 0 }, zoom: 0.58, yaw: 45, pitch: 42 },
    PRESIDENT: { position: { x: 0, y: -520, z: 400 }, target: { x: 0, y: 0, z: 0 }, zoom: 0.72, yaw: 45, pitch: 40 },
    METROIDVANIA: { position: { x: 0, y: -80, z: 80 }, target: { x: 0, y: 0, z: 0 }, zoom: 1.6, yaw: 0, pitch: 0 },
  };
  return { ...presets[mode], modePreset: mode };
}

export function zoomIsoCamera(camera: IsoCamera, delta: number): IsoCamera {
  const zoom = clamp(safe(camera.zoom, 1) + safe(delta, 0), 0.35, 4);
  return { ...camera, zoom: round(zoom) };
}

export function panIsoCamera(camera: IsoCamera, offset: Partial<IsoVector3>): IsoCamera {
  return {
    ...camera,
    target: {
      x: round(camera.target.x + safe(offset.x, 0)),
      y: round(camera.target.y + safe(offset.y, 0)),
      z: round(camera.target.z + safe(offset.z, 0)),
    },
  };
}

export function focusIsoCamera(camera: IsoCamera, target: IsoVector3, zoom = camera.zoom): IsoCamera {
  return {
    ...camera,
    target: { x: round(safe(target.x, 0)), y: round(safe(target.y, 0)), z: round(safe(target.z, 0)) },
    zoom: round(clamp(safe(zoom, camera.zoom), 0.35, 4)),
  };
}

function safe(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function round(value: number): number {
  return Number(value.toFixed(3));
}
