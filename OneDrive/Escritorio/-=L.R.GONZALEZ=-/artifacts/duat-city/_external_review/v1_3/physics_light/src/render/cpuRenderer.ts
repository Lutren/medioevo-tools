/**
 * CPU Renderer — Render CPU-First, Paleta Indexada
 * 
 * CPU-first + pixel-art realista es decisión de voz, no limitación.
 * Paleta indexada como vocabulario restringido:
 * un escritor fuerte no usa todas las palabras del diccionario.
 */

import { WorldCell, RGB } from '../types';
import { DeltaFramebuffer, DirtyTile } from './deltaFramebuffer';
import { computeLightProfile } from '../light/qStateLight';
import { fibMobLOD } from '../core/fibmob';
import { QStateMap } from '../core/qstate';

export interface RenderConfig {
  enablePalette: boolean;
  enableQColor: boolean;
  enableLOD: boolean;
}

export class CPURenderer {
  private fb: DeltaFramebuffer;
  private config: RenderConfig;
  private palette: Map<string, RGB> = new Map();

  constructor(fb: DeltaFramebuffer, config: RenderConfig = {
    enablePalette: true,
    enableQColor: true,
    enableLOD: true
  }) {
    this.fb = fb;
    this.config = config;
    this.initPalette();
  }

  private initPalette() {
    // Paleta por material (vocabulario restringido por escena)
    this.palette.set('VOID',     {r:10, g:10, b:20});
    this.palette.set('STONE',    {r:80, g:75, b:70});
    this.palette.set('WATER',    {r:40, g:70, b:120});
    this.palette.set('FIRE',     {r:220, g:80, b:20});
    this.palette.set('SMOKE',    {r:60, g:60, b:65});
    this.palette.set('METAL',    {r:140, g:145, b:150});
    this.palette.set('GLASS',    {r:180, g:210, b:220});
    this.palette.set('NEON',     {r:200, g:50, b:255});
    this.palette.set('STEAM',    {r:200, g:200, b:210});
    this.palette.set('ORGANIC',  {r:60, g:120, b:60});
  }

  /**
   * Renderizar frame: solo tiles dirty
   */
  render(cells: WorldCell[], cameraX: number, cameraY: number, frame: number): void {
    const ctx = this.fb.getContext();
    if (!ctx) return;

    const dirtyTiles = this.fb.flushDirty();
    const tileSize = this.fb.getTileSize();

    for (const tile of dirtyTiles) {
      if (!this.fb.isValidTile(tile.tx, tile.ty)) continue;

      // LOD por distancia a cámara
      const worldX = tile.tx * tileSize + tileSize/2;
      const worldY = tile.ty * tileSize + tileSize/2;
      const dist = Math.hypot(worldX - cameraX, worldY - cameraY);
      const lod = this.config.enableLOD ? fibMobLOD(dist, 64) : 1;

      const drawSize = tileSize * lod;
      const px = tile.tx * tileSize;
      const py = tile.ty * tileSize;

      // Encontrar celda en este tile
      const cell = cells.find(c => {
        const ctx = Math.floor(c.x / tileSize);
        const cty = Math.floor(c.y / tileSize);
        return ctx === tile.tx && cty === tile.ty;
      });

      if (!cell) {
        // Void
        ctx.fillStyle = '#0a0a14';
        ctx.fillRect(px, py, drawSize, drawSize);
        continue;
      }

      // Color base
      let color = this.palette.get(cell.material) || {r:128, g:128, b:128};

      // Modulación por luz
      const lightProfile = computeLightProfile(cell);
      const luxFactor = Math.min(1, lightProfile.lux / 50);

      color = {
        r: Math.min(255, color.r * (0.3 + 0.7 * luxFactor) + lightProfile.color.r * luxFactor * 0.3),
        g: Math.min(255, color.g * (0.3 + 0.7 * luxFactor) + lightProfile.color.g * luxFactor * 0.3),
        b: Math.min(255, color.b * (0.3 + 0.7 * luxFactor) + lightProfile.color.b * luxFactor * 0.3)
      };

      // Q-State color override
      if (this.config.enableQColor) {
        const qColor = hexToRgb(QStateMap[cell.light.qLight].color);
        color = blendRgb(color, qColor, 0.2 * luxFactor);
      }

      // Dithering Fibonacci para sombras suaves
      const dither = fibonacciDither(px, py, luxFactor);
      color = {
        r: Math.min(255, color.r + dither),
        g: Math.min(255, color.g + dither),
        b: Math.min(255, color.b + dither)
      };

      ctx.fillStyle = `rgb(${Math.floor(color.r)},${Math.floor(color.g)},${Math.floor(color.b)})`;
      ctx.fillRect(px, py, drawSize, drawSize);

      // Borde sutil para definición pixel-art
      if (lod === 1) {
        ctx.strokeStyle = 'rgba(0,0,0,0.2)';
        ctx.lineWidth = 0.5;
        ctx.strokeRect(px, py, tileSize, tileSize);
      }
    }
  }

  setPalette(material: string, color: RGB) {
    this.palette.set(material, color);
  }
}

function hexToRgb(hex: string): RGB {
  return {
    r: parseInt(hex.slice(1,3), 16),
    g: parseInt(hex.slice(3,5), 16),
    b: parseInt(hex.slice(5,7), 16)
  };
}

function blendRgb(a: RGB, b: RGB, t: number): RGB {
  return {
    r: a.r * (1-t) + b.r * t,
    g: a.g * (1-t) + b.g * t,
    b: a.b * (1-t) + b.b * t
  };
}

function fibonacciDither(x: number, y: number, intensity: number): number {
  // Secuencia de Fibonacci para dithering espacial
  const fib = [1, 1, 2, 3, 5, 8, 13, 21];
  const idx = (x * 3 + y * 5) % fib.length;
  const noise = (fib[idx] / 21) - 0.5;
  return noise * 10 * intensity;
}
