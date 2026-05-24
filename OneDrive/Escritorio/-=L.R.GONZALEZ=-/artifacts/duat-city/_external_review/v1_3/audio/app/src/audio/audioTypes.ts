// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Types — Tipos fundamentales del motor de audio
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Certeza operacional del sistema */
export type Certeza = 'CERTEZA' | 'INFERENCIA' | 'INCOGNITA' | 'BLOQUEO';

/** Gate de acción */
export type ActionGate = 'APPROVE' | 'REVIEW' | 'BLOCK';

/** Bus de audio categorizado */
export type AudioBusName =
  | 'master'
  | 'music'
  | 'ambience'
  | 'sfx'
  | 'ui'
  | 'npc'
  | 'material'
  | 'danger';

/** Tipos de materiales que generan audio */
export type MaterialType =
  | 'water'
  | 'fire'
  | 'smoke'
  | 'neon'
  | 'metal'
  | 'glass'
  | 'crystal'
  | 'steam'
  | 'wet_stone'
  | 'stone'
  | 'wood'
  | 'sand';

/** Estados Q-state para audio glyphs */
export type QState = '00' | '01' | '10' | '11';

/** Tipos de síntesis disponibles */
export type SynthType =
  | 'oscillator'
  | 'noise'
  | 'granular'
  | 'modal'
  | 'fm'
  | 'additive'
  | 'reverb'
  | 'spatial';

/** Tipos de onda para osciladores */
export type Waveform = 'sine' | 'square' | 'sawtooth' | 'triangle';

/** Estados de emoción para NPC */
export type EmotionalState =
  | 'calm'
  | 'alert'
  | 'agitated'
  | 'fearful'
  | 'curious'
  | 'hostile'
  | 'mystical';

/** Moods de ambiente orquestal */
export type MoodType =
  | 'archive'
  | 'forge'
  | 'garden'
  | 'market'
  | 'ruin'
  | 'gate_review'
  | 'gate_block'
  | 'silence';

/** Perfil de reverberación por ubicación */
export type ReverbProfile =
  | 'catacomb'
  | 'stone_chamber'
  | 'open_cavern'
  | 'small_room'
  | 'metal_tunnel'
  | 'outdoor'
  | 'water_surface'
  | 'dense_forest';

/** Nodo del grafo de audio */
export interface AudioNodeDescriptor {
  id: string;
  type: SynthType;
  inputs: string[];
  params: Record<string, number | string | boolean>;
  outputGain: number;
  bus: AudioBusName;
}

/** Descriptor de sonido generado */
export interface SoundDescriptor {
  name: string;
  material?: MaterialType;
  nodes: AudioNodeDescriptor[];
  duration?: number;
  loop?: boolean;
  priority: number; // 0-10, mayor = más prioritario
  maxVoices: number;
  bus: AudioBusName;
}

/** Métricas en tiempo real del motor */
export interface AudioMetrics {
  activeVoices: number;
  cpuEstimate: number; // 0-1
  droppedVoices: number;
  masterGain: number;
  /** Residuo del canal de audio */
  R_audio: number;
  /** Eficiencia del audio */
  Phi_audio: number;
  clippingDetected: boolean;
  silenceDetected: boolean;
  timestamp: number;
}

/** Configuración de mezcla por bus */
export interface BusConfig {
  name: AudioBusName;
  gain: number;
  muted: boolean;
  solo: boolean;
  compressor: boolean;
  eq: boolean;
}

/** Configuración del motor */
export interface AudioEngineConfig {
  sampleRate: number;
  maxVoices: number;
  enableMetrics: boolean;
  busDefaults: BusConfig[];
  masterGain: number;
}

/** Estado del motor de audio */
export interface AudioEngineState {
  enabled: boolean;
  suspended: boolean;
  config: AudioEngineConfig;
  buses: Map<AudioBusName, BusConfig>;
  metrics: AudioMetrics;
  currentMood: MoodType;
  reverbProfile: ReverbProfile;
}

/** Estado de audio de un NPC */
export interface NPCAudioState {
  id: string;
  role: string;
  footstepMaterial: MaterialType;
  breathEnabled: boolean;
  actionMotif: string | null;
  emotionalMotif: EmotionalState;
  proximity: number; // 0-1, distancia
  R_influence: number; // cómo afecta R al audio
  Phi_influence: number; // cómo afecta Phi_eff al audio
}

/** Evento del mundo que genera audio */
export interface WorldAudioEvent {
  type: 'material' | 'light' | 'npc' | 'weather' | 'gate' | 'quest' | 'osit';
  source: string;
  position?: { x: number; y: number };
  intensity: number; // 0-1
  material?: MaterialType;
  npcState?: NPCAudioState;
  mood?: MoodType;
  qState?: QState;
  gate?: ActionGate;
}

/** Configuración de escena de audio (vibecoding) */
export interface AudioSceneConfig {
  instruments: string[];
  ambience: string[];
  sfxDensity: number; // 0-1
  musicTension: number; // 0-1
  reverbProfile: ReverbProfile;
  mixLevels: Partial<Record<AudioBusName, number>>;
  proceduralSeed: number;
  mood: MoodType;
}

/** Perfil de audio para export RPG */
export interface RPGAudioProfile {
  ambience: string[];
  music_mood: MoodType;
  motif_map: Record<string, string>;
  material_sounds: Partial<Record<MaterialType, string[]>>;
  npc_audio_rules: string[];
  location_reverb: ReverbProfile;
  gate_sounds: Partial<Record<ActionGate, string>>;
  sample_manifest_refs: string[];
  procedural_seed: number;
}

/** Descriptor de sample revisado */
export interface SampleDescriptor {
  id: string;
  name: string;
  sourceUrl: string;
  author: string;
  license: 'CC0' | 'CC-BY' | 'CC-BY-NC' | 'UNKNOWN';
  attribution?: string;
  sha256: string;
  tags: string[];
  duration: number;
  approved: boolean;
}

/** Manifest de samples */
export interface SampleManifest {
  version: string;
  samples: SampleDescriptor[];
  lastUpdated: string;
  publicationAllowed: boolean;
}

/** Resultado del parser de vibecoding */
export interface VibeParseResult {
  matched: boolean;
  config: Partial<AudioSceneConfig>;
  confidence: number;
}

/** Motif musical */
export interface Motif {
  notes: number[];
  durations: number[];
  amplitudes: number[];
  instrument: string;
  tension: number;
}

/** Progresión armónica */
export interface Harmony {
  chords: number[][];
  tensions: number[];
  rootNotes: number[];
}

/** Config de tensión */
export interface TensionConfig {
  level: number;
  intervals: number[];
  clusters: boolean;
  dissonance: number;
}

/** Envelope ADSR */
export interface ADSRConfig {
  attack: number;
  decay: number;
  sustain: number;
  release: number;
}

/** Configuración de filtro */
export interface FilterConfig {
  type: 'lowpass' | 'highpass' | 'bandpass' | 'notch' | 'lowshelf' | 'highshelf' | 'peaking';
  frequency: number;
  Q: number;
  gain?: number;
}

/** Configuración de reverb */
export interface ReverbConfig {
  duration: number; // segundos
  decay: number;
  preDelay: number;
  wet: number;
  dry: number;
}

/** Configuración espacial */
export interface SpatialConfig {
  pan: number; // -1 a 1
  distance: number; // 0 a 1
  occlusion: number; // 0 a 1
  reverbProfile: ReverbProfile;
}

/** Motor de audio en estado saludable */
export interface AudioHealthReport {
  certeza: Certeza;
  gate: ActionGate;
  R_audio: number;
  Phi_audio: number;
  voicesUsed: number;
  voicesMax: number;
  clippingEvents: number;
  enabled: boolean;
  userGestureRequired: boolean;
}
