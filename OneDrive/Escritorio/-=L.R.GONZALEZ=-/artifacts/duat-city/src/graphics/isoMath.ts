export interface IsoConfig {
  tileWidth: number;
  tileHeight: number;
  originX: number;
  originY: number;
}

export interface DrawableDepth {
  x: number;
  y: number;
  z?: number;
  id?: string;
}

export function gridToScreen(x: number, y: number, z = 0, cfg: IsoConfig = defaultIsoConfig()): { x: number; y: number } {
  return {
    x: cfg.originX + (x - y) * (cfg.tileWidth / 2),
    y: cfg.originY + (x + y) * (cfg.tileHeight / 2) - z,
  };
}

export function screenToGrid(px: number, py: number, z = 0, cfg: IsoConfig = defaultIsoConfig()): { x: number; y: number } {
  const sx = (px - cfg.originX) / (cfg.tileWidth / 2);
  const sy = (py - cfg.originY + z) / (cfg.tileHeight / 2);
  return {
    x: (sy + sx) / 2,
    y: (sy - sx) / 2,
  };
}

export function sortByDepth<T extends DrawableDepth>(drawables: T[]): T[] {
  return drawables
    .slice()
    .sort((a, b) => {
      const da = a.x + a.y + (a.z ?? 0) * 0.1;
      const db = b.x + b.y + (b.z ?? 0) * 0.1;
      if (da !== db) return da - db;
      return String(a.id ?? "").localeCompare(String(b.id ?? ""));
    });
}

export function defaultIsoConfig(): IsoConfig {
  return { tileWidth: 32, tileHeight: 16, originX: 0, originY: 0 };
}
