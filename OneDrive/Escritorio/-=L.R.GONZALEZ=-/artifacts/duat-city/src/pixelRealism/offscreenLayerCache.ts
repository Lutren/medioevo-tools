export interface LayerCacheEntry<T> {
  key: string;
  value: T;
  dirty: boolean;
  used: number;
}

export interface OffscreenLayerCache<T = unknown> {
  entries: Map<string, LayerCacheEntry<T>>;
  hits: number;
  misses: number;
}

export function createOffscreenLayerCache<T = unknown>(): OffscreenLayerCache<T> {
  return { entries: new Map(), hits: 0, misses: 0 };
}

export function getOrCreateLayer<T>(cache: OffscreenLayerCache<T>, key: string, factory: () => T): T {
  const existing = cache.entries.get(key);
  if (existing && !existing.dirty) {
    cache.hits++;
    existing.used++;
    return existing.value;
  }
  const value = factory();
  cache.entries.set(key, { key, value, dirty: false, used: 1 });
  cache.misses++;
  return value;
}

export function invalidateLayer(cache: OffscreenLayerCache, keyPrefix: string): void {
  for (const [key, entry] of cache.entries) {
    if (key.startsWith(keyPrefix)) cache.entries.set(key, { ...entry, dirty: true });
  }
}

export function computeLayerDirtyKey(parts: Record<string, unknown>): string {
  return Object.keys(parts).sort().map(key => `${key}:${String(parts[key])}`).join("|");
}
