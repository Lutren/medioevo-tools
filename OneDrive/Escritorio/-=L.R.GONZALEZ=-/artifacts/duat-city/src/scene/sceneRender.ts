import type { CityState } from "../core/types";
import { TILE_SIZE, worldToScreen, type Camera } from "../render/camera";
import type { PlayableSceneState } from "./sceneTypes";

export function drawPlayableSceneOverlay(
  ctx: CanvasRenderingContext2D,
  state: CityState,
  cam: Camera,
  scene: PlayableSceneState | undefined,
  debug = false,
): void {
  if (!scene || (scene.materials.length === 0 && scene.lights.length === 0)) return;
  const size = TILE_SIZE * cam.zoom;
  ctx.save();
  for (const light of scene.lights) {
    if (!light.active) continue;
    const { x, y } = worldToScreen(light.x, light.y, cam);
    drawLightGlow(ctx, x + size / 2, y + size / 2, size * light.radius * 0.42, light.color, light.intensity);
  }
  for (const cell of scene.materials) {
    if (cell.x < cam.x - 2 || cell.y < cam.y - 2 || cell.x > cam.x + state.width + 2 || cell.y > cam.y + state.height + 2) continue;
    const { x, y } = worldToScreen(cell.x, cell.y, cam);
    drawMaterialCell(ctx, x, y, size, cell.material, cell.wetness, cell.light, state.tick);
    if (debug) {
      ctx.strokeStyle = qColor(cell.qState);
      ctx.lineWidth = cell.qState === "11" ? 2 : 1;
      ctx.strokeRect(x + 2, y + 2, size - 4, size - 4);
    }
  }
  if (debug) drawSceneDebugHud(ctx, scene);
  ctx.restore();
}

function drawMaterialCell(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  size: number,
  material: PlayableSceneState["materials"][number]["material"],
  wetness: number,
  light: number,
  tick: number,
): void {
  ctx.save();
  const inset = Math.max(1, size * 0.1);
  if (material === "water") {
    ctx.fillStyle = `rgba(54, 120, 168, ${0.52 + wetness * 0.22})`;
    ctx.fillRect(x + inset, y + size * 0.52, size - inset * 2, size * 0.34);
    ctx.strokeStyle = "rgba(150,220,255,0.62)";
    ctx.beginPath();
    ctx.moveTo(x + inset, y + size * 0.58 + Math.sin(tick * 0.3) * 1.5);
    ctx.lineTo(x + size - inset, y + size * 0.57 + Math.cos(tick * 0.2) * 1.5);
    ctx.stroke();
  } else if (material === "fire") {
    const flicker = 0.8 + Math.sin(tick * 0.8) * 0.18;
    ctx.fillStyle = `rgba(255, 122, 47, ${0.58 * flicker})`;
    ctx.fillRect(x + size * 0.34, y + size * 0.26, size * 0.32, size * 0.42);
    ctx.fillStyle = "rgba(255, 220, 112, 0.8)";
    ctx.fillRect(x + size * 0.43, y + size * 0.36, size * 0.14, size * 0.22);
    drawLightGlow(ctx, x + size / 2, y + size * 0.44, size * 2.1, "#ff7a2f", Math.max(0.4, light));
  } else if (material === "smoke") {
    ctx.fillStyle = "rgba(120, 128, 138, 0.35)";
    ctx.beginPath();
    ctx.arc(x + size * 0.5, y + size * 0.36, Math.max(3, size * 0.28), 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "rgba(180, 190, 205, 0.18)";
    ctx.fillRect(x + size * 0.32, y + size * 0.22, size * 0.36, size * 0.18);
  } else if (material === "stone") {
    ctx.fillStyle = wetness > 0.3 ? "#6f7376" : "#5f5b56";
    ctx.fillRect(x + inset, y + size * 0.34, size - inset * 2, size * 0.42);
    if (wetness > 0.3) {
      ctx.fillStyle = "rgba(150, 220, 255, 0.18)";
      ctx.fillRect(x + inset, y + size * 0.34, size - inset * 2, size * 0.12);
    }
  } else if (material === "wood") {
    ctx.fillStyle = wetness > 0.3 ? "#6d5846" : "#72523a";
    ctx.fillRect(x + inset, y + size * 0.38, size - inset * 2, size * 0.32);
    ctx.strokeStyle = "rgba(20, 12, 8, 0.32)";
    ctx.beginPath();
    ctx.moveTo(x + size * 0.25, y + size * 0.45);
    ctx.lineTo(x + size * 0.75, y + size * 0.45);
    ctx.stroke();
  } else if (material === "neon") {
    ctx.fillStyle = "rgba(34, 232, 255, 0.82)";
    ctx.fillRect(x + size * 0.25, y + size * 0.42, size * 0.5, Math.max(2, size * 0.12));
    drawLightGlow(ctx, x + size / 2, y + size * 0.48, size * 2.4, "#22e8ff", 0.95);
  }
  ctx.restore();
}

function drawLightGlow(ctx: CanvasRenderingContext2D, x: number, y: number, radius: number, color: string, intensity: number): void {
  const gradient = ctx.createRadialGradient(x, y, 0, x, y, Math.max(4, radius));
  gradient.addColorStop(0, colorToRgba(color, 0.26 * intensity));
  gradient.addColorStop(0.42, colorToRgba(color, 0.11 * intensity));
  gradient.addColorStop(1, colorToRgba(color, 0));
  ctx.fillStyle = gradient;
  ctx.fillRect(x - radius, y - radius, radius * 2, radius * 2);
}

function drawSceneDebugHud(ctx: CanvasRenderingContext2D, scene: PlayableSceneState): void {
  ctx.fillStyle = "rgba(5,10,18,0.82)";
  ctx.fillRect(10, 142, 226, 74);
  ctx.fillStyle = "#c9f4ff";
  ctx.font = "10px monospace";
  ctx.fillText(`Scene materials ${scene.metrics.activeMaterialCells}`, 18, 160);
  ctx.fillText(`Scene lights ${scene.metrics.activeLightSources}`, 18, 176);
  ctx.fillText(`Particles ${scene.metrics.particles}`, 18, 192);
  ctx.fillText(`Q ${JSON.stringify(scene.metrics.qStateCounts)}`, 18, 208);
}

function colorToRgba(hex: string, alpha: number): string {
  const clean = hex.replace("#", "");
  if (!/^[0-9a-f]{6}$/i.test(clean)) return `rgba(255,255,255,${Math.max(0, alpha)})`;
  const r = parseInt(clean.slice(0, 2), 16);
  const g = parseInt(clean.slice(2, 4), 16);
  const b = parseInt(clean.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${Math.max(0, Math.min(1, alpha))})`;
}

function qColor(qState: "00" | "01" | "10" | "11"): string {
  if (qState === "01") return "#ff4d6d";
  if (qState === "10") return "#7bd88f";
  if (qState === "11") return "#ffd166";
  return "#6e7681";
}
