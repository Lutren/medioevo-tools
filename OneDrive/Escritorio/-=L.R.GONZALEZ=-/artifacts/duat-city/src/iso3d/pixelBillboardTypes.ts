import type { Gate } from "../core/types";
import type { IsoBillboard } from "./isoTypes";

export interface PixelBillboardPalette {
  agent: string;
  building: string;
  water: string;
  fire: string;
  smoke: string;
  neon: string;
  q00: string;
  q01: string;
  q10: string;
  q11: string;
}

export interface PixelBillboardPopulation {
  agents: IsoBillboard[];
  buildings: IsoBillboard[];
  props: IsoBillboard[];
  materials: IsoBillboard[];
  qglyphs: IsoBillboard[];
}

export interface PixelBillboardStateTag {
  R: number;
  Phi_eff: number;
  gate: Gate;
  qState?: "00" | "01" | "10" | "11";
}

export const DEFAULT_PIXEL_BILLBOARD_PALETTE: PixelBillboardPalette = {
  agent: "#d7c49a",
  building: "#8f7659",
  water: "#4b9ad4",
  fire: "#ff8e3c",
  smoke: "#8b8d93",
  neon: "#52f0ff",
  q00: "#8aa38a",
  q01: "#d6b85a",
  q10: "#6cc1d8",
  q11: "#dd6a6a",
};
