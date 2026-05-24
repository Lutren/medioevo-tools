/**
 * Cuerpo Calloso / Cross-Modal Transduction Engine
 * 
 * Conecta todas las cortezas.
 * Un evento en una modalidad genera deltas en las demás.
 * 
 * Luz → Audio (ya implementado en v1.3.0)
 * Física → Audio (ya implementado en v1.3.0)
 * Aquí: Audio → Luz, Audio → Física, Luz → Física, Física → Luz
 * 
 * Principio: el mundo no tiene canales separados.
 * Tiene un campo que se filtra de diferentes maneras.
 */

import { CrossModalEvent, WorldCell, AudioEvent, QState } from '../../types';

export class CrossModalTransduction {
  private events: CrossModalEvent[] = [];
  private maxEvents = 128;

  /**
   * Audio → Luz: un sonido fuerte genera un flash
   */
  audioToLight(audio: AudioEvent, cells: WorldCell[]): CrossModalEvent[] {
    const events: CrossModalEvent[] = [];
    if (audio.intensity < 0.5) return events;

    // Encontrar celda más cercana al evento
    const target = cells.find(c => 
      c.audio?.eventQueue?.includes(audio)
    );

    if (target) {
      events.push({
        source: 'audio',
        target: 'light',
        delta: {
          emissive: audio.intensity * 0.3,
          qLight: this.intensityToQ(audio.intensity),
          duration: audio.intensity * 10
        },
        timestamp: audio.timestamp,
        confidence: audio.intensity
      });
    }

    return events;
  }

  /**
   * Audio → Física: un golpe fuerte genera vibración/pressure
   */
  audioToPhysics(audio: AudioEvent, cells: WorldCell[]): CrossModalEvent[] {
    const events: CrossModalEvent[] = [];
    if (audio.intensity < 0.7) return events;

    const target = cells.find(c => 
      c.audio?.eventQueue?.includes(audio)
    );

    if (target) {
      events.push({
        source: 'audio',
        target: 'physics',
        delta: {
          pressure: audio.intensity * 2,
          velocity: {
            x: (Math.random() - 0.5) * audio.intensity * 10,
            y: (Math.random() - 0.5) * audio.intensity * 10
          }
        },
        timestamp: audio.timestamp,
        confidence: audio.intensity
      });
    }

    return events;
  }

  /**
   * Luz → Física: luz intensa genera calor/pressure
   */
  lightToPhysics(cell: WorldCell): CrossModalEvent[] {
    const events: CrossModalEvent[] = [];
    if (cell.light.receivedLux < 50) return events;

    events.push({
      source: 'light',
      target: 'physics',
      delta: {
        temperature: cell.light.receivedLux * 0.1,
        pressure: cell.light.receivedLux * 0.01
      },
      timestamp: Date.now(),
      confidence: Math.min(1, cell.light.receivedLux / 100)
    });

    return events;
  }

  /**
   * Física → Luz: colisiones generan sparks
   */
  physicsToLight(cell: WorldCell): CrossModalEvent[] {
    const events: CrossModalEvent[] = [];
    const v = Math.hypot(cell.physics.velocity.x, cell.physics.velocity.y);
    if (v < 30) return events;

    events.push({
      source: 'physics',
      target: 'light',
      delta: {
        emissive: Math.min(1, v / 100),
        qLight: '11' as QState,
        color: { r: 255, g: 200, b: 100 }
      },
      timestamp: Date.now(),
      confidence: Math.min(1, v / 100)
    });

    return events;
  }

  /**
   * Procesar todas las celdas y generar eventos cruzados
   */
  processAll(cells: WorldCell[]): CrossModalEvent[] {
    const allEvents: CrossModalEvent[] = [];

    for (const cell of cells) {
      // Luz → Física
      allEvents.push(...this.lightToPhysics(cell));

      // Física → Luz
      allEvents.push(...this.physicsToLight(cell));

      // Audio → otros (si hay eventos de audio pendientes)
      if (cell.audio?.eventQueue) {
        for (const audio of cell.audio.eventQueue) {
          allEvents.push(...this.audioToLight(audio, [cell]));
          allEvents.push(...this.audioToPhysics(audio, [cell]));
        }
      }
    }

    this.events.push(...allEvents);
    if (this.events.length > this.maxEvents) {
      this.events = this.events.slice(-this.maxEvents);
    }

    return allEvents;
  }

  private intensityToQ(intensity: number): QState {
    if (intensity < 0.25) return '00';
    if (intensity < 0.5) return '01';
    if (intensity < 0.75) return '10';
    return '11';
  }

  getEvents(): CrossModalEvent[] { return [...this.events]; }
  getEventsBySource(source: string): CrossModalEvent[] {
    return this.events.filter(e => e.source === source);
  }
}
