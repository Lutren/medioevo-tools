import type { Direction } from "../core/types";

export type ViewMode = "OPERATIONAL" | "BEAUTIFUL" | "DEBUG";

export interface GraphicsBudget {
  tileDetail: 0 | 1 | 2;
  agentDetail: 0 | 1 | 2;
  particlesEnabled: boolean;
  shadowsEnabled: boolean;
  heatmapEnabled: boolean;
  chunkMode: "FULL" | "DIRTY";
  direction: Direction;
  reason: string;
}

export interface GraphicsMetrics {
  direction: Direction;
  chunksRendered: number;
  dirtyChunks: number;
  particlesCount: number;
  renderBudget: string;
  R_graphics: number;
  Phi_graphics: number;
  quaternaryGate?: string;
}

export interface DirtyChunk {
  x: number;
  y: number;
  key: string;
}

export interface Particle {
  id: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  age: number;
  ttl: number;
  kind: "task" | "production" | "block" | "anomaly";
}
