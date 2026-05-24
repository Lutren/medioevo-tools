export interface SpriteFrame {
  x: number;
  y: number;
  w: number;
  h: number;
  key: string;
}

export function buildSpriteSheetFrames(keys: string[], frameW: number, frameH: number, columns = 4): SpriteFrame[] {
  return keys.map((key, index) => ({
    key,
    x: (index % columns) * frameW,
    y: Math.floor(index / columns) * frameH,
    w: frameW,
    h: frameH,
  }));
}
