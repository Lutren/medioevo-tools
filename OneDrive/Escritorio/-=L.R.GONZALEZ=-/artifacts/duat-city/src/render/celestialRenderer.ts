import type { CelestialState } from "../engine/celestialEngine";
import type { SpriteResolver } from "../graphics/spriteResolver";

export function drawCelestialPass(
  ctx: CanvasRenderingContext2D,
  state: CelestialState,
  spriteResolver: SpriteResolver
): void {
  ctx.save();
  
  // Logic: Select asset based on phase/cycle (Example: Using sun_wukong for daytime)
  const sunAsset = "duat_010_sun_wukong"; 
  const sunX = state.sunPosition.x + ctx.canvas.width / 2;
  const sunY = state.sunPosition.y + ctx.canvas.height / 2;

  // Use spriteResolver to fetch and draw the actual asset
  const sprite = spriteResolver.resolve(sunAsset);
  if (sprite) {
    ctx.drawImage(sprite, sunX - 32, sunY - 32, 64, 64);
  } else {
    // Fallback drawing if asset not found
    ctx.fillStyle = "#FFD700";
    ctx.beginPath();
    ctx.arc(sunX, sunY, 30, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();
}
