export const DRAW_LAYERS = [
  "terrain",
  "roads-buildings",
  "r-phi-heatmap",
  "fibmob-overlay",
  "agents",
  "particles-effects",
  "selection-ui",
] as const;

export type DrawLayer = typeof DRAW_LAYERS[number];
