import type { Agent, Building, CityState, Mode } from "../core/types";
import type { ViewMode } from "../graphics/types";
import { TILE_SIZE, type Camera } from "./camera";

export interface ViewportSize {
  width: number;
  height: number;
}

export interface CameraPresetResult {
  camera: Camera;
  showHeatmap: boolean;
  showFibmob: boolean;
  showPhysicsDebug: boolean;
  showChunkDebug: boolean;
  showAgentLabels: boolean;
}

interface Bounds {
  minX: number;
  minY: number;
  maxX: number;
  maxY: number;
}

export function fitCityToViewport(city: CityState, width: number, height: number, padding = 80): Camera {
  return fitBoundsToViewport(fullCityBounds(city), width, height, padding, 1.25);
}

export function centerOnCity(city: CityState, width = 960, height = 720, zoom = 1): Camera {
  return centerBounds(fullCityBounds(city), width, height, clampZoom(zoom));
}

export function centerOnActiveDistrict(city: CityState, width = 960, height = 720, zoom = 1.35): Camera {
  const bounds = activeBounds(city);
  return centerBounds(bounds, width, height, clampZoom(zoom));
}

export function centerOnSelectedAgent(agent: Agent, width = 960, height = 720, zoom = 2.1): Camera {
  return centerBounds({ minX: agent.x - 2, minY: agent.y - 2, maxX: agent.x + 2, maxY: agent.y + 2 }, width, height, clampZoom(zoom));
}

export function centerOnSelectedBuilding(building: Building, width = 960, height = 720, zoom = 1.9): Camera {
  return centerBounds({ minX: building.x - 2, minY: building.y - 2, maxX: building.x + 2, maxY: building.y + 2 }, width, height, clampZoom(zoom));
}

export function applyCameraPreset(
  mode: Mode,
  viewMode: ViewMode,
  city: CityState,
  viewport: ViewportSize,
  selectedId?: string | null,
): CameraPresetResult {
  const width = Math.max(320, viewport.width || 960);
  const height = Math.max(240, viewport.height || 720);
  const selectedAgent = selectedId ? city.agents.find(agent => agent.id === selectedId) : undefined;
  const selectedBuilding = selectedId ? city.buildings.find(building => building.id === selectedId) : undefined;

  if (viewMode === "DEBUG") {
    return {
      camera: fitBoundsToViewport(activeBounds(city), width, height, 40, 1.15),
      showHeatmap: true,
      showFibmob: true,
      showPhysicsDebug: true,
      showChunkDebug: true,
      showAgentLabels: true,
    };
  }

  if (viewMode === "BEAUTIFUL") {
    return {
      camera: fitBoundsToViewport(activeBounds(city), width, height, 42, 2.45),
      showHeatmap: false,
      showFibmob: false,
      showPhysicsDebug: false,
      showChunkDebug: false,
      showAgentLabels: false,
    };
  }

  if (selectedAgent && mode === "AGENT") {
    return {
      camera: centerOnSelectedAgent(selectedAgent, width, height, 2.1),
      showHeatmap: false,
      showFibmob: false,
      showPhysicsDebug: false,
      showChunkDebug: false,
      showAgentLabels: true,
    };
  }

  if (selectedBuilding && mode === "CITY") {
    return {
      camera: centerOnSelectedBuilding(selectedBuilding, width, height, 1.7),
      showHeatmap: false,
      showFibmob: false,
      showPhysicsDebug: false,
      showChunkDebug: false,
      showAgentLabels: true,
    };
  }

  if (mode === "AGENT") {
    const critical = mostCriticalAgent(city);
    return {
      camera: critical ? centerOnSelectedAgent(critical, width, height, 1.9) : centerOnActiveDistrict(city, width, height, 1.45),
      showHeatmap: false,
      showFibmob: false,
      showPhysicsDebug: false,
      showChunkDebug: false,
      showAgentLabels: true,
    };
  }

  if (mode === "RPG") {
    return {
      camera: fitBoundsToViewport(landmarkBounds(city), width, height, 80, 1.25),
      showHeatmap: false,
      showFibmob: false,
      showPhysicsDebug: false,
      showChunkDebug: false,
      showAgentLabels: false,
    };
  }

  if (mode === "OSIT") {
    return {
      camera: fitBoundsToViewport(activeBounds(city), width, height, 54, 1.35),
      showHeatmap: true,
      showFibmob: false,
      showPhysicsDebug: false,
      showChunkDebug: false,
      showAgentLabels: true,
    };
  }

  return {
    camera: fitBoundsToViewport(activeBounds(city), width, height, 64, 1.55),
    showHeatmap: false,
    showFibmob: false,
    showPhysicsDebug: false,
    showChunkDebug: false,
    showAgentLabels: true,
  };
}

export function mostCriticalAgent(city: CityState): Agent | undefined {
  return city.agents
    .slice()
    .sort((a, b) => criticalScore(b) - criticalScore(a))[0];
}

export function isFiniteCamera(camera: Camera): boolean {
  return Number.isFinite(camera.x) && Number.isFinite(camera.y) && Number.isFinite(camera.zoom) && camera.zoom > 0;
}

function fullCityBounds(city: CityState): Bounds {
  return { minX: 0, minY: 0, maxX: Math.max(1, city.width - 1), maxY: Math.max(1, city.height - 1) };
}

function activeBounds(city: CityState): Bounds {
  const points = [
    ...city.tiles.filter(tile => tile.type !== "empty").map(tile => ({ x: tile.x, y: tile.y })),
    ...city.buildings.map(building => ({ x: building.x, y: building.y })),
    ...city.agents.map(agent => ({ x: agent.x, y: agent.y })),
  ];
  return boundsFromPoints(points, fullCityBounds(city), 3);
}

function landmarkBounds(city: CityState): Bounds {
  const landmarkTypes = new Set(["observatory", "archive", "temple", "ruin", "gatehouse", "market"]);
  const points = city.buildings.filter(building => landmarkTypes.has(building.type)).map(building => ({ x: building.x, y: building.y }));
  return boundsFromPoints(points.length > 0 ? points : city.buildings, activeBounds(city), 4);
}

function boundsFromPoints(points: Array<{ x: number; y: number }>, fallback: Bounds, pad = 2): Bounds {
  if (points.length === 0) return fallback;
  const xs = points.map(point => point.x).filter(Number.isFinite);
  const ys = points.map(point => point.y).filter(Number.isFinite);
  if (xs.length === 0 || ys.length === 0) return fallback;
  return {
    minX: Math.min(...xs) - pad,
    minY: Math.min(...ys) - pad,
    maxX: Math.max(...xs) + pad,
    maxY: Math.max(...ys) + pad,
  };
}

function fitBoundsToViewport(bounds: Bounds, width: number, height: number, padding: number, maxZoom: number): Camera {
  const worldWidth = Math.max(4, bounds.maxX - bounds.minX + 1);
  const worldHeight = Math.max(4, bounds.maxY - bounds.minY + 1);
  const usableWidth = Math.max(160, width - padding * 2);
  const usableHeight = Math.max(140, height - padding * 2);
  const zoom = clampZoom(Math.min(maxZoom, usableWidth / (worldWidth * TILE_SIZE), usableHeight / (worldHeight * TILE_SIZE)));
  return centerBounds(bounds, width, height, zoom);
}

function centerBounds(bounds: Bounds, width: number, height: number, zoom: number): Camera {
  const safeZoom = clampZoom(zoom);
  const centerX = (bounds.minX + bounds.maxX + 1) / 2;
  const centerY = (bounds.minY + bounds.maxY + 1) / 2;
  return sanitizeCamera({
    x: centerX - width / (2 * TILE_SIZE * safeZoom),
    y: centerY - height / (2 * TILE_SIZE * safeZoom),
    zoom: safeZoom,
  });
}

function clampZoom(zoom: number): number {
  if (!Number.isFinite(zoom)) return 1;
  return Math.max(0.45, Math.min(3.25, zoom));
}

function sanitizeCamera(camera: Camera): Camera {
  return {
    x: Number.isFinite(camera.x) ? camera.x : 0,
    y: Number.isFinite(camera.y) ? camera.y : 0,
    zoom: clampZoom(camera.zoom),
  };
}

function criticalScore(agent: Agent): number {
  const lowestNeed = Math.min(...Object.values(agent.needs));
  return agent.R + (1 - lowestNeed) * 0.5 + (agent.gate === "BLOCK" ? 1 : agent.gate === "REVIEW" ? 0.5 : 0);
}
