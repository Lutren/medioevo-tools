/**
 * DUAT Brain OS v1.4.0 — Tipos Unificados del Sistema Nervioso
 * Fingerprint: DUAT-v1.4.0-BRAIN-OS-TYPES
 */

export type QState = '00' | '01' | '10' | '11';
export type Gate = 'APPROVE' | 'REVIEW' | 'BLOCK';
export type Regime = 'OPTIMO' | 'SATURADO' | 'JAMMED' | 'CRITICO';

export interface OSITState {
  state: QState;
  memory: Float32Array;
  calibration: number;
  noise: number;
  goal: string;
  gate: Gate;
  lastUpdate: number;
}

export interface SystemMetrics {
  R: number;
  Phi_eff: number;
  J_c: number;
  regime: Regime;
}

export interface Vec2 { x: number; y: number; }

export interface RGB { r: number; g: number; b: number; }

export interface WorldCell {
  x: number; y: number; z?: number;
  material: string;
  osit: OSITState;
  physics: any;
  light: any;
  audio?: any;
}

export interface EngineConfig {
  gridSize: number;
  gridWidth: number;
  gridHeight: number;
  maxSubsteps: number;
  emlThreshold: number;
  jammingThreshold: number;
  enableAudioBridge: boolean;
  enableLightBridge: boolean;
}

// Brain-specific types
export interface HandoffManifest {
  fingerprint: string;
  timestamp: number;
  residueVector: Float32Array;
  predictedState: any;
  observerSnapshot: OSITState;
  nextAction: string;
  evidence: string[];
}

export interface ActionDecision {
  action: string;
  target: string;
  priority: number;
  resourceBudget: ResourceBudget;
  gate: Gate;
  rationale: string;
}

export interface ResourceBudget {
  cpuPercent: number;
  memoryMB: number;
  timeMs: number;
}

export interface AttentionFilter {
  channel: string;
  signalThreshold: number;
  noiseMax: number;
  R_max: number;
  pattern: string;
}

export interface TimingTick {
  tau: number;
  phase: number;
  beat: number;
  globalFrame: number;
}

export interface TestClaim {
  id: string;
  claim: string;
  test: () => boolean;
  falsifier: () => boolean;
  status: 'PASS' | 'FAIL' | 'PENDING';
  lastRun: number;
}

export interface ResourceState {
  cpuUsed: number;
  memoryUsed: number;
  batteryLevel?: number;
  temperature: number;
  fps: number;
}

export interface CrossModalEvent {
  source: string;
  target: string;
  delta: any;
  timestamp: number;
  confidence: number;
}

export interface BodySchema {
  observerPosition: Vec2;
  attentionFocus: Vec2;
  sensorRange: number;
  availableModalities: string[];
  currentModality: string;
}
