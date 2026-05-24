import type { ResourceKey } from "../core/types";
import { clamp } from "../core/math";

export const RESOURCE_MAX: Record<ResourceKey, number> = {
  food: 200,
  materials: 200,
  knowledge: 200,
  trust: 100,
  signal: 100,
  energy: 200,
  culture: 100,
};

export const RESOURCE_LABELS: Record<ResourceKey, string> = {
  food: "Food",
  materials: "Materials",
  knowledge: "Knowledge",
  trust: "Trust",
  signal: "Signal",
  energy: "Energy",
  culture: "Culture",
};

export const RESOURCE_ICONS: Record<ResourceKey, string> = {
  food: "🌾",
  materials: "⚙️",
  knowledge: "📚",
  trust: "🤝",
  signal: "📡",
  energy: "⚡",
  culture: "🎭",
};

export const ALL_RESOURCES: ResourceKey[] = [
  "food", "materials", "knowledge", "trust", "signal", "energy", "culture",
];

export function makeDefaultResources(): Record<ResourceKey, number> {
  return { food: 80, materials: 60, knowledge: 40, trust: 60, signal: 30, energy: 100, culture: 20 };
}

export function applyResourceDelta(
  resources: Record<ResourceKey, number>,
  delta: Partial<Record<ResourceKey, number>>
): Record<ResourceKey, number> {
  const result = { ...resources };
  for (const [key, amount] of Object.entries(delta)) {
    const k = key as ResourceKey;
    result[k] = clamp((result[k] ?? 0) + (amount ?? 0), 0, RESOURCE_MAX[k]);
  }
  return result;
}

export function getResourceShortage(resources: Record<ResourceKey, number>): string[] {
  const shortages: string[] = [];
  if (resources.food < 20) shortages.push("food");
  if (resources.materials < 15) shortages.push("materials");
  if (resources.knowledge < 10) shortages.push("knowledge");
  if (resources.trust < 15) shortages.push("trust");
  if (resources.energy < 20) shortages.push("energy");
  return shortages;
}

export function computeResourceR(resources: Record<ResourceKey, number>): number {
  let r = 0;
  if (resources.food < 20) r += 0.1;
  if (resources.materials < 15) r += 0.08;
  if (resources.knowledge < 10) r += 0.05;
  if (resources.trust < 15) r += 0.08;
  if (resources.energy < 20) r += 0.06;
  return Math.min(0.4, r);
}
