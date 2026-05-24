import type { TileType } from "../core/types";

export const TILE_COLORS: Record<TileType, string> = {
  empty:       "#1a1f2e",
  road:        "#2d3142",
  plaza:       "#3d4a3e",
  residential: "#2a4a6b",
  workshop:    "#5a3a1a",
  archive:     "#1a3a5a",
  observatory: "#1a2a4a",
  market:      "#4a3a1a",
  clinic:      "#1a4a3a",
  academy:     "#2a1a5a",
  theater:     "#4a2139",
  temple:      "#3a1a4a",
  garden:      "#1a4a2a",
  ruin:        "#3a2a1a",
  gatehouse:   "#3a3a2a",
  water:       "#123a5a",
  forest:      "#123f2a",
  stone:       "#3b4148",
  wall:        "#30333a",
};

export const TILE_BORDER_COLORS: Record<TileType, string> = {
  empty:       "#252b3a",
  road:        "#404560",
  plaza:       "#4d6050",
  residential: "#3a6a8b",
  workshop:    "#7a5a3a",
  archive:     "#3a5a7a",
  observatory: "#3a4a6a",
  market:      "#6a5a3a",
  clinic:      "#3a6a5a",
  academy:     "#4a3a7a",
  theater:     "#7a4264",
  temple:      "#5a3a6a",
  garden:      "#3a6a4a",
  ruin:        "#5a4a3a",
  gatehouse:   "#5a5a4a",
  water:       "#2a6b91",
  forest:      "#28704a",
  stone:       "#69717a",
  wall:        "#777b85",
};

export const TILE_LABELS: Record<TileType, string> = {
  empty: "",
  road: "",
  plaza: "PLZ",
  residential: "RES",
  workshop: "WRK",
  archive: "ARC",
  observatory: "OBS",
  market: "MKT",
  clinic: "CLN",
  academy: "ACM",
  theater: "THR",
  temple: "TMP",
  garden: "GRD",
  ruin: "RIN",
  gatehouse: "GTE",
  water: "WTR",
  forest: "FOR",
  stone: "STN",
  wall: "WAL",
};

export const TILE_ICONS: Record<TileType, string> = {
  empty: "",
  road: "",
  plaza: "⬜",
  residential: "🏠",
  workshop: "⚙️",
  archive: "📚",
  observatory: "🔭",
  market: "🏪",
  clinic: "⚕️",
  academy: "🎓",
  theater: "THR",
  temple: "⛩️",
  garden: "🌿",
  ruin: "🏚️",
  gatehouse: "🚪",
  water: "~",
  forest: "^",
  stone: "#",
  wall: "[]",
};

export const AGENT_ROLE_COLORS: Record<string, string> = {
  Observer:    "#00d4ff",
  Engineer:    "#ff6b35",
  Archivist:   "#7b68ee",
  Medic:       "#00ff9d",
  Builder:     "#ffa500",
  Trader:      "#ffff00",
  Teacher:     "#ff69b4",
  Scout:       "#adff2f",
  Gatekeeper:  "#dc143c",
  Storykeeper: "#9370db",
  Artisan:     "#ff8c00",
  Courier:     "#20b2aa",
  Psychologist: "#ff7ab6",
};

export const GATE_COLORS: Record<string, string> = {
  APPROVE: "#00ff9d",
  REVIEW:  "#ffcc00",
  BLOCK:   "#ff4444",
};

export const REGIME_COLORS: Record<string, string> = {
  OPTIMO:    "#00ff9d",
  FUNCIONAL: "#7bc8f6",
  CARGADO:   "#ffcc00",
  SATURADO:  "#ff4444",
};

export function rColor(R: number): string {
  if (R < 0.2) return "#00ff9d";
  if (R < 0.4) return "#adff2f";
  if (R < 0.6) return "#ffcc00";
  if (R < 0.8) return "#ff6b35";
  return "#ff4444";
}

export function heatmapColor(R: number, alpha = 0.55): string {
  if (R < 0.2) return `rgba(0,255,157,${alpha})`;
  if (R < 0.4) return `rgba(173,255,47,${alpha})`;
  if (R < 0.6) return `rgba(255,204,0,${alpha})`;
  if (R < 0.8) return `rgba(255,107,53,${alpha})`;
  return `rgba(255,68,68,${alpha})`;
}
