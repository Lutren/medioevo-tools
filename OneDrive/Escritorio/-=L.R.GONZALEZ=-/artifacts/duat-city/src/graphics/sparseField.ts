import type { CityState } from "../core/types";
import type { DirtyChunk } from "./types";

export function chunkKey(x: number, y: number, chunkSize = 8): string {
  return `${Math.floor(x / chunkSize)}:${Math.floor(y / chunkSize)}`;
}

export function computeDirtyChunks(prev: CityState | null, next: CityState, chunkSize = 8): DirtyChunk[] {
  if (!prev || prev.tick === next.tick) return allChunks(next, chunkSize);
  const keys = new Set<string>();

  for (let i = 0; i < next.tiles.length; i++) {
    const a = prev.tiles[i];
    const b = next.tiles[i];
    if (!a || !b) continue;
    if (a.type !== b.type || a.buildingId !== b.buildingId || Math.abs(a.R - b.R) > 0.04 || Math.abs(a.Phi_eff - b.Phi_eff) > 0.04) {
      keys.add(chunkKey(b.x, b.y, chunkSize));
    }
  }

  for (const agent of next.agents) {
    const old = prev.agents.find(a => a.id === agent.id);
    if (!old || chunkKey(old.x, old.y, chunkSize) !== chunkKey(agent.x, agent.y, chunkSize)) {
      keys.add(chunkKey(agent.x, agent.y, chunkSize));
    }
  }

  return [...keys].map(key => {
    const [x, y] = key.split(":").map(Number);
    return { x, y, key };
  });
}

export function allChunks(state: CityState, chunkSize = 8): DirtyChunk[] {
  const chunks: DirtyChunk[] = [];
  for (let y = 0; y < Math.ceil(state.height / chunkSize); y++) {
    for (let x = 0; x < Math.ceil(state.width / chunkSize); x++) {
      chunks.push({ x, y, key: `${x}:${y}` });
    }
  }
  return chunks;
}
