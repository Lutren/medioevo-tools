// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Spatial — Audio espacial 2D/2.5D
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type ReverbProfile, type SpatialConfig } from '../audioTypes';
import { Reverb } from './reverb';

/** Audio espacial para 2D/2.5D */
export class SpatialAudio {
  private ctx: AudioContext;
  private reverb: Reverb;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.reverb = new Reverb(ctx);
  }

  /** Atenuación por distancia */
  static distanceAttenuation(distance: number, maxDist = 1): number {
    const d = Math.max(0, Math.min(1, distance / maxDist));
    // Curva inversa cuadrática suave
    return 1 / (1 + 3 * d * d);
  }

  /** Pan estéreo por posición de pantalla (-1 a 1) */
  static panByPosition(x: number, screenWidth: number): number {
    return (x / screenWidth) * 2 - 1;
  }

  /** Posicionaliza un nodo de audio */
  positionize(
    sourceNode: AudioNode,
    x: number,
    y: number,
    screenW: number,
    screenH: number,
    profile: ReverbProfile = 'catacomb'
  ): GainNode {
    const pan = SpatialAudio.panByPosition(x, screenW);
    const dist = Math.sqrt(
      Math.pow((x / screenW) - 0.5, 2) + Math.pow((y / screenH) - 0.5, 2)
    ) * 2;
    const attenuation = SpatialAudio.distanceAttenuation(dist);

    // Stereo panner
    const panner = this.ctx.createStereoPanner();
    panner.pan.setValueAtTime(pan, this.ctx.currentTime);

    // Gain por distancia
    const distGain = this.ctx.createGain();
    distGain.gain.setValueAtTime(attenuation, this.ctx.currentTime);

    // Reverb por ubicación
    const { input: reverbInput, output: reverbOutput } = this.reverb.create(profile, 0.2);

    sourceNode.connect(panner);
    panner.connect(distGain);
    distGain.connect(reverbInput);
    reverbOutput.connect(this.ctx.destination);

    return distGain;
  }

  /** Crea config espacial */
  createConfig(
    pan: number,
    distance: number,
    occlusion = 0,
    profile: ReverbProfile = 'catacomb'
  ): SpatialConfig {
    return { pan, distance, occlusion, reverbProfile: profile };
  }

  /** Aplica oclusión por pared/material */
  applyOcclusion(gainNode: GainNode, occlusion: number): void {
    const attenuation = 1 - Math.max(0, Math.min(1, occlusion));

    gainNode.gain.setValueAtTime(
      gainNode.gain.value * attenuation,
      this.ctx.currentTime
    );

    // Filtro por oclusión
    const freqCutoff = 2000 + (1 - occlusion) * 6000;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(freqCutoff, this.ctx.currentTime);
    gainNode.connect(filter);
  }

  /** Filtro indoor/outdoor */
  indoorFilter(): BiquadFilterNode {
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(3000, this.ctx.currentTime);
    filter.Q.setValueAtTime(0.5, this.ctx.currentTime);
    return filter;
  }

  outdoorFilter(): BiquadFilterNode {
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.setValueAtTime(80, this.ctx.currentTime);
    filter.Q.setValueAtTime(0.5, this.ctx.currentTime);
    return filter;
  }

  /** Perfil acústico por material */
  materialAcoustics(type: 'water' | 'metal' | 'stone' | 'wood'): BiquadFilterNode {
    const filter = this.ctx.createBiquadFilter();
    switch (type) {
      case 'water':
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(800, this.ctx.currentTime);
        break;
      case 'metal':
        filter.type = 'peaking';
        filter.frequency.setValueAtTime(4000, this.ctx.currentTime);
        filter.gain.setValueAtTime(6, this.ctx.currentTime);
        break;
      case 'stone':
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1500, this.ctx.currentTime);
        break;
      case 'wood':
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(2500, this.ctx.currentTime);
        break;
    }
    return filter;
  }
}
