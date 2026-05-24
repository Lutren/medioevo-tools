/**
 * Delta Framebuffer — Memoria Selectiva
 * 
 * El motor no redibuja todo. Solo redibuja lo que cambió.
 * Esto no es optimización; es atención.
 * El mundo, como un narrador, no describe lo que no cambia.
 */

export interface DirtyTile {
  tx: number;  // tile x
  ty: number;  // tile y
  reason: 'PHYSICS' | 'LIGHT' | 'MATERIAL' | 'NPC' | 'FORCED';
  timestamp: number;
}

export class DeltaFramebuffer {
  private tileSize: number;
  private width: number;
  private height: number;
  private dirtyTiles: Map<string, DirtyTile> = new Map();
  private frameBuffer: ImageData | null = null;
  private canvas: HTMLCanvasElement | null = null;
  private ctx: CanvasRenderingContext2D | null = null;

  constructor(tileSize: number = 16, width: number = 800, height: number = 600) {
    this.tileSize = tileSize;
    this.width = width;
    this.height = height;
  }

  attachCanvas(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    canvas.width = this.width;
    canvas.height = this.height;
    this.frameBuffer = this.ctx!.createImageData(this.width, this.height);
  }

  /**
   * Marcar tile como dirty
   */
  markDirty(tx: number, ty: number, reason: DirtyTile['reason'], frame: number) {
    const key = `${tx},${ty}`;
    this.dirtyTiles.set(key, { tx, ty, reason, timestamp: frame });
  }

  /**
   * Marcar región alrededor de un punto
   */
  markRegionDirty(x: number, y: number, radius: number, reason: DirtyTile['reason'], frame: number) {
    const t0x = Math.floor((x - radius) / this.tileSize);
    const t0y = Math.floor((y - radius) / this.tileSize);
    const t1x = Math.ceil((x + radius) / this.tileSize);
    const t1y = Math.ceil((y + radius) / this.tileSize);

    for (let ty = t0y; ty <= t1y; ty++) {
      for (let tx = t0x; tx <= t1x; tx++) {
        this.markDirty(tx, ty, reason, frame);
      }
    }
  }

  /**
   * Obtener tiles sucios y limpiar
   */
  flushDirty(): DirtyTile[] {
    const tiles = Array.from(this.dirtyTiles.values());
    this.dirtyTiles.clear();
    return tiles;
  }

  /**
   * Verificar si tile está en bounds
   */
  isValidTile(tx: number, ty: number): boolean {
    return tx >= 0 && ty >= 0 && 
           tx * this.tileSize < this.width && 
           ty * this.tileSize < this.height;
  }

  getTileSize(): number { return this.tileSize; }
  getWidth(): number { return this.width; }
  getHeight(): number { return this.height; }
  getContext(): CanvasRenderingContext2D | null { return this.ctx; }
}
