// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Spatial Audio — Audio espacial 2D/2.5D completo
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type ReverbProfile } from './audioTypes';
import { Reverb } from './synthesis/reverb';

/** Audio espacial completo */
export class SpatialAudioManager {
  private ctx: AudioContext;
  private reverb: Reverb;
  private currentProfile: ReverbProfile = 'catacomb';

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.reverb = new Reverb(ctx);
  }

  /** Atenuación por distancia */
  static distanceAttenuation(distance: number, maxDist = 1): number {
    const d = Math.max(0, Math.min(1, distance / maxDist));
    return 1 / (1 + 3 * d * d);
  }

  /** Pan estéreo */
  static panByPosition(x: number, screenWidth: number): number {
    return (x / screenWidth) * 2 - 1;
  }

  /** Posicionaliza audio */
  positionize(
    sourceNode: AudioNode,
    x: number,
    y: number,
    screenW: number,
    screenH: number,
    profile?: ReverbProfile
  ): GainNode {
    const pan = SpatialAudioManager.panByPosition(x, screenW);
    const dist = Math.sqrt(
      Math.pow((x / screenW) - 0.5, 2) + Math.pow((y / screenH) - 0.5, 2)
    ) * 2;
    const attenuation = SpatialAudioManager.distanceAttenuation(dist);

    const panner = this.ctx.createStereoPanner();
    panner.pan.setValueAtTime(pan, this.ctx.currentTime);

    const distGain = this.ctx.createGain();
    distGain.gain.setValueAtTime(attenuation, this.ctx.currentTime);

    const revProfile = profile || this.currentProfile;
    const { input: reverbInput, output: reverbOutput } = this.reverb.create(revProfile, 0.2);

    sourceNode.connect(panner);
    panner.connect(distGain);
    distGain.connect(reverbInput);
    reverbOutput.connect(this.ctx.destination);

    return distGain;
  }

  /** Oclusión por pared */
  applyOcclusion(gainNode: GainNode, occlusion: number): void {
    const attenuation = 1 - Math.max(0, Math.min(1, occlusion));
    const freqCutoff = 500 + (1 - occlusion) * 3000;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(freqCutoff, this.ctx.currentTime);

    gainNode.gain.setValueAtTime(
      gainNode.gain.value * attenuation,
      this.ctx.currentTime
    );
  }

  /** Indoor filter */
  indoorFilter(): BiquadFilterNode {
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(3000, this.ctx.currentTime);
    filter.Q.setValueAtTime(0.5, this.ctx.currentTime);
    return filter;
  }

  /** Outdoor filter */
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

  setProfile(profile: ReverbProfile): void {
    this.currentProfile = profile;
  }
}
