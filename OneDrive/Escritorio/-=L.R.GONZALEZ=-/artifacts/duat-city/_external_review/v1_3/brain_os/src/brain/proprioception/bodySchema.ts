/**
 * Propiocepción / Body Schema Engine
 * 
 * El cerebro necesita saber dónde está su "cuerpo" en el mundo.
 * En el motor, el "cuerpo" es la cámara + el player + los NPCs activos.
 * 
 * Trackea quién es el observador principal, dónde está su atención,
 * y qué recursos sensoriales tiene disponibles.
 * 
 * Principio: sin cuerpo no hay perspectiva.
 * Sin perspectiva no hay mundo.
 */

import { BodySchema, Vec2, WorldCell } from '../../types';

export interface SensorModality {
  name: string;
  range: number;
  resolution: number;
  enabled: boolean;
  latency: number;
}

export class BodySchemaEngine {
  private schema: BodySchema;
  private modalities: Map<string, SensorModality> = new Map();
  private attentionHistory: Vec2[] = [];
  private maxHistory = 16;

  constructor(initialPosition: Vec2 = {x: 0, y: 0}) {
    this.schema = {
      observerPosition: initialPosition,
      attentionFocus: initialPosition,
      sensorRange: 200,
      availableModalities: ['visual', 'audio', 'haptic'],
      currentModality: 'visual'
    };

    this.modalities.set('visual', { name: 'visual', range: 300, resolution: 1, enabled: true, latency: 0 });
    this.modalities.set('audio', { name: 'audio', range: 400, resolution: 0.5, enabled: true, latency: 0.01 });
    this.modalities.set('haptic', { name: 'haptic', range: 50, resolution: 2, enabled: true, latency: 0.05 });
  }

  /**
   * Actualizar posición del observador
   */
  moveObserver(position: Vec2) {
    this.schema.observerPosition = position;
  }

  /**
   * Mover atención (no necesariamente donde está el cuerpo)
   */
  shiftAttention(focus: Vec2) {
    this.attentionHistory.push(focus);
    if (this.attentionHistory.length > this.maxHistory) this.attentionHistory.shift();
    this.schema.attentionFocus = focus;
  }

  /**
   * Calcular velocidad de atención (dónde está yendo la mirada)
   */
  attentionVelocity(): Vec2 {
    if (this.attentionHistory.length < 2) return {x: 0, y: 0};
    const last = this.attentionHistory[this.attentionHistory.length - 1];
    const prev = this.attentionHistory[this.attentionHistory.length - 2];
    return {
      x: last.x - prev.x,
      y: last.y - prev.y
    };
  }

  /**
   * Determinar qué celdas están dentro del alcance sensorial
   */
  perceive(cells: WorldCell[]): WorldCell[] {
    const modality = this.modalities.get(this.schema.currentModality);
    if (!modality || !modality.enabled) return [];

    return cells.filter(c => {
      const dist = Math.hypot(c.x - this.schema.attentionFocus.x, c.y - this.schema.attentionFocus.y);
      return dist <= modality.range;
    });
  }

  /**
   * Cambiar modalidad sensorial
   */
  switchModality(name: string) {
    if (this.modalities.has(name)) {
      this.schema.currentModality = name;
    }
  }

  /**
   * Calcular "sensación" de proximidad a peligro
   */
  proximitySense(cells: WorldCell[]): number {
    let danger = 0;
    for (const c of cells) {
      if (c.material === 'FIRE' || c.material === 'DANGER') {
        const dist = Math.hypot(c.x - this.schema.observerPosition.x, c.y - this.schema.observerPosition.y);
        if (dist < 100) danger += (100 - dist) / 100;
      }
    }
    return Math.min(1, danger);
  }

  /**
   * Calcular "sensación" de estabilidad del suelo
   */
  groundSense(cells: WorldCell[]): number {
    const below = cells.find(c => 
      Math.abs(c.x - this.schema.observerPosition.x) < 10 &&
      c.y > this.schema.observerPosition.y &&
      c.y < this.schema.observerPosition.y + 50
    );
    if (!below) return 0; // vacío
    if (below.material === 'STONE' || below.material === 'METAL') return 1;
    if (below.material === 'WATER') return 0.3;
    if (below.material === 'ORGANIC') return 0.7;
    return 0.5;
  }

  getSchema(): BodySchema { return { ...this.schema }; }
  getModalities(): SensorModality[] { return Array.from(this.modalities.values()); }
  getModality(name: string): SensorModality | undefined { return this.modalities.get(name); }
}
