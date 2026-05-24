import type { SpriteRef } from "./atlas";

const cache = new Map<string, HTMLImageElement | "failed">();

export function loadSprite(sprite: SpriteRef): HTMLImageElement | undefined {
  if (!sprite.src || typeof Image === "undefined") return undefined;
  const cached = cache.get(sprite.id);
  if (cached === "failed") return undefined;
  if (cached instanceof HTMLImageElement) return cached.complete ? cached : undefined;
  const img = new Image();
  img.onload = () => cache.set(sprite.id, img);
  img.onerror = () => cache.set(sprite.id, "failed");
  img.src = sprite.src;
  cache.set(sprite.id, img);
  return undefined;
}

export function clearSpriteCache(): void {
  cache.clear();
}
