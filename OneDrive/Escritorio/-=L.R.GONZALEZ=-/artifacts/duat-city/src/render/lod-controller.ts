import type { Camera } from "./camera";
import { computeLODV2 } from "./lod-controller-v2";
import type { PhysicsMetrics } from "../physics/types";

export interface LODState {
  renderAgents: boolean;
  renderLabels: boolean;
  renderIcons: boolean;
  renderHeatmap: boolean;
  renderParticles?: boolean;
  renderPhysicsDebug?: boolean;
  agentRadius: number;
  tileDetail: number;
  chunkSize?: number;
  updateStride?: number;
  direction?: "EXPAND" | "HOLD" | "COMPRESS";
  tickType?: "compressed" | "normal" | "prime" | "event";
  reason?: string;
  R_lod?: number;
  Phi_lod?: number;
}

export function computeLOD(
  camera: Camera,
  R: number,
  Phi_eff = 1 - R,
  tick = 1,
  physicsMetrics?: PhysicsMetrics,
  showPhysicsDebug = false,
): LODState {
  return computeLODV2({ camera, R, Phi_eff, tick, physicsMetrics, showPhysicsDebug });
}
