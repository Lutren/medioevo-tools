import type { CityState } from "../core/types";
import type { FieldMetrics } from "../physicsField/pixelTypes";
import { createCity } from "../sim/city";
import { AGENT_ROLES, createAgent } from "../sim/agents";
import { tickEngine } from "../sim/engine";
import { computeGraphicsBudget, estimateGraphicsMetrics } from "../graphics/graphicsMetrics";

export interface VisualBenchmarkScenario {
  id: string;
  agents: number;
  lights: boolean;
  particles: boolean;
  pixelField: boolean;
  overlays: boolean;
}

export interface VisualBenchmarkResult extends VisualBenchmarkScenario {
  frames: number;
  avg_fps: number;
  min_fps: number;
  max_fps: number;
  frame_time_avg_ms: number;
  frame_time_p95_ms: number;
  agents_count: number;
  buildings_count: number;
  active_pixel_field_cells: number;
  particles_count: number;
  dirty_chunks_count: number;
  R_graphics: number;
  Phi_graphics: number;
  R_physics: number;
  Phi_physics: number;
}

export interface VisualBenchmarkOutput {
  schema: "duat.visual-benchmark.v0.7";
  generated_at: string;
  mode: "node-simulation-estimate";
  frames_per_scenario: number;
  scenarios: VisualBenchmarkResult[];
}

export const VISUAL_BENCHMARK_SCENARIOS: VisualBenchmarkScenario[] = [
  { id: "baseline-12-agents", agents: 12, lights: true, particles: true, pixelField: true, overlays: false },
  { id: "50-agents", agents: 50, lights: true, particles: true, pixelField: true, overlays: false },
  { id: "100-agents", agents: 100, lights: true, particles: true, pixelField: true, overlays: false },
  { id: "lights-off", agents: 50, lights: false, particles: true, pixelField: true, overlays: false },
  { id: "particles-off", agents: 50, lights: true, particles: false, pixelField: true, overlays: false },
  { id: "pixel-field-off", agents: 50, lights: true, particles: true, pixelField: false, overlays: false },
  { id: "overlays-on", agents: 50, lights: true, particles: true, pixelField: true, overlays: true },
];

export function runVisualBenchmark(framesPerScenario = 260): VisualBenchmarkOutput {
  return {
    schema: "duat.visual-benchmark.v0.7",
    generated_at: new Date().toISOString(),
    mode: "node-simulation-estimate",
    frames_per_scenario: framesPerScenario,
    scenarios: VISUAL_BENCHMARK_SCENARIOS.map(scenario => runScenario(scenario, framesPerScenario)),
  };
}

function runScenario(scenario: VisualBenchmarkScenario, frames: number): VisualBenchmarkResult {
  let state = withAgentCount(createCity(), scenario.agents);
  const frameTimes: number[] = [];
  let particlesCount = scenario.particles ? 24 : 0;
  for (let frame = 0; frame < frames; frame++) {
    const start = performance.now();
    state = tickEngine(state, {
      enableAgentPhysics: true,
      enablePhysicsCollisions: true,
      enablePixelField: scenario.pixelField,
      physicsDt: 0.05,
    });
    const budget = computeGraphicsBudget(
      state.R,
      state.Phi_eff,
      1,
      state.physicsMetrics?.R_physics ?? 0,
      state.tick,
    );
    const graphics = estimateGraphicsMetrics(
      budget,
      scenario.overlays ? 36 : 12,
      scenario.overlays ? 12 : 4,
      particlesCount,
    );
    state = { ...state, graphicsMetrics: graphics };
    const syntheticRenderCost = estimateRenderCostMs(state, scenario, state.fieldMetrics);
    const elapsed = Math.max(0.01, performance.now() - start + syntheticRenderCost);
    frameTimes.push(elapsed);
    particlesCount = scenario.particles ? Math.max(0, Math.min(300, particlesCount + (frame % 15 === 0 ? 2 : -1))) : 0;
  }
  const sorted = frameTimes.slice().sort((a, b) => a - b);
  const avg = frameTimes.reduce((sum, value) => sum + value, 0) / Math.max(1, frameTimes.length);
  const min = sorted[0] ?? avg;
  const max = sorted[sorted.length - 1] ?? avg;
  const p95 = sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95))] ?? avg;
  const graphics = state.graphicsMetrics!;
  return {
    ...scenario,
    frames,
    avg_fps: round(1000 / avg),
    min_fps: round(1000 / max),
    max_fps: round(1000 / min),
    frame_time_avg_ms: round(avg),
    frame_time_p95_ms: round(p95),
    agents_count: state.agents.length,
    buildings_count: state.buildings.length,
    active_pixel_field_cells: state.fieldMetrics?.activeCells ?? 0,
    particles_count: particlesCount,
    dirty_chunks_count: graphics.dirtyChunks,
    R_graphics: graphics.R_graphics,
    Phi_graphics: graphics.Phi_graphics,
    R_physics: state.physicsMetrics?.R_physics ?? 0,
    Phi_physics: state.physicsMetrics?.Phi_physics ?? 1,
  };
}

function withAgentCount(state: CityState, count: number): CityState {
  if (count <= state.agents.length) return { ...state, agents: state.agents.slice(0, count) };
  const agents = [...state.agents];
  for (let i = agents.length; i < count; i++) {
    agents.push(createAgent(AGENT_ROLES[i % AGENT_ROLES.length], 24 + (i % 8) * 0.12, 16 + (i % 9) * 0.12));
  }
  return { ...state, agents };
}

function estimateRenderCostMs(state: CityState, scenario: VisualBenchmarkScenario, field?: FieldMetrics): number {
  const lightCost = scenario.lights ? state.buildings.length * 0.012 : 0;
  const overlayCost = scenario.overlays ? state.tiles.length * 0.0008 : 0;
  const particleCost = scenario.particles ? 0.18 : 0;
  const fieldCost = scenario.pixelField ? (field?.activeCells ?? 0) * 0.002 : 0;
  const agentCost = state.agents.length * 0.015;
  return lightCost + overlayCost + particleCost + fieldCost + agentCost;
}

function round(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.round(value * 100) / 100;
}
