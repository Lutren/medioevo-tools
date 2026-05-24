import type { Agent, CityState } from "../core/types";
import type { PixelMaterial } from "../physicsField/pixelTypes";
import type { VibeSceneConfig } from "../vibecoding/vibeTypes";
import { getVibePreset } from "../vibecoding/vibePresets";
import type {
  PlacedLightSource,
  PlacedMaterialCell,
  PlayableLightKind,
  PlayableMaterial,
  PlayableSceneMetrics,
  PlayableSceneSave,
  PlayableSceneState,
} from "./sceneTypes";

const MATERIAL_TO_PIXEL: Record<PlayableMaterial, PixelMaterial> = {
  water: "water",
  fire: "fire",
  smoke: "smoke",
  stone: "stone",
  wood: "wood",
  neon: "neon",
};

const LIGHT_COLORS: Record<PlayableLightKind, string> = {
  torch: "#ffb45c",
  window: "#ffd79a",
  neon: "#22e8ff",
  fire: "#ff7a2f",
  magic: "#72ffd8",
  signal: "#5ce0be",
  ruin_anomaly: "#a457ff",
};

const MATERIAL_LIGHT: Record<PlayableMaterial, number> = {
  water: 0,
  fire: 1,
  smoke: 0.08,
  stone: 0,
  wood: 0,
  neon: 1,
};

export function createDefaultPlayableSceneState(): PlayableSceneState {
  const scene: PlayableSceneState = {
    schema: "duat/playable-scene/v1.1",
    version: "1.1",
    tick: 0,
    paused: false,
    timeOfDay: "day",
    weather: "clear",
    materials: [],
    lights: [],
    metrics: emptySceneMetrics(),
  };
  return { ...scene, metrics: computeSceneMetrics(scene) };
}

export function setSceneTime(scene: PlayableSceneState, timeOfDay: PlayableSceneState["timeOfDay"]): PlayableSceneState {
  return withMetrics({ ...scene, timeOfDay });
}

export function setSceneWeather(scene: PlayableSceneState, weather: PlayableSceneState["weather"]): PlayableSceneState {
  const materials = weather === "rain"
    ? scene.materials.map(cell => ({ ...cell, wetness: Math.max(cell.wetness, 0.62), active: true }))
    : scene.materials;
  return withMetrics({ ...scene, weather, materials });
}

export function placeSceneMaterial(scene: PlayableSceneState, x: number, y: number, material: PlayableMaterial): PlayableSceneState {
  const clean = scene.materials.filter(cell => cell.x !== x || cell.y !== y);
  const light = MATERIAL_LIGHT[material];
  const cell: PlacedMaterialCell = {
    id: `mat-${x}-${y}-${material}`,
    x,
    y,
    material,
    wetness: material === "water" ? 1 : scene.weather === "rain" ? 0.55 : 0,
    temperature: material === "fire" ? 1 : material === "smoke" ? 0.45 : 0.2,
    light,
    active: ["water", "fire", "smoke", "neon"].includes(material),
    qState: material === "fire" || material === "neon" ? "11" : material === "water" ? "10" : "00",
    tickPlaced: scene.tick,
  };
  const selected = { kind: "material" as const, id: cell.id, x, y };
  return withMetrics({ ...scene, materials: [...clean, cell], selected });
}

export function placeSceneLight(scene: PlayableSceneState, x: number, y: number, kind: PlayableLightKind): PlayableSceneState {
  const clean = scene.lights.filter(light => light.x !== x || light.y !== y);
  const light: PlacedLightSource = {
    id: `light-${x}-${y}-${kind}`,
    x,
    y,
    kind,
    color: LIGHT_COLORS[kind],
    intensity: kind === "window" ? 0.7 : kind === "torch" ? 0.82 : 1,
    radius: kind === "ruin_anomaly" ? 8 : kind === "signal" || kind === "magic" ? 7 : 5,
    active: true,
    tickPlaced: scene.tick,
  };
  const selected = { kind: "light" as const, id: light.id, x, y };
  return withMetrics({ ...scene, lights: [...clean, light], selected });
}

export function eraseSceneAt(scene: PlayableSceneState, x: number, y: number): PlayableSceneState {
  return withMetrics({
    ...scene,
    materials: scene.materials.filter(cell => cell.x !== x || cell.y !== y),
    lights: scene.lights.filter(light => light.x !== x || light.y !== y),
    selected: undefined,
  });
}

export function selectSceneAt(scene: PlayableSceneState, x: number, y: number): PlayableSceneState {
  const material = scene.materials.find(cell => cell.x === x && cell.y === y);
  if (material) return { ...scene, selected: { kind: "material", id: material.id, x, y } };
  const light = scene.lights.find(source => source.x === x && source.y === y);
  if (light) return { ...scene, selected: { kind: "light", id: light.id, x, y } };
  return { ...scene, selected: undefined };
}

export function stepPlayableScene(scene: PlayableSceneState, width: number, height: number): PlayableSceneState {
  const occupied = new Map<string, PlacedMaterialCell>();
  const nextMaterials: PlacedMaterialCell[] = [];
  const ordered = scene.materials.map(cell => updateMaterialCell(cell, scene));

  for (const cell of ordered) {
    let moved = cell;
    if (cell.material === "water") moved = moveWater(cell, occupied, width, height, scene.tick);
    if (cell.material === "smoke") moved = moveSmoke(cell, occupied);
    const key = coordKey(moved.x, moved.y);
    if (!occupied.has(key)) {
      occupied.set(key, moved);
      nextMaterials.push(moved);
    }
  }

  for (const cell of ordered) {
    if (cell.material !== "fire") continue;
    const smokeY = Math.max(0, cell.y - 1);
    const key = coordKey(cell.x, smokeY);
    if (!occupied.has(key)) {
      const smoke = makeMaterialAt(scene.tick, cell.x, smokeY, "smoke", scene.weather === "rain" ? 0.25 : 0);
      occupied.set(key, smoke);
      nextMaterials.push(smoke);
    }
  }

  return withMetrics({
    ...scene,
    tick: scene.tick + 1,
    materials: nextMaterials.slice(-400),
    lights: scene.lights.map(light => ({
      ...light,
      intensity: light.kind === "neon" || light.kind === "ruin_anomaly"
        ? Math.max(0.55, Math.min(1, light.intensity + Math.sin(scene.tick * 0.6 + light.x) * 0.03))
        : light.intensity,
    })),
  });
}

export function applyVibeSceneToPlayableScene(scene: PlayableSceneState, vibe: VibeSceneConfig, width: number, height: number): PlayableSceneState {
  let next: PlayableSceneState = {
    ...scene,
    timeOfDay: vibe.timeOfDay,
    weather: vibe.weather,
    activeVibe: vibe,
    lastIntent: vibe.visualTags,
  };
  const seeds = seedMaterialsForVibe(vibe, width, height);
  for (const seed of seeds) next = placeSceneMaterial(next, seed.x, seed.y, seed.material);
  const lights = seedLightsForVibe(vibe, width, height);
  for (const light of lights) next = placeSceneLight(next, light.x, light.y, light.kind);
  return withMetrics(next);
}

export function makeAgentLoadState(state: CityState, count: number): CityState {
  if (count <= state.agents.length) return { ...state, agents: state.agents.slice(0, count) };
  const agents: Agent[] = [];
  for (let i = 0; i < count; i++) {
    const base = state.agents[i % Math.max(1, state.agents.length)];
    const x = 4 + (i % Math.max(1, state.width - 8));
    const y = 5 + (Math.floor(i / 8) % Math.max(1, state.height - 10));
    agents.push({
      ...base,
      id: `agent-load-${i + 1}`,
      name: `${base.name} ${i + 1}`,
      x,
      y,
      R: Math.min(1, base.R + (i % 11) * 0.003),
      Phi_eff: Math.max(0, base.Phi_eff - (i % 7) * 0.002),
      memory: base.memory.slice(-3),
      relationships: {},
    });
  }
  return { ...state, agents };
}

export function serializePlayableScene(scene: PlayableSceneState): string {
  const save: PlayableSceneSave = {
    schema: "duat/playable-scene-save/v1.1",
    exportedAt: new Date().toISOString(),
    scene: withMetrics(scene),
  };
  return JSON.stringify(save, null, 2);
}

export function deserializePlayableScene(json: string): PlayableSceneState | undefined {
  try {
    const parsed = JSON.parse(json) as Partial<PlayableSceneSave> & Partial<PlayableSceneState> & { scene?: Partial<PlayableSceneState> };
    const scene: Partial<PlayableSceneState> | undefined = parsed.schema === "duat/playable-scene-save/v1.1" ? parsed.scene : parsed;
    if (!scene || !Array.isArray(scene.materials) || !Array.isArray(scene.lights)) return undefined;
    return withMetrics({
      schema: "duat/playable-scene/v1.1",
      version: "1.1",
      tick: Number(scene.tick ?? 0),
      paused: Boolean(scene.paused),
      timeOfDay: scene.timeOfDay ?? "day",
      weather: scene.weather ?? "clear",
      activeVibe: scene.activeVibe,
      materials: scene.materials.filter(isPlacedMaterialCell),
      lights: scene.lights.filter(isPlacedLightSource),
      selected: scene.selected,
      lastIntent: Array.isArray(scene.lastIntent) ? scene.lastIntent : undefined,
      metrics: emptySceneMetrics(),
    });
  } catch {
    return undefined;
  }
}

export function playableSceneRpgProfile(scene: PlayableSceneState): object {
  return {
    schema: "duat/playable-rpg-scene/v1.1",
    timeOfDay: scene.timeOfDay,
    weather: scene.weather,
    vibe: scene.activeVibe?.id,
    placed_materials: scene.materials.map(cell => ({
      id: cell.id,
      x: cell.x,
      y: cell.y,
      material: cell.material,
      wetness: round(cell.wetness),
      light: round(cell.light),
      qState: cell.qState,
    })),
    placed_lights: scene.lights.map(light => ({
      id: light.id,
      x: light.x,
      y: light.y,
      kind: light.kind,
      color: light.color,
      intensity: round(light.intensity),
      radius: light.radius,
    })),
    hazards: scene.materials
      .filter(cell => cell.material === "fire" || cell.material === "smoke" || cell.material === "neon")
      .map(cell => `${cell.material}:${cell.x},${cell.y}`),
    quest_hooks: [
      ...scene.lights.filter(light => light.kind === "ruin_anomaly").map(light => `investigate anomaly light:${light.x},${light.y}`),
      ...scene.materials.filter(cell => cell.material === "water").map(cell => `drain flooded passage:${cell.x},${cell.y}`).slice(0, 3),
      ...scene.materials.filter(cell => cell.material === "fire").map(cell => `contain fire and smoke:${cell.x},${cell.y}`).slice(0, 3),
      ...scene.materials.filter(cell => cell.material === "neon").map(cell => `repair neon market:${cell.x},${cell.y}`).slice(0, 3),
    ],
  };
}

export function playableMaterialToPixelMaterial(material: PlayableMaterial): PixelMaterial {
  return MATERIAL_TO_PIXEL[material];
}

export function computeSceneMetrics(scene: Pick<PlayableSceneState, "materials" | "lights" | "weather">): PlayableSceneMetrics {
  const qStateCounts = emptySceneMetrics().qStateCounts;
  let reflectiveCells = 0;
  let blockedCells = 0;
  let emissiveCells = 0;
  let wetCells = 0;
  for (const cell of scene.materials) {
    qStateCounts[cell.qState]++;
    if (cell.material === "water" || cell.wetness > 0.35 || cell.material === "neon") reflectiveCells++;
    if (cell.material === "stone" || cell.material === "wood") blockedCells++;
    if (cell.material === "fire" || cell.material === "neon") emissiveCells++;
    if (cell.wetness > 0.2) wetCells++;
  }
  const weatherParticles = scene.weather === "rain" || scene.weather === "snow" || scene.weather === "fog" ? 24 : 0;
  const particles = weatherParticles + scene.materials.filter(cell => cell.material === "smoke" || cell.material === "fire").length * 3;
  return {
    activeMaterialCells: scene.materials.filter(cell => cell.active || (cell.material !== "stone" && cell.material !== "wood")).length,
    activeLightSources: scene.lights.filter(light => light.active).length,
    particles,
    reflectiveCells,
    blockedCells,
    emissiveCells,
    wetCells,
    qStateCounts,
  };
}

function withMetrics(scene: PlayableSceneState): PlayableSceneState {
  return { ...scene, metrics: computeSceneMetrics(scene) };
}

function emptySceneMetrics(): PlayableSceneMetrics {
  return {
    activeMaterialCells: 0,
    activeLightSources: 0,
    particles: 0,
    reflectiveCells: 0,
    blockedCells: 0,
    emissiveCells: 0,
    wetCells: 0,
    qStateCounts: { "00": 0, "01": 0, "10": 0, "11": 0 },
  };
}

function updateMaterialCell(cell: PlacedMaterialCell, scene: PlayableSceneState): PlacedMaterialCell {
  const rainWetness = scene.weather === "rain" ? 0.08 : 0;
  if (cell.material === "fire") {
    const rainPenalty = scene.weather === "rain" ? 0.18 : 0;
    return {
      ...cell,
      temperature: Math.max(0.2, cell.temperature - rainPenalty + 0.03),
      light: Math.max(0.55, 1 - rainPenalty),
      wetness: Math.max(0, cell.wetness - 0.12 + rainWetness * 0.25),
      active: true,
      qState: scene.tick % 2 === 0 ? "11" : "01",
    };
  }
  if (cell.material === "neon") {
    return { ...cell, light: 0.85 + Math.sin(scene.tick * 0.5 + cell.x) * 0.12, active: true, qState: "11" };
  }
  if (cell.material === "water") {
    return { ...cell, wetness: 1, light: Math.max(0, cell.light * 0.96), active: true, qState: "10" };
  }
  if (cell.material === "smoke") {
    return { ...cell, temperature: Math.max(0.1, cell.temperature - 0.02), light: Math.max(0, cell.light * 0.94), active: true, qState: "11" };
  }
  const wetness = Math.max(0, Math.min(1, cell.wetness + rainWetness - 0.01));
  return { ...cell, wetness, active: wetness > 0.35, qState: wetness > 0.35 ? "10" : "00" };
}

function moveWater(cell: PlacedMaterialCell, occupied: Map<string, PlacedMaterialCell>, width: number, height: number, tick: number): PlacedMaterialCell {
  const candidates = [
    { x: cell.x, y: Math.min(height - 1, cell.y + 1) },
    { x: Math.max(0, Math.min(width - 1, cell.x + (tick % 2 === 0 ? -1 : 1))), y: cell.y },
  ];
  for (const next of candidates) {
    if (next.x === cell.x && next.y === cell.y) continue;
    if (!occupied.has(coordKey(next.x, next.y))) return { ...cell, ...next, qState: "11" };
  }
  return { ...cell, qState: "10" };
}

function moveSmoke(cell: PlacedMaterialCell, occupied: Map<string, PlacedMaterialCell>): PlacedMaterialCell {
  const y = Math.max(0, cell.y - 1);
  if (y !== cell.y && !occupied.has(coordKey(cell.x, y))) return { ...cell, y, qState: "11" };
  return { ...cell, qState: "10" };
}

function makeMaterialAt(tick: number, x: number, y: number, material: PlayableMaterial, wetness: number): PlacedMaterialCell {
  return {
    id: `mat-${x}-${y}-${material}`,
    x,
    y,
    material,
    wetness,
    temperature: material === "fire" ? 1 : material === "smoke" ? 0.45 : 0.2,
    light: MATERIAL_LIGHT[material],
    active: true,
    qState: material === "fire" || material === "neon" || material === "smoke" ? "11" : "10",
    tickPlaced: tick,
  };
}

function seedMaterialsForVibe(vibe: VibeSceneConfig, width: number, height: number): Array<{ x: number; y: number; material: PlayableMaterial }> {
  const cx = Math.floor(width / 2);
  const cy = Math.floor(height / 2);
  const seeds: Array<{ x: number; y: number; material: PlayableMaterial }> = [];
  if (vibe.materials.includes("water")) seeds.push({ x: cx - 3, y: cy + 3, material: "water" }, { x: cx - 2, y: cy + 3, material: "water" });
  if (vibe.materials.includes("fire")) seeds.push({ x: cx, y: cy - 2, material: "fire" });
  if (vibe.materials.includes("smoke")) seeds.push({ x: cx, y: cy - 3, material: "smoke" });
  if (vibe.materials.includes("neon")) seeds.push({ x: cx + 3, y: cy - 1, material: "neon" });
  if (vibe.materials.includes("ruinMatter")) seeds.push({ x: cx + 5, y: cy + 1, material: "stone" });
  if (vibe.id === getVibePreset("desert_skyline").id) seeds.push({ x: cx - 4, y: cy, material: "stone" });
  return seeds;
}

function seedLightsForVibe(vibe: VibeSceneConfig, width: number, height: number): Array<{ x: number; y: number; kind: PlayableLightKind }> {
  const cx = Math.floor(width / 2);
  const cy = Math.floor(height / 2);
  if (vibe.lightProfile.includes("neon")) return [{ x: cx + 3, y: cy - 1, kind: "neon" }];
  if (vibe.lightProfile.includes("torch") || vibe.lightProfile.includes("window")) return [{ x: cx, y: cy - 2, kind: "torch" }, { x: cx + 2, y: cy - 2, kind: "window" }];
  if (vibe.lightProfile.includes("ruin") || vibe.lightProfile.includes("anomaly")) return [{ x: cx + 5, y: cy + 1, kind: "ruin_anomaly" }];
  if (vibe.lightProfile.includes("signal")) return [{ x: cx, y: cy, kind: "signal" }];
  return [];
}

function isPlacedMaterialCell(value: unknown): value is PlacedMaterialCell {
  const cell = value as PlacedMaterialCell;
  return Boolean(cell && typeof cell.id === "string" && Number.isFinite(cell.x) && Number.isFinite(cell.y) && isPlayableMaterial(cell.material));
}

function isPlacedLightSource(value: unknown): value is PlacedLightSource {
  const light = value as PlacedLightSource;
  return Boolean(light && typeof light.id === "string" && Number.isFinite(light.x) && Number.isFinite(light.y) && isPlayableLightKind(light.kind));
}

function isPlayableMaterial(material: unknown): material is PlayableMaterial {
  return material === "water" || material === "fire" || material === "smoke" || material === "stone" || material === "wood" || material === "neon";
}

function isPlayableLightKind(kind: unknown): kind is PlayableLightKind {
  return kind === "torch" || kind === "window" || kind === "neon" || kind === "fire" || kind === "magic" || kind === "signal" || kind === "ruin_anomaly";
}

function coordKey(x: number, y: number): string {
  return `${x},${y}`;
}

function round(value: number): number {
  return Number(value.toFixed(3));
}
