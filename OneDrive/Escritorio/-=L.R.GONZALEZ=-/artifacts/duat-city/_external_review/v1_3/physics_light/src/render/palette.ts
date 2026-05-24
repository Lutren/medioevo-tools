/**
 * Paleta Indexada — Vocabulario Restringido
 * 
 * 64-128 colores por escena, elegidos como personajes de reparto.
 * Cada color tiene un rol.
 * "El azul del archivo" no es solo azul;
 * es el azul de los documentos que no deberían existir.
 */

import { RGB } from '../types';

export interface PaletteEntry {
  name: string;
  color: RGB;
  role: string;        // qué representa narrativamente
  material?: string;    // a qué material se asigna
  qState?: string;      // en qué Q-state predomina
}

export class IndexedPalette {
  private colors: PaletteEntry[] = [];
  private index: Map<string, number> = new Map();

  constructor() {
    this.initBasePalette();
  }

  private initBasePalette() {
    this.add({ name: 'archive_blue', color: {r:30, g:40, b:80}, role: 'documents forbidden', material: 'STONE', qState: '01' });
    this.add({ name: 'forge_orange', color: {r:200, g:80, b:20}, role: 'heat and work', material: 'METAL', qState: '11' });
    this.add({ name: 'garden_green', color: {r:60, g:140, b:70}, role: 'life hidden', material: 'ORGANIC', qState: '10' });
    this.add({ name: 'neon_purple', color: {r:180, g:40, b:220}, role: 'electric soul', material: 'NEON', qState: '11' });
    this.add({ name: 'water_deep', color: {r:20, g:50, b:100}, role: 'memory flow', material: 'WATER', qState: '00' });
    this.add({ name: 'smoke_grey', color: {r:90, g:90, b:95}, role: 'truth obscured', material: 'SMOKE', qState: '01' });
    this.add({ name: 'crystal_white', color: {r:200, g:220, b:230}, role: 'clarity fragile', material: 'GLASS', qState: '10' });
    this.add({ name: 'void_black', color: {r:10, g:10, b:15}, role: 'absence', material: 'VOID', qState: '00' });
    this.add({ name: 'ember_red', color: {r:220, g:40, b:30}, role: 'warning', material: 'FIRE', qState: '11' });
    this.add({ name: 'stone_brown', color: {r:100, g:90, b:80}, role: 'foundation', material: 'STONE', qState: '10' });
  }

  add(entry: PaletteEntry): number {
    const idx = this.colors.length;
    this.colors.push(entry);
    this.index.set(entry.name, idx);
    return idx;
  }

  get(name: string): PaletteEntry | undefined {
    const idx = this.index.get(name);
    return idx !== undefined ? this.colors[idx] : undefined;
  }

  getByMaterial(material: string): PaletteEntry[] {
    return this.colors.filter(c => c.material === material);
  }

  getByQState(q: string): PaletteEntry[] {
    return this.colors.filter(c => c.qState === q);
  }

  getAll(): PaletteEntry[] { return this.colors; }
  size(): number { return this.colors.length; }
}
