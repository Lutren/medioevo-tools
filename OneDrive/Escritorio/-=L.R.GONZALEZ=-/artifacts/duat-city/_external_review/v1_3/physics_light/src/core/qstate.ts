/**
 * Q-State Unificado — Audio, Luz, Física, Mecánicas
 * 
 * Codificación:
 * 00 = silence/low — oscuridad esperada, calma física, silencio
 * 01 = missing/anomaly — señal ausente, anomalía lumínica, inestabilidad
 * 10 = stable — iluminación estable, física predecible, tono sostenido
 * 11 = burst/event — evento lumínico, colisión, gate abierto, burst sonoro
 */

import { QState } from '../types';

export interface QStateProfile {
  label: string;
  audio: string;
  light: string;
  physics: string;
  mechanics: string;
  color: string;
}

export const QStateMap: Record<QState, QStateProfile> = {
  '00': {
    label: 'Silencio / Oscuridad Esperada',
    audio: 'low hum o silence',
    light: 'oscuridad estable, sin sorpresas',
    physics: 'equilibrio, inercia mínima',
    mechanics: 'zona segura, recuperación',
    color: '#1a1a2e'
  },
  '01': {
    label: 'Señal Ausente / Anomalía',
    audio: 'missing signal pulse',
    light: 'luz que debería estar y no está',
    physics: 'inestabilidad, precursor de cambio',
    mechanics: 'intriga, quest hook',
    color: '#4a0e4e'
  },
  '10': {
    label: 'Estable / Confirmado',
    audio: 'tono sostenido, armónico',
    light: 'iluminación natural del entorno',
    physics: 'movimiento predecible, colisiones normales',
    mechanics: 'progresión normal',
    color: '#e8dcc8'
  },
  '11': {
    label: 'Burst / Evento',
    audio: 'event burst, gate sound',
    light: 'flash, emisión brusca, revelación',
    physics: 'colisión, explosión, transición de fase',
    mechanics: 'gate abierto, NPC reactivo, quest trigger',
    color: '#ff6b35'
  }
};

/**
 * Transición Q-State desde dos estados vecinos (operación tipo Conway)
 */
export function qTransition(a: QState, b: QState): QState {
  const table: Record<string, QState> = {
    '00+00': '00', '00+01': '01', '00+10': '01', '00+11': '01',
    '01+00': '01', '01+01': '00', '01+10': '10', '01+11': '11',
    '10+00': '01', '10+01': '10', '10+10': '10', '10+11': '11',
    '11+00': '01', '11+01': '11', '11+10': '11', '11+11': '10'
  };
  const key = `${a}+${b}`;
  return table[key] || '10';
}

/**
 * Agregación Q-State múltiple (votación ponderada)
 */
export function qAggregate(states: QState[], weights?: number[]): QState {
  const w = weights || states.map(() => 1);
  let score = 0;
  for (let i = 0; i < states.length; i++) {
    const val = states[i] === '00' ? 0 : states[i] === '01' ? 1 : states[i] === '10' ? 2 : 3;
    score += val * w[i];
  }
  const avg = score / w.reduce((a, b) => a + b, 0);
  if (avg < 0.5) return '00';
  if (avg < 1.5) return '01';
  if (avg < 2.5) return '10';
  return '11';
}
