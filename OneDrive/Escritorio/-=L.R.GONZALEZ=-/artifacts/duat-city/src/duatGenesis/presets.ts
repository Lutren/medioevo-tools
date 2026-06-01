/**
 * Fertile and infertile presets for DUAT Genesis field seeding.
 * Each preset is a configuration function that, given a center point,
 * can seed a DuatEngine instance.
 */

import type { DuatEngine } from "./engine";

export type PresetConfig = {
  name: string;
  description: string;
  seedFn: (engine: DuatEngine, cx: number, cy: number) => void;
  expectedState: "fertile" | "infertile";
};

export const PLAYABLE_PRESET: PresetConfig = {
  name: "playable",
  description: "Balanced preset intended for interactive play.",
  seedFn: (engine, cx, cy) => {
    engine.seedDuat(cx, cy);
  },
  expectedState: "fertile",
};

export const FERTILE_PRESETS: PresetConfig[] = [
  {
    name: "osiris-stable",
    description: "Gaussian blob seed producing stable OSIRIS state with high liveness.",
    seedFn: (engine, cx, cy) => {
      engine.seedOsiris(cx, cy);
    },
    expectedState: "fertile",
  },
  {
    name: "duat-ring",
    description: "Ring-seed producing DUAT intermediate state.",
    seedFn: (engine, cx, cy) => {
      engine.seedDuat(cx, cy);
    },
    expectedState: "fertile",
  },
  {
    name: "atum-cluster",
    description: "Hexagonal cluster seed producing ATUM structure.",
    seedFn: (engine, cx, cy) => {
      engine.seedAtum(cx, cy);
    },
    expectedState: "fertile",
  },
];

export const INFERTILE_PRESETS: PresetConfig[] = [
  {
    name: "empty-field",
    description: "No seed; should remain NU (vacuum).",
    seedFn: () => {
      /* no-op */
    },
    expectedState: "infertile",
  },
  {
    name: "conway-glider",
    description: "Conway mode with glider seed; not DUAT.",
    seedFn: (engine, cx, cy) => {
      // Place a simple glider in the middle
      engine.paint(cx + 1, cy, 0, 1);
      engine.paint(cx + 2, cy + 1, 0, 1);
      engine.paint(cx, cy + 2, 0, 1);
      engine.paint(cx + 1, cy + 2, 0, 1);
      engine.paint(cx + 2, cy + 2, 0, 1);
    },
    expectedState: "infertile",
  },
];
