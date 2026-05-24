// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Material Audio — Mapeo material->audio
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type MaterialType } from './audioTypes';

/** Mapeo de materiales a parámetros de audio */
export const MaterialAudioMap: Record<MaterialType, {
  sound: string;
  frequency: number;
  filter: { type: string; freq: number; Q: number };
  decay: number;
}> = {
  water: {
    sound: 'waterFlow',
    frequency: 0,
    filter: { type: 'lowpass', freq: 800, Q: 0.5 },
    decay: 0,
  },
  fire: {
    sound: 'fireCrackle',
    frequency: 0,
    filter: { type: 'bandpass', freq: 300, Q: 0.8 },
    decay: 0,
  },
  smoke: {
    sound: 'smokeBreath',
    frequency: 0,
    filter: { type: 'lowpass', freq: 200, Q: 0.3 },
    decay: 2.0,
  },
  neon: {
    sound: 'neonHum',
    frequency: 60,
    filter: { type: 'bandpass', freq: 120, Q: 2 },
    decay: 0,
  },
  metal: {
    sound: 'metalHit',
    frequency: 800,
    filter: { type: 'bandpass', freq: 3000, Q: 8 },
    decay: 2.0,
  },
  glass: {
    sound: 'glassCrystal',
    frequency: 1200,
    filter: { type: 'highpass', freq: 2000, Q: 4 },
    decay: 4.0,
  },
  crystal: {
    sound: 'glassCrystal',
    frequency: 1500,
    filter: { type: 'highpass', freq: 2500, Q: 6 },
    decay: 5.0,
  },
  steam: {
    sound: 'steamPipe',
    frequency: 0,
    filter: { type: 'bandpass', freq: 2000, Q: 2 },
    decay: 0.3,
  },
  stone: {
    sound: 'metalHit',
    frequency: 400,
    filter: { type: 'lowpass', freq: 600, Q: 1 },
    decay: 0.4,
  },
  wet_stone: {
    sound: 'waterFlow',
    frequency: 0,
    filter: { type: 'lowpass', freq: 500, Q: 0.7 },
    decay: 0,
  },
  wood: {
    sound: 'metalHit',
    frequency: 600,
    filter: { type: 'lowpass', freq: 1200, Q: 1.2 },
    decay: 0.8,
  },
  sand: {
    sound: 'smokeBreath',
    frequency: 0,
    filter: { type: 'lowpass', freq: 300, Q: 0.5 },
    decay: 0.1,
  },
};
