import type { Agent, CityState, Gate } from "../core/types";
import type { PlacedLightSource, PlacedMaterialCell } from "../scene/sceneTypes";
import type { AudioCue, AudioCueKind, AudioGameFeelMetrics } from "./audioTypes";
import { DEFAULT_AUDIO_GAMEFEEL_CONFIG } from "./audioTypes";

const MATERIAL_FREQ: Record<string, number> = {
  water: 174,
  fire: 92,
  smoke: 61,
  stone: 110,
  wood: 146,
  neon: 523,
};

const LIGHT_FREQ: Record<string, number> = {
  torch: 196,
  window: 262,
  neon: 740,
  fire: 130,
  magic: 660,
  signal: 392,
  ruin_anomaly: 55,
};

export interface AudioMappingOptions {
  maxCues?: number;
  seed?: number;
  includeAgentCues?: boolean;
}

export function mapWorldToAudioCues(state: CityState, options: AudioMappingOptions = {}): AudioCue[] {
  const maxCues = options.maxCues ?? DEFAULT_AUDIO_GAMEFEEL_CONFIG.maxCues;
  const seed = options.seed ?? DEFAULT_AUDIO_GAMEFEEL_CONFIG.seed;
  const scene = state.playableScene;
  const cues: AudioCue[] = [];

  for (const cell of scene?.materials ?? []) {
    cues.push(materialCue(cell, state.width, seed));
  }
  for (const light of scene?.lights ?? []) {
    cues.push(lightCue(light, state.width, seed));
  }
  for (const cue of cosmologyFireCues(scene?.materials ?? [], state.width, seed)) {
    cues.push(cue);
  }
  if (options.includeAgentCues !== false) {
    for (const agent of state.agents.slice(0, 24)) {
      const cue = agentCue(agent, state.width, seed);
      if (cue) cues.push(cue);
    }
  }
  cues.push(gateCue(state.gate, seed));

  return dedupeCues(cues)
    .sort((a, b) => b.priority - a.priority || a.id.localeCompare(b.id))
    .slice(0, maxCues)
    .map(normalizeCue);
}

export function computeAudioMetrics(cues: AudioCue[]): AudioGameFeelMetrics {
  const safe = cues.map(normalizeCue);
  const cueCount = safe.length;
  const gainSum = safe.reduce((sum, cue) => sum + cue.gain, 0);
  const peakGain = safe.reduce((max, cue) => Math.max(max, cue.gain), 0);
  const materialCues = safe.filter(cue => cue.source === "material").length;
  const lightCues = safe.filter(cue => cue.source === "light").length;
  const agentCues = safe.filter(cue => cue.source === "agent").length;
  const highPriorityCues = safe.filter(cue => cue.priority >= 0.72).length;
  const R_audio = round3(clamp01(cueCount / 48 + highPriorityCues * 0.018 + peakGain * 0.08));
  const Phi_audio = round3(clamp01(1 - R_audio * 0.55 + (cueCount > 0 ? 0.05 : 0)));
  return {
    R_audio,
    Phi_audio,
    cueCount,
    highPriorityCues,
    materialCues,
    lightCues,
    agentCues,
    averageGain: round3(cueCount > 0 ? gainSum / cueCount : 0),
    peakGain: round3(peakGain),
    deterministicHash: cueHash(safe),
    finite: safe.every(cue => [cue.frequencyHz, cue.durationMs, cue.gain, cue.pan, cue.priority].every(Number.isFinite)),
    proceduralOnly: true,
  };
}

export function mapEpistemicClassificationToAudioCue(classification: string, seed = DEFAULT_AUDIO_GAMEFEEL_CONFIG.seed): AudioCue {
  const normalized = classification.toUpperCase();
  const kind: AudioCueKind = normalized.includes("CERTEZA")
    ? "language_certeza"
    : normalized.includes("INFERENCIA")
      ? "language_inferencia"
      : normalized.includes("BLOQUEO")
        ? "language_bloqueo"
        : "language_incognita";
  const frequencyHz = kind === "language_certeza" ? 330 : kind === "language_inferencia" ? 294 : kind === "language_bloqueo" ? 82 : 220;
  return normalizeCue({
    id: `language-${kind}-${seed}`,
    kind,
    source: "language",
    label: `Language ${classification}`,
    frequencyHz,
    durationMs: kind === "language_bloqueo" ? 220 : 120,
    gain: kind === "language_bloqueo" ? 0.18 : 0.08,
    pan: 0,
    priority: kind === "language_bloqueo" ? 0.82 : 0.48,
    tags: ["language-cortex", "classified-output"],
  });
}

function materialCue(cell: PlacedMaterialCell, width: number, seed: number): AudioCue {
  const base = MATERIAL_FREQ[cell.material] ?? 180;
  const kind = `material_${cell.material}` as AudioCueKind;
  const hot = cell.material === "fire" || cell.material === "neon";
  return {
    id: `material-${cell.id}`,
    kind,
    source: "material",
    label: `${cell.material} cell ${cell.x},${cell.y}`,
    frequencyHz: base + deterministicOffset(cell.id, seed, 17),
    durationMs: cell.material === "smoke" ? 280 : hot ? 180 : 140,
    gain: clamp01((hot ? 0.16 : 0.08) + cell.wetness * 0.06 + cell.light * 0.08),
    pan: panForX(cell.x, width),
    priority: clamp01((cell.active ? 0.36 : 0.16) + cell.light * 0.36 + (cell.material === "fire" ? 0.24 : 0)),
    qState: cell.qState,
    tags: ["pixel-cell", cell.material, cell.active ? "active" : "stable"],
  };
}

function lightCue(light: PlacedLightSource, width: number, seed: number): AudioCue {
  const base = LIGHT_FREQ[light.kind] ?? 260;
  return {
    id: `light-${light.id}`,
    kind: `light_${light.kind}` as AudioCueKind,
    source: "light",
    label: `${light.kind} light ${light.x},${light.y}`,
    frequencyHz: base + deterministicOffset(light.id, seed, 23),
    durationMs: light.kind === "ruin_anomaly" ? 420 : light.kind === "neon" ? 240 : 160,
    gain: clamp01(0.06 + light.intensity * 0.18),
    pan: panForX(light.x, width),
    priority: clamp01(0.32 + light.intensity * 0.42 + (light.kind === "ruin_anomaly" ? 0.2 : 0)),
    tags: ["light-grid", light.kind, light.active ? "active" : "inactive"],
  };
}

function cosmologyFireCues(cells: PlacedMaterialCell[], width: number, seed: number): AudioCue[] {
  return cells
    .filter(cell => cell.material === "fire")
    .slice(0, 4)
    .map(cell => normalizeCue({
      id: `cosmology-fire-${cell.id}`,
      kind: "cosmology_fire_event",
      source: "cosmology",
      label: `in-world fire event ${cell.x},${cell.y}`,
      frequencyHz: 73 + deterministicOffset(cell.id, seed, 11),
      durationMs: 360,
      gain: 0.14,
      pan: panForX(cell.x, width),
      priority: 0.78,
      qState: cell.qState,
      tags: ["IN_WORLD_COSMOLOGY", "fire_event", "fictional-boundary"],
    }));
}

function agentCue(agent: Agent, width: number, seed: number): AudioCue | undefined {
  const weakestNeed = Math.min(...Object.values(agent.needs));
  const needsCue = weakestNeed < 0.32;
  const riskCue = agent.R > 0.34 || agent.gate !== "APPROVE";
  if (!needsCue && !riskCue && !agent.currentTaskId) return undefined;
  return normalizeCue({
    id: `agent-${agent.id}-${agent.currentTaskId ?? "life"}`,
    kind: needsCue ? "agent_need" : "agent_task",
    source: "agent",
    label: `${agent.name} ${needsCue ? "need" : "task"}`,
    frequencyHz: (needsCue ? 208 : 247) + deterministicOffset(agent.id, seed, 19),
    durationMs: needsCue ? 180 : 120,
    gain: clamp01(0.06 + agent.R * 0.16 + (1 - weakestNeed) * 0.08),
    pan: panForX(agent.x, width),
    priority: clamp01(0.28 + agent.R * 0.5 + (needsCue ? 0.18 : 0)),
    gate: agent.gate,
    tags: ["agent-life", agent.role, agent.currentTaskId ? "task" : "needs"],
  });
}

function gateCue(gate: Gate, seed: number): AudioCue {
  const kind: AudioCueKind = gate === "BLOCK" ? "gate_block" : gate === "REVIEW" ? "gate_review" : "gate_approve";
  return normalizeCue({
    id: `gate-${gate}-${seed}`,
    kind,
    source: "system",
    label: `ActionGate ${gate}`,
    frequencyHz: gate === "BLOCK" ? 70 : gate === "REVIEW" ? 165 : 330,
    durationMs: gate === "BLOCK" ? 260 : 110,
    gain: gate === "APPROVE" ? 0.035 : 0.11,
    pan: 0,
    priority: gate === "APPROVE" ? 0.12 : gate === "REVIEW" ? 0.62 : 0.88,
    gate,
    tags: ["ActionGate", gate],
  });
}

function dedupeCues(cues: AudioCue[]): AudioCue[] {
  const byId = new Map<string, AudioCue>();
  for (const cue of cues) byId.set(cue.id, cue);
  return Array.from(byId.values());
}

export function normalizeCue(cue: AudioCue): AudioCue {
  return {
    ...cue,
    frequencyHz: round3(Math.max(20, Math.min(16000, finite(cue.frequencyHz)))),
    durationMs: round3(Math.max(20, Math.min(2000, finite(cue.durationMs)))),
    gain: round3(clamp01(cue.gain)),
    pan: round3(Math.max(-1, Math.min(1, finite(cue.pan)))),
    priority: round3(clamp01(cue.priority)),
    tags: cue.tags.filter(Boolean).slice(0, 12),
  };
}

function panForX(x: number, width: number): number {
  if (width <= 1) return 0;
  return Math.max(-1, Math.min(1, (x / (width - 1)) * 2 - 1));
}

function deterministicOffset(id: string, seed: number, span: number): number {
  return ((hashString(`${id}:${seed}`) % (span * 2 + 1)) - span) * 0.5;
}

function cueHash(cues: AudioCue[]): number {
  return hashString(cues.map(cue => `${cue.id}:${cue.kind}:${cue.frequencyHz}:${cue.gain}`).join("|"));
}

function hashString(input: string): number {
  let hash = 2166136261;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return Math.abs(hash >>> 0);
}

function finite(value: number): number {
  return Number.isFinite(value) ? value : 0;
}

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, finite(value)));
}

function round3(value: number): number {
  return Number(Number.isFinite(value) ? value.toFixed(3) : "0");
}
