import type { RenderQualityPreset } from "../pixelRealism/renderPasses";
import type { LightGrid } from "./lightTypes";

export interface LightBudget {
  preset: RenderQualityPreset;
  activeLightCellCap: number;
  particleCap: number;
  updateCadenceFrames: number;
  intensityThreshold: number;
  maxBouncePasses: number;
  reflectionScale: number;
}

export const LIGHT_BUDGETS: Record<RenderQualityPreset, LightBudget> = {
  LOW: {
    preset: "LOW",
    activeLightCellCap: 1800,
    particleCap: 24,
    updateCadenceFrames: 23,
    intensityThreshold: 0.11,
    maxBouncePasses: 0,
    reflectionScale: 0.35,
  },
  MEDIUM: {
    preset: "MEDIUM",
    activeLightCellCap: 7200,
    particleCap: 56,
    updateCadenceFrames: 23,
    intensityThreshold: 0.10,
    maxBouncePasses: 1,
    reflectionScale: 0.55,
  },
  HIGH: {
    preset: "HIGH",
    activeLightCellCap: 20000,
    particleCap: 96,
    updateCadenceFrames: 12,
    intensityThreshold: 0.095,
    maxBouncePasses: 1,
    reflectionScale: 0.72,
  },
  BEAUTIFUL: {
    preset: "BEAUTIFUL",
    activeLightCellCap: 28000,
    particleCap: 128,
    updateCadenceFrames: 12,
    intensityThreshold: 0.09,
    maxBouncePasses: 2,
    reflectionScale: 0.85,
  },
  DEBUG: {
    preset: "DEBUG",
    activeLightCellCap: 9000,
    particleCap: 72,
    updateCadenceFrames: 23,
    intensityThreshold: 0.08,
    maxBouncePasses: 1,
    reflectionScale: 0.6,
  },
};

export function lightBudgetForPreset(preset: RenderQualityPreset): LightBudget {
  return LIGHT_BUDGETS[preset] ?? LIGHT_BUDGETS.MEDIUM;
}

export function lightUpdateBucket(frame: number, budget: LightBudget): number {
  const cadence = Math.max(1, budget.updateCadenceFrames);
  return Math.floor(Math.max(0, frame) / cadence);
}

export function shouldDropLowIntensityCell(intensity: number, budget: LightBudget): boolean {
  if (!Number.isFinite(intensity)) return true;
  return intensity < budget.intensityThreshold;
}

export function applyLightBudget(grid: LightGrid, budget: LightBudget): LightGrid {
  const candidates: Array<{ index: number; score: number }> = [];
  for (let index = 0; index < grid.cells.length; index++) {
    const cell = grid.cells[index];
    if (!Number.isFinite(cell.intensity)) {
      cell.intensity = 0;
      cell.dirty = true;
    }
    const emissionScore = (cell.emission.r + cell.emission.g + cell.emission.b) / 765;
    const score = cell.intensity + cell.reflectance * 0.35 + cell.scatter * 0.25 + emissionScore;
    if (score > 0.08 && !shouldDropLowIntensityCell(score, budget)) {
      candidates.push({ index, score });
    } else {
      cell.intensity = Math.min(cell.intensity, 0.079);
      cell.dirty = false;
    }
  }

  if (candidates.length > budget.activeLightCellCap) {
    candidates.sort((a, b) => b.score - a.score || a.index - b.index);
    const allowed = new Set(candidates.slice(0, budget.activeLightCellCap).map(item => item.index));
    for (const candidate of candidates) {
      if (allowed.has(candidate.index)) continue;
      const cell = grid.cells[candidate.index];
      cell.intensity = Math.min(cell.intensity, 0.079);
      cell.dirty = false;
    }
  }

  grid.budget = {
    activeLightCellCap: budget.activeLightCellCap,
    particleCap: budget.particleCap,
    intensityThreshold: budget.intensityThreshold,
    updateCadenceFrames: budget.updateCadenceFrames,
    reflectionScale: budget.reflectionScale,
  };
  return grid;
}
