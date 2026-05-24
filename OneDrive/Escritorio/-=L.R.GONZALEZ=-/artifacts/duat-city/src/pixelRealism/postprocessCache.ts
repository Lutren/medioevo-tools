import { computeLayerDirtyKey, createOffscreenLayerCache, getOrCreateLayer, invalidateLayer, type OffscreenLayerCache } from "./offscreenLayerCache";

export type PostprocessLayer = "bloom" | "dither" | "reflection" | "atmosphere";

export interface PostprocessCache<T = unknown> {
  cache: OffscreenLayerCache<T>;
}

export function createPostprocessCache<T = unknown>(): PostprocessCache<T> {
  return { cache: createOffscreenLayerCache<T>() };
}

export function getCachedPostprocess<T>(cache: PostprocessCache<T>, layer: PostprocessLayer, dirtyParts: Record<string, unknown>, factory: () => T): T {
  return getOrCreateLayer(cache.cache, `${layer}|${computeLayerDirtyKey(dirtyParts)}`, factory);
}

export function invalidatePostprocess(cache: PostprocessCache, layer: PostprocessLayer): void {
  invalidateLayer(cache.cache, `${layer}|`);
}
