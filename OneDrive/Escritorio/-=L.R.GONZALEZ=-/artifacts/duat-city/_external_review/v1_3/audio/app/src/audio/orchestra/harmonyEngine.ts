// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Harmony Engine — Motor de armonía procedural
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type MoodType } from '../audioTypes';

const PHI = 1.618033988749895;

/** Acordes por tipo */
const ChordTypes: Record<string, number[]> = {
  major: [0, 4, 7],
  minor: [0, 3, 7],
  diminished: [0, 3, 6],
  augmented: [0, 4, 8],
  sus2: [0, 2, 7],
  sus4: [0, 5, 7],
  maj7: [0, 4, 7, 11],
  min7: [0, 3, 7, 10],
  dom7: [0, 4, 7, 10],
  open5: [0, 7],
  cluster: [0, 1, 2, 3],
};

/** Progresiones por mood */
const MoodProgressions: Record<string, string[]> = {
  archive: ['minor', 'sus4', 'minor', 'open5'],
  forge: ['open5', 'major', 'sus4', 'major'],
  garden: ['major', 'maj7', 'sus2', 'major'],
  market: ['sus4', 'dom7', 'sus2', 'dom7'],
  ruin: ['diminished', 'minor', 'open5', 'cluster'],
  gate_review: ['sus4', 'sus2', 'major', 'sus4'],
  gate_block: ['diminished', 'cluster', 'augmented', 'diminished'],
  silence: ['open5', 'open5'],
};

/** Motor de armonía procedural */
export class HarmonyEngine {
  constructor(_seed = Date.now()) {
    // seed reserved for future randomized generation
  }

  /** Genera progresión armónica para un mood */
  generateProgression(
    mood: MoodType,
    rootFreq = 220,
    length = 4
  ): { chords: number[][]; tensions: number[]; rootNotes: number[] } {
    const chordTypes = MoodProgressions[mood] || MoodProgressions.archive;
    const chords: number[][] = [];
    const tensions: number[] = [];
    const rootNotes: number[] = [];

    // Inversiones del círculo de quintas con φ
    const circleOfFifths = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5];

    for (let i = 0; i < length; i++) {
      const chordType = chordTypes[i % chordTypes.length];
      const intervals = ChordTypes[chordType] || ChordTypes.minor;

      // Root note basada en posición del círculo con variación φ
      const rootIndex = Math.floor((i * PHI) % circleOfFifths.length);
      const rootSemitone = circleOfFifths[rootIndex];
      const rootNote = rootFreq * Math.pow(2, rootSemitone / 12);

      const chord = intervals.map(interval => rootNote * Math.pow(2, interval / 12));

      chords.push(chord);
      rootNotes.push(rootNote);

      // Tensión basada en tipo de acorde
      tensions.push(this.calculateChordTension(chordType));
    }

    return { chords, tensions, rootNotes };
  }

  /** Calma: quintas, octavas, cuartas abiertas */
  generateCalmHarmony(rootFreq = 220): { chords: number[][]; tensions: number[]; rootNotes: number[] } {
    const calmChords = ['open5', 'sus2', 'major', 'sus4'];
    const chords: number[][] = [];
    const tensions: number[] = [];
    const rootNotes: number[] = [];

    for (let i = 0; i < 4; i++) {
      const intervals = ChordTypes[calmChords[i]];
      const root = rootFreq * Math.pow(2, i * 5 / 12); // Quintas ascendentes
      chords.push(intervals.map(interval => root * Math.pow(2, interval / 12)));
      rootNotes.push(root);
      tensions.push(0.2);
    }

    return { chords, tensions, rootNotes };
  }

  /** Tensión: menores, tritonos, clusters */
  generateTensionHarmony(rootFreq = 220, level = 0.7): { chords: number[][]; tensions: number[]; rootNotes: number[] } {
    const tenseChords = level > 0.8
      ? ['diminished', 'cluster', 'augmented']
      : ['minor', 'diminished', 'dom7'];

    const chords: number[][] = [];
    const tensions: number[] = [];
    const rootNotes: number[] = [];

    for (let i = 0; i < 3; i++) {
      const intervals = ChordTypes[tenseChords[i]];
      const root = rootFreq * (1 + i * 0.1);
      chords.push(intervals.map(interval => root * Math.pow(2, interval / 12)));
      rootNotes.push(root);
      tensions.push(0.5 + level * 0.5);
    }

    return { chords, tensions, rootNotes };
  }

  private calculateChordTension(chordType: string): number {
    const tensionMap: Record<string, number> = {
      major: 0.2,
      minor: 0.35,
      diminished: 0.75,
      augmented: 0.7,
      sus2: 0.25,
      sus4: 0.4,
      maj7: 0.15,
      min7: 0.4,
      dom7: 0.5,
      open5: 0.1,
      cluster: 0.9,
    };
    return tensionMap[chordType] || 0.5;
  }

  /** Resuelve tensión a acorde estable */
  resolveTension(fromTension: number, rootFreq = 220): number[] {
    if (fromTension > 0.7) {
      // Resolución dramática
      return ChordTypes.major.map(interval => rootFreq * Math.pow(2, interval / 12));
    } else if (fromTension > 0.4) {
      // Resolución suave
      return ChordTypes.sus4.map(interval => rootFreq * Math.pow(2, interval / 12));
    }
    return ChordTypes.open5.map(interval => rootFreq * Math.pow(2, interval / 12));
  }
}
