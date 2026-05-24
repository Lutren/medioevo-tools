import type { Camera } from "./camera";
import { muK } from "../core/fibmob";
import { emlForCity } from "../core/eml";
import type { PhysicsMetrics } from "../physics/types";

export interface LODStateV2 {
  renderAgents: boolean;
  renderLabels: boolean;
  renderIcons: boolean;
  renderHeatmap: boolean;
  renderParticles: boolean;
  renderPhysicsDebug: boolean;
  agentRadius: number;
  tileDetail: number;
  chunkSize: number;
  updateStride: number;
  direction: "EXPAND" | "HOLD" | "COMPRESS";
  tickType: "compressed" | "normal" | "prime" | "event";
  reason: string;
  R_lod: number;
  Phi_lod: number;
}

export interface ComputeLODV2Input {
  camera: Camera;
  R: number;
  Phi_eff: number;
  tick: number;
  physicsMetrics?: PhysicsMetrics;
  showPhysicsDebug?: boolean;
}

export function computeLODV2(input: ComputeLODV2Input): LODStateV2 {
  const zoom = input.camera.zoom;
  const physicsR = input.physicsMetrics?.R_physics ?? 0;
  const mu = muK(Math.max(1, input.tick), 1);
  const tickType = classifyTick(input.tick, mu);
  const eml = emlForCity(input.Phi_eff, input.R);

  let direction = eml.direction;
  let reason = `EML ${eml.direction}`;
  if (input.R > 0.60 || physicsR > 0.60 || tickType === "compressed") {
    direction = "COMPRESS";
    reason = input.R > 0.60 ? "global R high" : physicsR > 0.60 ? "physics R high" : "FibMob compressed tick";
  } else if (input.R < 0.20 && input.Phi_eff > 0.75) {
    direction = "EXPAND";
    reason = "low R high Phi_eff";
  }

  const compressed = direction === "COMPRESS";
  const expanded = direction === "EXPAND";
  const R_lod = Math.max(input.R, physicsR);
  const Phi_lod = Math.max(0, Math.min(1, input.Phi_eff * (1 - physicsR * 0.25)));

  return {
    renderAgents: zoom >= 0.25,
    renderLabels: !compressed && zoom >= 1.2,
    renderIcons: !compressed && zoom >= 1.0,
    renderHeatmap: !compressed,
    renderParticles: expanded,
    renderPhysicsDebug: Boolean(input.showPhysicsDebug),
    agentRadius: Math.max(2, Math.min(expanded ? 7 : 5, zoom * (expanded ? 4.8 : 4))),
    tileDetail: compressed ? (zoom >= 1.5 ? 1 : 0) : zoom >= 1.5 ? 2 : zoom >= 0.8 ? 1 : 0,
    chunkSize: compressed ? 16 : 8,
    updateStride: compressed ? 4 : expanded ? 1 : 2,
    direction,
    tickType,
    reason,
    R_lod,
    Phi_lod,
  };
}

function classifyTick(tick: number, mu: number): LODStateV2["tickType"] {
  if (mu === 0) return "compressed";
  if (tick > 1 && isPrime(tick)) return "prime";
  if (tick % 8 === 0 || tick % 13 === 0 || tick % 21 === 0) return "event";
  return "normal";
}

function isPrime(n: number): boolean {
  if (n < 2) return false;
  if (n === 2) return true;
  if (n % 2 === 0) return false;
  for (let i = 3; i * i <= n; i += 2) {
    if (n % i === 0) return false;
  }
  return true;
}
