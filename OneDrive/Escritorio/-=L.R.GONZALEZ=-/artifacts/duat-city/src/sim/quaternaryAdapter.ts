import type { CityState, ResourceKey } from "../core/types";
import type { QEvaluation, QInput, QuaternaryStateSummary } from "../quaternary/types";
import { QuaternarySensorBank } from "../quaternary/quaternarySensor";
import { computeQuaternarySystemMetrics } from "../quaternary/quaternaryMetrics";
import { toQuaternaryHandoff } from "../quaternary/quaternaryHandoff";

const clamp01 = (n: number) => Math.max(0, Math.min(1, Number.isFinite(n) ? n : 0));
const round = (n: number) => Math.round(n * 1000) / 1000;

const sensorBank = new QuaternarySensorBank({
  windowSize: 64,
  minDwellTicks: 2,
  useFibMob: true,
});

export interface CityQuaternaryEvaluation {
  evaluations: QEvaluation[];
  summary: QuaternaryStateSummary;
  R_delta: number;
  Phi_delta: number;
}

export function resetCityQuaternarySensorBank(): void {
  sensorBank.reset();
}

export function evaluateCityQuaternary(state: CityState, previousState: CityState, tick = state.tick): CityQuaternaryEvaluation {
  if (previousState.tick === 0 && tick <= 1) resetCityQuaternarySensorBank();

  const inputs = buildCityInputs(state, previousState, tick);
  const evaluations = inputs.map(input => sensorBank.evaluate(input));
  const metrics = computeQuaternarySystemMetrics(evaluations);
  const handoff = toQuaternaryHandoff(metrics, evaluations);
  const R_delta = clamp01Delta(evaluations.reduce((sum, evaluation) => sum + evaluation.R_delta, 0) / Math.max(1, evaluations.length));
  const Phi_delta = clamp01Delta(evaluations.reduce((sum, evaluation) => sum + evaluation.Phi_delta, 0) / Math.max(1, evaluations.length));
  const secondaryR = state.physicsMetrics?.R_physics ?? state.fieldMetrics?.R_field;
  const secondaryPhi = state.physicsMetrics?.Phi_physics ?? state.fieldMetrics?.Phi_field;
  const combinedR = secondaryR == null
    ? clamp01(0.82 * state.R + 0.18 * metrics.R_quaternary)
    : clamp01(0.70 * state.R + 0.15 * metrics.R_quaternary + 0.15 * secondaryR);
  const combinedPhi = secondaryPhi == null
    ? clamp01(0.82 * state.Phi_eff + 0.18 * metrics.Phi_quaternary)
    : clamp01(0.70 * state.Phi_eff + 0.15 * metrics.Phi_quaternary + 0.15 * secondaryPhi);

  const summary: QuaternaryStateSummary = {
    R: metrics.R_quaternary,
    Phi_eff: metrics.Phi_quaternary,
    gate: metrics.recommendedGate,
    counts: metrics.counts,
    avgFrequency: metrics.avgFrequency,
    avgPermanence: metrics.avgPermanence,
    avgStability: metrics.avgStability,
    anomalyRate: metrics.anomalyRate,
    eventRate: metrics.eventRate,
    R_delta: round(R_delta),
    Phi_delta: round(Phi_delta),
    combinedR: round(combinedR),
    combinedPhi: round(combinedPhi),
    topAnomalies: handoff.top_anomalies,
    topUnstable: handoff.top_unstable,
    recent: evaluations.slice(-64),
    next_action: handoff.next_action,
  };

  return {
    evaluations,
    summary,
    R_delta: summary.R_delta,
    Phi_delta: summary.Phi_delta,
  };
}

function buildCityInputs(state: CityState, previousState: CityState, tick: number): QInput[] {
  const inputs: QInput[] = [];
  const resourceKeys = Object.keys(state.resources) as ResourceKey[];
  for (const key of resourceKeys) {
    const current = state.resources[key] ?? 0;
    const previous = previousState.resources[key] ?? 0;
    const threshold = key === "signal" ? 5 : 1;
    inputs.push({
      sourceId: `resource:${key}`,
      sourceKind: "resource",
      tick,
      presence: current > threshold,
      expected: previous > threshold || key === "signal",
      difference: Math.abs(current - previous) > Math.max(0.75, threshold * 0.10),
      rawValue: current,
      previousValue: previous,
      threshold,
    });
  }

  const previousAgents = new Map(previousState.agents.map(agent => [agent.id, agent]));
  for (const agent of state.agents) {
    const previous = previousAgents.get(agent.id);
    const moved = previous ? Math.abs(agent.x - previous.x) + Math.abs(agent.y - previous.y) > 0.15 : true;
    const taskChanged = previous ? agent.currentTaskId !== previous.currentTaskId : true;
    const metricChanged = previous ? Math.abs(agent.R - previous.R) > 0.025 || Math.abs(agent.Phi_eff - previous.Phi_eff) > 0.025 : true;
    inputs.push({
      sourceId: `agent:${agent.id}`,
      sourceKind: "agent",
      tick,
      presence: true,
      expected: true,
      difference: moved || taskChanged || metricChanged,
      rawValue: agent.R,
      previousValue: previous?.R,
    });
  }

  const previousBuildings = new Map(previousState.buildings.map(building => [building.id, building]));
  for (const building of state.buildings) {
    const previous = previousBuildings.get(building.id);
    const currentStorage = sumStorage(building.storage);
    const previousStorage = previous ? sumStorage(previous.storage) : 0;
    inputs.push({
      sourceId: `building:${building.id}`,
      sourceKind: "building",
      tick,
      presence: true,
      expected: true,
      difference: !previous || building.gate !== previous.gate || building.level !== previous.level || Math.abs(currentStorage - previousStorage) > 1,
      rawValue: currentStorage,
      previousValue: previousStorage,
    });
  }

  const previousTasks = new Map(previousState.tasks.map(task => [task.id, task]));
  for (const task of state.tasks.slice(0, 48)) {
    const previous = previousTasks.get(task.id);
    inputs.push({
      sourceId: `task:${task.id}`,
      sourceKind: "task",
      tick,
      presence: task.status === "active" || task.status === "pending",
      expected: previous ? previous.status === "active" || previous.status === "pending" : task.status !== "done",
      difference: !previous || task.status !== previous.status || Math.abs(task.progress - previous.progress) > 0.01,
      rawValue: task.progress,
      previousValue: previous?.progress,
    });
  }

  const previousTiles = new Map(previousState.tiles.map(tile => [tile.id, tile]));
  for (const tile of state.tiles.filter(tile => tile.type !== "empty").slice(0, 96)) {
    const previous = previousTiles.get(tile.id);
    inputs.push({
      sourceId: `tile:${tile.id}`,
      sourceKind: "tile",
      tick,
      presence: tile.type !== "empty",
      expected: previous ? previous.type !== "empty" : false,
      difference: !previous || tile.type !== previous.type || tile.buildingId !== previous.buildingId || Math.abs(tile.R - previous.R) > 0.025,
      rawValue: tile.R,
      previousValue: previous?.R,
    });
  }

  const activeCells = state.fieldMetrics?.activeCells ?? 0;
  const previousActiveCells = previousState.fieldMetrics?.activeCells ?? 0;
  inputs.push({
    sourceId: "pixel_field:active_cells",
    sourceKind: "pixel_cell",
    tick,
    presence: activeCells > 0,
    expected: previousActiveCells > 0,
    difference: Math.abs(activeCells - previousActiveCells) > 0,
    rawValue: activeCells,
    previousValue: previousActiveCells,
  });

  const bodyCount = state.physicsMetrics?.bodyCount ?? 0;
  const previousBodyCount = previousState.physicsMetrics?.bodyCount ?? 0;
  inputs.push({
    sourceId: "physics:body_count",
    sourceKind: "physics_body",
    tick,
    presence: bodyCount > 0,
    expected: previousBodyCount > 0,
    difference: Math.abs(bodyCount - previousBodyCount) > 0 || (state.physicsMetrics?.unresolvedCollisions ?? 0) > 0,
    rawValue: bodyCount,
    previousValue: previousBodyCount,
  });

  const chunks = state.graphicsMetrics?.chunksRendered ?? 0;
  const previousChunks = previousState.graphicsMetrics?.chunksRendered ?? 0;
  inputs.push({
    sourceId: "render:chunks",
    sourceKind: "render_chunk",
    tick,
    presence: chunks > 0,
    expected: previousChunks > 0,
    difference: Math.abs(chunks - previousChunks) > 0 || (state.graphicsMetrics?.R_graphics ?? 0) > 0.45,
    rawValue: chunks,
    previousValue: previousChunks,
  });

  return inputs;
}

function sumStorage(storage: Partial<Record<ResourceKey, number>>): number {
  return Object.values(storage).reduce((sum, value) => sum + (value ?? 0), 0);
}

function clamp01Delta(n: number): number {
  if (!Number.isFinite(n)) return 0;
  return Math.max(-1, Math.min(1, n));
}

