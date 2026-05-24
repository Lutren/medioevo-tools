// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Engine — Core del motor de audio
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import {
  type AudioEngineConfig,
  type AudioEngineState,
  type AudioMetrics,
  type AudioBusName,
  type AudioHealthReport,
  type SoundDescriptor,
  type MoodType,
  type ReverbProfile,
} from './audioTypes';
import { AudioBus } from './audioBus';
import { AudioMixer } from './audioMixer';
import { AudioMetricsCollector } from './audioMetrics';
import { AudioGraph } from './audioGraph';
import { AudioClock } from './audioClock';

const DEFAULT_CONFIG: AudioEngineConfig = {
  sampleRate: 44100,
  maxVoices: 32,
  enableMetrics: true,
  masterGain: 0.8,
  busDefaults: [
    { name: 'master', gain: 0.8, muted: false, solo: false, compressor: true, eq: false },
    { name: 'music', gain: 0.6, muted: false, solo: false, compressor: true, eq: true },
    { name: 'ambience', gain: 0.7, muted: false, solo: false, compressor: false, eq: true },
    { name: 'sfx', gain: 0.9, muted: false, solo: false, compressor: true, eq: false },
    { name: 'ui', gain: 1.0, muted: false, solo: false, compressor: false, eq: false },
    { name: 'npc', gain: 0.75, muted: false, solo: false, compressor: true, eq: true },
    { name: 'material', gain: 0.8, muted: false, solo: false, compressor: false, eq: true },
    { name: 'danger', gain: 1.0, muted: false, solo: false, compressor: true, eq: false },
  ],
};

/** Core del motor de audio procedural */
export class AudioEngine {
  private ctx: AudioContext | null = null;
  private config: AudioEngineConfig;
  private buses: Map<AudioBusName, AudioBus> = new Map();
  private mixer: AudioMixer;
  private metrics: AudioMetricsCollector;
  private graph: AudioGraph;
  private clock: AudioClock;
  private enabled = false;
  private userGestureReceived = false;
  private masterGainNode: GainNode | null = null;
  private compressorNode: DynamicsCompressorNode | null = null;
  private voicePool: GainNode[] = [];
  private activeSounds: Map<string, SoundDescriptor> = new Map();
  private currentMood: MoodType = 'silence';
  private currentReverb: ReverbProfile = 'catacomb';

  constructor(config?: Partial<AudioEngineConfig>) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.mixer = new AudioMixer(this.config.busDefaults);
    this.metrics = new AudioMetricsCollector();
    this.graph = new AudioGraph();
    this.clock = new AudioClock(this.config.sampleRate);
  }

  /** Inicializa el AudioContext (requiere user gesture) */
  async init(): Promise<boolean> {
    try {
      if (typeof window === 'undefined') {
        console.log('[DUAT-AUDIO] Entorno sin browser — modo mock');
        return this.initMock();
      }

      this.ctx = new AudioContext({
        sampleRate: this.config.sampleRate,
        latencyHint: 'interactive',
      });

      // Master compressor para prevenir clipping
      this.compressorNode = this.ctx.createDynamicsCompressor();
      this.compressorNode.threshold.setValueAtTime(-12, this.ctx.currentTime);
      this.compressorNode.knee.setValueAtTime(6, this.ctx.currentTime);
      this.compressorNode.ratio.setValueAtTime(12, this.ctx.currentTime);
      this.compressorNode.attack.setValueAtTime(0.003, this.ctx.currentTime);
      this.compressorNode.release.setValueAtTime(0.1, this.ctx.currentTime);

      // Master gain
      this.masterGainNode = this.ctx.createGain();
      this.masterGainNode.gain.setValueAtTime(this.config.masterGain, this.ctx.currentTime);

      // Chain: compressor -> masterGain -> destination
      this.compressorNode.connect(this.masterGainNode);
      this.masterGainNode.connect(this.ctx.destination);

      // Inicializar buses
      for (const busConfig of this.config.busDefaults) {
        const bus = new AudioBus(busConfig, this.ctx);
        bus.connect(this.compressorNode);
        this.buses.set(busConfig.name, bus);
      }

      // Voice pool para reuso de nodos
      this.initVoicePool();

      this.clock.start(this.ctx);

      console.log('[DUAT-AUDIO] Engine inicializado — sampleRate:', this.config.sampleRate);
      return true;
    } catch (err) {
      console.warn('[DUAT-AUDIO] Error inicializando:', err);
      return this.initMock();
    }
  }

  /** Inicialización mock para entornos sin browser */
  private initMock(): boolean {
    this.enabled = false;
    this.metrics.setMockMode(true);
    console.log('[DUAT-AUDIO] Modo mock activado');
    return true;
  }

  /** Crea pool de voces para reuso */
  private initVoicePool(): void {
    if (!this.ctx) return;
    for (let i = 0; i < this.config.maxVoices; i++) {
      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0, this.ctx.currentTime);
      this.voicePool.push(gain);
    }
  }

  /** Habilita audio tras user gesture */
  async enable(): Promise<boolean> {
    if (this.enabled) return true;
    if (!this.ctx) {
      const ok = await this.init();
      if (!ok) return false;
    }
    if (this.ctx?.state === 'suspended') {
      await this.ctx.resume();
    }
    this.userGestureReceived = true;
    this.enabled = true;
    console.log('[DUAT-AUDIO] Audio habilitado por usuario');
    return true;
  }

  /** Deshabilita audio */
  disable(): void {
    this.enabled = false;
    if (this.masterGainNode) {
      this.masterGainNode.gain.setTargetAtTime(0, this.ctx?.currentTime ?? 0, 0.1);
    }
    console.log('[DUAT-AUDIO] Audio deshabilitado');
  }

  /** Está el audio habilitado? */
  isEnabled(): boolean {
    return this.enabled;
  }

  /** Se recibió user gesture? */
  hasUserGesture(): boolean {
    return this.userGestureReceived;
  }

  /** Obtiene el AudioContext */
  getContext(): AudioContext | null {
    return this.ctx;
  }

  /** Obtiene configuración */
  getConfig(): AudioEngineConfig {
    return { ...this.config };
  }

  /** Obtiene un bus */
  getBus(name: AudioBusName): AudioBus | undefined {
    return this.buses.get(name);
  }

  /** Obtiene el mixer */
  getMixer(): AudioMixer {
    return this.mixer;
  }

  /** Obtiene métricas actuales */
  getMetrics(): AudioMetrics {
    return this.metrics.getMetrics();
  }

  /** Obtiene el grafo */
  getGraph(): AudioGraph {
    return this.graph;
  }

  /** Obtiene el reloj */
  getClock(): AudioClock {
    return this.clock;
  }

  /** Establece master gain */
  setMasterGain(value: number): void {
    const clamped = Math.max(0, Math.min(1, value));
    this.config.masterGain = clamped;
    if (this.masterGainNode && this.ctx) {
      this.masterGainNode.gain.setTargetAtTime(clamped, this.ctx.currentTime, 0.01);
    }
  }

  /** Establece gain de bus */
  setBusGain(bus: AudioBusName, value: number): void {
    const b = this.buses.get(bus);
    if (b) b.setGain(value);
    this.mixer.setBusGain(bus, value);
  }

  /** Mute/unmute bus */
  setBusMute(bus: AudioBusName, muted: boolean): void {
    const b = this.buses.get(bus);
    if (b) b.setMute(muted);
  }

  /** Mute all */
  muteAll(): void {
    for (const [, bus] of this.buses) {
      bus.setMute(true);
    }
  }

  /** Unmute all */
  unmuteAll(): void {
    for (const [, bus] of this.buses) {
      bus.setMute(false);
    }
  }

  /** Reproducir sonido procedural */
  playSound(descriptor: SoundDescriptor): string | null {
    if (!this.enabled || !this.ctx) return null;

    // Check voice limit
    if (this.metrics.getMetrics().activeVoices >= this.config.maxVoices) {
      this.metrics.recordDroppedVoice();
      console.warn('[DUAT-AUDIO] Límite de voces alcanzado');
      return null;
    }

    const id = `snd_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.activeSounds.set(id, descriptor);
    this.metrics.recordVoiceStart();

    // Build graph and play
    this.graph.build(descriptor, this.ctx, this.buses.get(descriptor.bus));

    return id;
  }

  /** Detener sonido */
  stopSound(id: string): void {
    const desc = this.activeSounds.get(id);
    if (!desc) return;

    this.graph.release(id, this.ctx?.currentTime ?? 0);
    this.activeSounds.delete(id);
    this.metrics.recordVoiceStop();
  }

  /** Establecer mood actual */
  setMood(mood: MoodType): void {
    this.currentMood = mood;
    console.log('[DUAT-AUDIO] Mood:', mood);
  }

  /** Obtener mood actual */
  getMood(): MoodType {
    return this.currentMood;
  }

  /** Establecer perfil de reverb */
  setReverbProfile(profile: ReverbProfile): void {
    this.currentReverb = profile;
    console.log('[DUAT-AUDIO] Reverb profile:', profile);
  }

  /** Obtener perfil de reverb */
  getReverbProfile(): ReverbProfile {
    return this.currentReverb;
  }

  /** Tick de update — llamar cada frame */
  update(): void {
    if (!this.enabled) return;
    this.metrics.update();
    this.graph.update(this.ctx?.currentTime ?? 0);
  }

  /** Genera reporte de salud */
  getHealthReport(): AudioHealthReport {
    const m = this.metrics.getMetrics();
    return {
      certeza: m.clippingDetected ? 'INFERENCIA' : 'CERTEZA',
      gate: m.clippingDetected ? 'REVIEW' : 'APPROVE',
      R_audio: m.R_audio,
      Phi_audio: m.Phi_audio,
      voicesUsed: m.activeVoices,
      voicesMax: this.config.maxVoices,
      clippingEvents: m.clippingDetected ? 1 : 0,
      enabled: this.enabled,
      userGestureRequired: !this.userGestureReceived,
    };
  }

  /** Exporta estado como JSON */
  exportState(): AudioEngineState {
    return {
      enabled: this.enabled,
      suspended: !this.enabled,
      config: { ...this.config },
      buses: new Map(
        Array.from(this.buses.entries()).map(([k, v]) => [k, v.getConfig()])
      ),
      metrics: this.getMetrics(),
      currentMood: this.currentMood,
      reverbProfile: this.currentReverb,
    };
  }

  /** Limpieza */
  dispose(): void {
    this.enabled = false;
    for (const [, bus] of this.buses) {
      bus.dispose();
    }
    this.buses.clear();
    this.voicePool = [];
    this.ctx?.close();
    this.ctx = null;
    console.log('[DUAT-AUDIO] Engine liberado');
  }
}

/** Singleton del engine */
let engineInstance: AudioEngine | null = null;

export function getAudioEngine(config?: Partial<AudioEngineConfig>): AudioEngine {
  if (!engineInstance) {
    engineInstance = new AudioEngine(config);
  }
  return engineInstance;
}

export function resetAudioEngine(): void {
  engineInstance?.dispose();
  engineInstance = null;
}
