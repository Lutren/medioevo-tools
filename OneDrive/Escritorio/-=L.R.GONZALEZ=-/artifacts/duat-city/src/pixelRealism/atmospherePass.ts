import type { CityState } from "../core/types";
import type { PixelRealismConfig } from "./renderPasses";

export function drawAtmospherePass(ctx: CanvasRenderingContext2D, state: CityState, config: PixelRealismConfig): void {
  ctx.save();
  const night = config.timeOfDay === "night";
  const interior = config.timeOfDay === "interior";
  const grd = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
  if (night) {
    grd.addColorStop(0, "rgba(3, 9, 23, 0.26)");
    grd.addColorStop(1, "rgba(6, 13, 20, 0.42)");
  } else if (interior) {
    grd.addColorStop(0, "rgba(70, 36, 18, 0.18)");
    grd.addColorStop(1, "rgba(22, 13, 11, 0.34)");
  } else {
    grd.addColorStop(0, "rgba(66, 94, 109, 0.08)");
    grd.addColorStop(1, "rgba(18, 22, 18, 0.22)");
  }
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  if (config.weather === "rain") drawRain(ctx, state.tick);
  if (config.weather === "snow") drawSnow(ctx, state.tick);
  if (config.weather === "fog" || config.weather === "jungle_mist" || config.weather === "desert_haze") {
    ctx.fillStyle = config.weather === "desert_haze" ? "rgba(220, 170, 100, 0.08)" : "rgba(165, 190, 190, 0.10)";
    for (let y = 0; y < ctx.canvas.height; y += 24) {
      ctx.fillRect((Math.sin(state.tick * 0.05 + y) * 20) - 10, y, ctx.canvas.width + 20, 8);
    }
  }
  ctx.restore();
}

function drawRain(ctx: CanvasRenderingContext2D, tick: number): void {
  ctx.strokeStyle = "rgba(118, 202, 255, 0.28)";
  ctx.lineWidth = 1;
  for (let i = 0; i < 90; i++) {
    const x = (i * 47 + tick * 3) % ctx.canvas.width;
    const y = (i * 29 + tick * 7) % ctx.canvas.height;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x - 5, y + 13);
    ctx.stroke();
  }
}

function drawSnow(ctx: CanvasRenderingContext2D, tick: number): void {
  ctx.fillStyle = "rgba(234, 246, 255, 0.34)";
  for (let i = 0; i < 70; i++) {
    const x = (i * 43 + Math.sin(tick * 0.08 + i) * 12) % ctx.canvas.width;
    const y = (i * 31 + tick * 1.5) % ctx.canvas.height;
    ctx.fillRect(x, y, 2, 2);
  }
}
