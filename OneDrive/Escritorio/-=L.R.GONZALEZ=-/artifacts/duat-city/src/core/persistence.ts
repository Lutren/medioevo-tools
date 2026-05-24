import type { CityState } from "./types";

const SAVE_KEY = "duat-city-save";
const PREFS_KEY = "duat-city-prefs";

export function saveCityToJson(state: CityState): string {
  return JSON.stringify({
    schema: "duat-agent-city/save/v1",
    savedAt: Date.now(),
    state,
  }, null, 2);
}

export function loadCityFromJson(json: string): CityState | null {
  try {
    const parsed = JSON.parse(json);
    if (!parsed.state) return null;
    return parsed.state as CityState;
  } catch {
    return null;
  }
}

export function saveToLocalStorage(state: CityState): void {
  void state;
}

export function loadFromLocalStorage(): CityState | null {
  return null;
}

export interface UIPrefs {
  showHeatmap: boolean;
  showFibmob: boolean;
  showAgentLabels: boolean;
  speed: number;
}

export const DEFAULT_PREFS: UIPrefs = {
  showHeatmap: false,
  showFibmob: false,
  showAgentLabels: true,
  speed: 1,
};

export function savePrefs(prefs: UIPrefs): void {
  try { localStorage.setItem(PREFS_KEY, JSON.stringify(prefs)); } catch { /* ignore */ }
}

export function loadPrefs(): UIPrefs {
  try {
    const raw = localStorage.getItem(PREFS_KEY);
    if (!raw) return DEFAULT_PREFS;
    return { ...DEFAULT_PREFS, ...JSON.parse(raw) };
  } catch { return DEFAULT_PREFS; }
}

export function downloadJson(filename: string, content: string): void {
  const blob = new Blob([content], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
