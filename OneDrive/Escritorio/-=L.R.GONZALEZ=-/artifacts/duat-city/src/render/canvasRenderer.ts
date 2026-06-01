import type { CityState, Mode } from "../core/types";
import type { GraphicsBudget, ViewMode } from "../graphics/types";
import type { PhysicsMetrics } from "../physics/types";
import type { SpriteResolver } from "../graphics/spriteResolver";
import { defaultRenderCounters, type PerformanceRenderCounters } from "../performance/performanceTypes";
import { Camera, TILE_SIZE, worldToScreen } from "./camera";
import { LODState } from "./lod-controller";
import { TILE_LABELS } from "./palette";
import { drawAgentSprite } from "../graphics/agentRenderer";
import { drawBuilding } from "../graphics/buildingRenderer";
import { computeLightMap, sampleLight, applyLightOverlay } from "../graphics/lightEngine";
import { fieldSummaryToOverlay } from "../graphics/pixelField";
import { drawIsoTile } from "../graphics/tileRenderer";
import { sortByDepth } from "../graphics/isoMath";
import { qStateColor } from "../quaternary/qstate";
import type { PixelRealismRuntime } from "../pixelRealism/pixelRealismMetrics";
import { beginPixelRealismFrame, finishPixelRealismFrame } from "../pixelRealism/pixelRenderer";
import { capParticles } from "../pixelRealism/renderBudget";
import { drawPlayableSceneOverlay } from "../scene/sceneRender";

import { drawCelestialPass } from "./celestialRenderer";
import type { CelestialState } from "../engine/celestialEngine";

export interface RenderOptions {
  showHeatmap: boolean;
  showFibmob: boolean;
  showAgentLabels: boolean;
  selectedId: string | null;
  mode: Mode;
  graphicsBudget?: GraphicsBudget;
  physicsMetrics?: PhysicsMetrics;
  showPhysicsDebug?: boolean;
  showChunkDebug?: boolean;
  showQuaternaryDebug?: boolean;
  viewMode?: ViewMode;
  spriteResolver?: SpriteResolver;
  pixelRealismRuntime?: PixelRealismRuntime;
  celestialState?: CelestialState;
}

export function renderCity(
  ctx: CanvasRenderingContext2D,
  state: CityState,
  cam: Camera,
  lod: LODState,
  opts: RenderOptions
): PerformanceRenderCounters {
  const { width: W, height: H } = state;
  const ts = TILE_SIZE * cam.zoom;
  const lightMap = computeLightMap(state);
  const viewMode = opts.viewMode ?? "OPERATIONAL";
  const beautiful = viewMode === "BEAUTIFUL";
  const debug = viewMode === "DEBUG";
  const counters = defaultRenderCounters(viewMode, cam.zoom);
  const qDebug = !beautiful && Boolean(opts.showQuaternaryDebug || debug);
  const qMap = qDebug ? new Map(state.quaternary?.recent.map(evaluation => [evaluation.sourceId, evaluation])) : new Map();
  const sparseBaseTiles = viewMode === "OPERATIONAL"
    && !debug
    && !qDebug
    && !opts.showHeatmap
    && !opts.showFibmob
    && !opts.showPhysicsDebug
    && !opts.showChunkDebug;
  counters.dirtyChunks = opts.graphicsBudget?.chunkMode === "FULL" ? 24 : 4;
  const rawParticles = (opts.graphicsBudget?.particlesEnabled ? 12 : 0) + (state.playableScene?.metrics.particles ?? 0);
  counters.particlesRendered = opts.pixelRealismRuntime ? capParticles(rawParticles, opts.pixelRealismRuntime.config) : rawParticles;
  counters.activePixelCells = (state.fieldMetrics?.activeCells ?? 0) + (state.playableScene?.metrics.activeMaterialCells ?? 0);

  if (opts.pixelRealismRuntime) beginPixelRealismFrame(ctx, opts.pixelRealismRuntime);
  ctx.fillStyle = opts.pixelRealismRuntime?.config.timeOfDay === "night"
    ? "#070c17"
    : opts.pixelRealismRuntime?.config.timeOfDay === "interior"
      ? "#17100d"
      : "#111620";
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  if (opts.celestialState && opts.spriteResolver) {
    drawCelestialPass(ctx, opts.celestialState, opts.spriteResolver);
  }

  // Visible tile range
  const startX = Math.max(0, Math.floor(cam.x));
  const startY = Math.max(0, Math.floor(cam.y));
  const endX = Math.min(W, Math.ceil(cam.x + ctx.canvas.width / ts) + 1);
  const endY = Math.min(H, Math.ceil(cam.y + ctx.canvas.height / ts) + 1);

  // Draw tiles
  for (let ty = startY; ty < endY; ty++) {
    for (let tx = startX; tx < endX; tx++) {
      const tile = state.tiles[ty * W + tx];
      if (!tile) continue;
      const qTile = qDebug ? qMap.get(`tile:${tile.id}`) : undefined;
      if (sparseBaseTiles && tile.type === "empty" && !tile.buildingId && !qTile) continue;
      counters.tilesRendered++;

      const { x: sx, y: sy } = worldToScreen(tx, ty, cam);
      drawIsoTile(ctx, tile, {
        x: sx,
        y: sy,
        size: ts,
        showHeatmap: !beautiful && (opts.showHeatmap || debug) && (opts.graphicsBudget?.heatmapEnabled ?? true),
        showFibmob: !beautiful && (opts.showFibmob || debug) && ts > 8,
        light: sampleLight(lightMap, tx / W, ty / H),
      });
      counters.overlaysEnabled = counters.overlaysEnabled || (!beautiful && ((opts.showHeatmap || debug) || (opts.showFibmob || debug)));

      // Tile label
      if (!beautiful && lod.tileDetail >= 1 && ts >= 14 && tile.type !== "empty" && tile.type !== "road") {
        const label = TILE_LABELS[tile.type];
        if (label) {
          ctx.fillStyle = "rgba(255,255,255,0.55)";
          ctx.font = `${Math.max(7, ts * 0.36)}px monospace`;
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(label, sx + ts / 2, sy + ts / 2);
        }
      }

      // Selection highlight
      if (tile.buildingId && tile.buildingId === opts.selectedId) {
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.strokeRect(sx + 1, sy + 1, ts - 2, ts - 2);
      }

      if (qDebug) {
        if (qTile && qTile.state !== "00") {
          ctx.save();
          ctx.strokeStyle = qStateColor(qTile.state);
          ctx.lineWidth = qTile.state === "11" ? 2 : 1;
          ctx.globalAlpha = qTile.state === "10" ? 0.38 : qTile.state === "01" ? 0.72 : 0.86;
          ctx.strokeRect(sx + 2, sy + 2, ts - 4, ts - 4);
          if (qTile.state === "11") {
            ctx.fillStyle = qStateColor(qTile.state);
            ctx.globalAlpha = 0.10 + 0.08 * Math.sin(state.tick * 0.6);
            ctx.fillRect(sx + 3, sy + 3, ts - 6, ts - 6);
          }
          ctx.restore();
          counters.overlaysEnabled = true;
        }
      }
    }
  }

  drawPlayableSceneOverlay(ctx, state, cam, state.playableScene, debug);

  const fieldOverlay = fieldSummaryToOverlay(state.fieldSummary);
  if (!beautiful && fieldOverlay.alpha > 0 && debug) {
    ctx.fillStyle = fieldOverlay.color;
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    counters.overlaysEnabled = true;
  }

  // Draw roads with dashed center line
  if (ts >= 8) {
    ctx.strokeStyle = "#404560";
    ctx.lineWidth = 1;
    for (let ty = startY; ty < endY; ty++) {
      for (let tx = startX; tx < endX; tx++) {
        const tile = state.tiles[ty * W + tx];
        if (!tile || tile.type !== "road") continue;
        const { x: sx, y: sy } = worldToScreen(tx, ty, cam);
        ctx.beginPath();
        ctx.moveTo(sx + ts / 2, sy + 2);
        ctx.lineTo(sx + ts / 2, sy + ts - 2);
        ctx.stroke();
      }
    }
  }

  // Draw buildings as small 2.5D masses above the tiles.
  for (const building of sortByDepth(state.buildings)) {
    if (building.x < startX - 1 || building.y < startY - 1 || building.x > endX + 1 || building.y > endY + 1) continue;
    const { x: sx, y: sy } = worldToScreen(building.x, building.y, cam);
    counters.buildingsRendered++;
    drawBuilding(ctx, building, {
      x: sx,
      y: sy,
      size: ts,
      tick: state.tick,
      selected: building.id === opts.selectedId,
      light: sampleLight(lightMap, building.x / W, building.y / H),
      spriteResolver: opts.spriteResolver,
      viewMode,
    });
  }

  // Draw agents
  if (lod.renderAgents) {
    for (const agent of sortByDepth(state.agents)) {
      if (agent.x < cam.x - 1 || agent.y < cam.y - 1) continue;
      const { x: sx, y: sy } = worldToScreen(agent.x, agent.y, cam);
      if (sx < -20 || sy < -20 || sx > ctx.canvas.width + 20 || sy > ctx.canvas.height + 20) continue;

      const r = lod.agentRadius;
      const isSelected = agent.id === opts.selectedId;
      counters.agentsRendered++;
      drawAgentSprite(ctx, agent, {
        x: sx,
        y: sy,
        size: ts,
        radius: r,
        selected: isSelected,
        showLabel: !beautiful && lod.renderLabels && opts.showAgentLabels,
        spriteResolver: opts.spriteResolver,
        viewMode,
      });
      if (qDebug) {
        const qAgent = qMap.get(`agent:${agent.id}`);
        if (qAgent && qAgent.state !== "00") {
          ctx.save();
          ctx.strokeStyle = qStateColor(qAgent.state);
          ctx.lineWidth = qAgent.state === "11" ? 2 : 1;
          ctx.globalAlpha = qAgent.state === "10" ? 0.55 : 0.90;
          ctx.beginPath();
          ctx.arc(sx + ts / 2, sy + ts / 2, Math.max(4, r + 3), 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
          counters.overlaysEnabled = true;
        }
      }
    }
  }

  if (opts.graphicsBudget?.shadowsEnabled !== false) {
    applyLightOverlay(ctx, lightMap);
  }

  if (opts.pixelRealismRuntime) {
    finishPixelRealismFrame(ctx, state, cam, {
      runtime: opts.pixelRealismRuntime,
      selectedId: opts.selectedId,
      debug,
    });
  }

  if (!beautiful && (opts.showPhysicsDebug || debug)) {
    ctx.strokeStyle = "rgba(123,200,246,0.55)";
    ctx.lineWidth = 1;
    for (const agent of state.agents) {
      const { x: sx, y: sy } = worldToScreen(agent.x, agent.y, cam);
      ctx.beginPath();
      ctx.arc(sx + ts / 2, sy + ts / 2, Math.max(3, ts * 0.22), 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.fillStyle = "rgba(10,14,20,0.82)";
    ctx.fillRect(8, 8, 180, 48);
    ctx.fillStyle = "#c9d1d9";
    ctx.font = "10px monospace";
    ctx.fillText(`pairs ${opts.physicsMetrics?.pairChecks ?? 0}`, 16, 25);
    ctx.fillText(`R_phys ${opts.physicsMetrics?.R_physics.toFixed(3) ?? "n/a"}`, 16, 39);
  }

  if (!beautiful && (opts.showChunkDebug || debug)) {
    ctx.strokeStyle = "rgba(255,255,255,0.16)";
    ctx.lineWidth = 1;
    const chunk = (lod.chunkSize ?? 8) * ts;
    for (let y = 0; y < ctx.canvas.height; y += chunk) {
      for (let x = 0; x < ctx.canvas.width; x += chunk) {
        ctx.strokeRect(x, y, chunk, chunk);
      }
    }
  }

  // Grid origin marker
  if (ts >= 10) {
    const { x: ox, y: oy } = worldToScreen(0, 0, cam);
    ctx.fillStyle = "rgba(255,255,255,0.2)";
    ctx.fillRect(ox, oy, ts, ts);
  }
  return counters;
}
