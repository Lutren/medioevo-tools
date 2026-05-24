import type { PhysicsBody } from "./types";

export interface SpatialHash {
  cellSize: number;
  buckets: Map<string, PhysicsBody[]>;
}

export function makeSpatialHash(cellSize = 1.5): SpatialHash {
  return { cellSize, buckets: new Map() };
}

export function cellKey(x: number, y: number, cellSize: number): string {
  const cx = Math.floor(x / cellSize);
  const cy = Math.floor(y / cellSize);
  return `${cx}:${cy}`;
}

export function insertBody(hash: SpatialHash, body: PhysicsBody): void {
  const key = cellKey(body.x, body.y, hash.cellSize);
  const bucket = hash.buckets.get(key);
  if (bucket) bucket.push(body);
  else hash.buckets.set(key, [body]);
}

export function buildSpatialHash(bodies: PhysicsBody[], cellSize = 1.5): SpatialHash {
  const hash = makeSpatialHash(cellSize);
  for (const body of bodies) insertBody(hash, body);
  return hash;
}

export function queryNearby(hash: SpatialHash, body: PhysicsBody): PhysicsBody[] {
  const cx = Math.floor(body.x / hash.cellSize);
  const cy = Math.floor(body.y / hash.cellSize);
  const out: PhysicsBody[] = [];
  for (let y = cy - 1; y <= cy + 1; y++) {
    for (let x = cx - 1; x <= cx + 1; x++) {
      const bucket = hash.buckets.get(`${x}:${y}`);
      if (!bucket) continue;
      out.push(...bucket);
    }
  }
  return out;
}

export function estimatePairChecks(hash: SpatialHash): number {
  let checks = 0;
  for (const bucket of hash.buckets.values()) {
    checks += Math.max(0, (bucket.length * (bucket.length - 1)) / 2);
  }
  return checks;
}
