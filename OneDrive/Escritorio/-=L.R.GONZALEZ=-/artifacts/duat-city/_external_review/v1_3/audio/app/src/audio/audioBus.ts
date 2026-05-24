// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Bus — Canal de audio categorizado
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type BusConfig, type AudioBusName } from './audioTypes';

/** Bus de audio con su propio gain, compressor y EQ */
export class AudioBus {
  private config: BusConfig;
  private gainNode: GainNode;
  private compressor: DynamicsCompressorNode | null = null;
  private eqNode: BiquadFilterNode | null = null;
  private sources: GainNode[] = [];

  constructor(config: BusConfig, ctx: AudioContext) {
    this.config = { ...config };
    this.gainNode = ctx.createGain();
    this.gainNode.gain.setValueAtTime(config.muted ? 0 : config.gain, ctx.currentTime);

    if (config.compressor) {
      this.compressor = ctx.createDynamicsCompressor();
      this.compressor.threshold.setValueAtTime(-18, ctx.currentTime);
      this.compressor.knee.setValueAtTime(9, ctx.currentTime);
      this.compressor.ratio.setValueAtTime(4, ctx.currentTime);
      this.compressor.attack.setValueAtTime(0.01, ctx.currentTime);
      this.compressor.release.setValueAtTime(0.1, ctx.currentTime);
      this.gainNode.connect(this.compressor);
    }

    if (config.eq) {
      this.eqNode = ctx.createBiquadFilter();
      this.eqNode.type = 'peaking';
      this.eqNode.frequency.setValueAtTime(1000, ctx.currentTime);
      this.eqNode.Q.setValueAtTime(1, ctx.currentTime);
      this.eqNode.gain.setValueAtTime(0, ctx.currentTime);
    }
  }

  /** Conecta una fuente a este bus */
  connectSource(source: GainNode): void {
    if (!this.sources.includes(source)) {
      this.sources.push(source);
    }
    if (this.compressor) {
      source.connect(this.gainNode);
    }
  }

  /** Conecta el bus al destino */
  connect(destination: AudioNode): void {
    const output = this.compressor ?? this.gainNode;
    output.connect(destination);
  }

  /** Establece gain */
  setGain(value: number): void {
    this.config.gain = Math.max(0, Math.min(2, value));
    this.gainNode.gain.setTargetAtTime(
      this.config.muted ? 0 : this.config.gain,
      this.gainNode.context.currentTime,
      0.01
    );
  }

  /** Obtiene gain */
  getGain(): number {
    return this.config.gain;
  }

  /** Mute/unmute */
  setMute(muted: boolean): void {
    this.config.muted = muted;
    this.gainNode.gain.setTargetAtTime(
      muted ? 0 : this.config.gain,
      this.gainNode.context.currentTime,
      0.01
    );
  }

  /** Obtiene config */
  getConfig(): BusConfig {
    return { ...this.config };
  }

  /** Nombre del bus */
  getName(): AudioBusName {
    return this.config.name;
  }

  /** Libera recursos */
  dispose(): void {
    for (const src of this.sources) {
      src.disconnect();
    }
    this.sources = [];
    this.gainNode.disconnect();
    this.compressor?.disconnect();
    this.eqNode?.disconnect();
  }
}
