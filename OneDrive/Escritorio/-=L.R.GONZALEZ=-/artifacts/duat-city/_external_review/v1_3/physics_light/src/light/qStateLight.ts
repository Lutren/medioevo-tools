/**
 * Q-State Light — Semántica Visual Unificada
 * 
 * La luz es cambio de estado causal en un campo.
 * Cada celda emite, absorbe o transmite.
 * No traces rays infinitos; propaga estados.
 */

import { QState, WorldCell, RGB } from '../types';
import { QStateMap } from '../core/qstate';

export interface LightProfile {
  qState: QState;
  lux: number;
  color: RGB;
  description: string;
}

/**
 * Determina perfil lumínico de una celda basado en su estado Q
 */
export function computeLightProfile(cell: WorldCell): LightProfile {
  const profile = QStateMap[cell.light.qLight];

  // Modulación por material
  let lux = cell.light.emissive * 100; // base
  let color = hexToRgb(profile.color);

  // Materiales modifican la luz como "acordes"
  switch (cell.material) {
    case 'WATER':
      color = blendRgb(color, {r:20, g:40, b:80}, 0.3);
      lux *= 0.8;
      break;
    case 'FIRE':
      color = blendRgb(color, {r:255, g:100, b:20}, 0.6);
      lux *= 1.5;
      break;
    case 'NEON':
      color = blendRgb(color, {r:200, g:50, b:255}, 0.8);
      lux *= 2.0;
      break;
    case 'GLASS':
      // Cristal refracta: parciales inarmónicos de luz
      color = distortColor(color, cell.physics.pressure);
      break;
    case 'SMOKE':
      color = blendRgb(color, {r:80, g:80, b:80}, 0.5);
      lux *= 0.4;
      break;
  }

  return {
    qState: cell.light.qLight,
    lux: cell.light.receivedLux + lux,
    color,
    description: profile.light
  };
}

function hexToRgb(hex: string): RGB {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return {r, g, b};
}

function blendRgb(a: RGB, b: RGB, t: number): RGB {
  return {
    r: Math.round(a.r * (1-t) + b.r * t),
    g: Math.round(a.g * (1-t) + b.g * t),
    b: Math.round(a.b * (1-t) + b.b * t)
  };
}

function distortColor(c: RGB, pressure: number): RGB {
  // Parciales inarmónicos: desplazar canales por presión
  const shift = Math.sin(pressure * 3) * 20;
  return {
    r: Math.min(255, Math.max(0, c.r + shift)),
    g: Math.min(255, Math.max(0, c.g - shift * 0.5)),
    b: Math.min(255, Math.max(0, c.b + shift * 0.3))
  };
}
