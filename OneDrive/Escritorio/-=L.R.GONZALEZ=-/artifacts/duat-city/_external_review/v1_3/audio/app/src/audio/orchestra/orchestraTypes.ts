// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Orchestra Types — Tipos del motor orquestal
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Instrumento sintético */
export interface SyntheticInstrument {
  name: string;
  category: 'strings' | 'brass' | 'choir' | 'percussion' | 'other';
  fundamental: number;
  timbre: string;
  attack: number;
  decay: number;
  sustain: number;
  release: number;
}

/** Motif musical */
export interface Motif {
  notes: number[]; // frecuencias
  durations: number[];
  amplitudes: number[];
  instrument: string;
  tension: number; // 0-1
}

/** Progresión armónica */
export interface Harmony {
  chords: number[][]; // cada acorde = array de frecuencias
  tensions: number[]; // tensión de cada acorde
  rootNotes: number[];
}

/** Config de tensión */
export interface TensionConfig {
  level: number; // 0-1
  intervals: number[]; // intervalos en semitonos
  clusters: boolean;
  dissonance: number;
}
