// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Synthesis Index — 12 sonidos base del mundo DUAT
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { NoiseGenerator } from './noise';
import { ModalResonator } from './modalResonator';
import { GranularSynth } from './granular';
import { FMSynth } from './fm';
import { AdditiveSynth } from './additive';
import { FilterUtil } from './filters';
import { Oscillator, Freq } from './oscillators';
import { Envelope } from './envelopes';
import { Reverb } from './reverb';
import { SpatialAudio } from './spatial';

export { Oscillator, Freq, Envelope, NoiseGenerator, ModalResonator };
export { GranularSynth, FMSynth, AdditiveSynth, FilterUtil, Reverb };

/** Motor de síntesis procedural completo */
export class SynthesisEngine {
  private ctx: AudioContext;
  private noise: NoiseGenerator;
  private modal: ModalResonator;
  private granular: GranularSynth;
  private fm: FMSynth;
  private additive: AdditiveSynth;
  private reverb: Reverb;
  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.noise = new NoiseGenerator(ctx);
    this.modal = new ModalResonator(ctx);
    this.granular = new GranularSynth(ctx);
    this.fm = new FMSynth(ctx);
    this.additive = new AdditiveSynth(ctx);
    this.reverb = new Reverb(ctx);
  }

  // ==========================================================
  // 1. WATER FLOW — Agua: ruido filtrado + burbujeo granular
  // ==========================================================
  waterFlow(gain = 0.4): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Base: ruido rosa filtrado low-pass
    const { source: noiseSrc, gainNode: noiseGain } = this.noise.createSource(2, 'pink', 1);
    const lowpass = this.ctx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.setValueAtTime(600, this.ctx.currentTime);
    lowpass.Q.setValueAtTime(0.5, this.ctx.currentTime);

    // Modulación lenta (flujo)
    const flowLFO = this.ctx.createOscillator();
    const flowLFOGain = this.ctx.createGain();
    flowLFO.frequency.setValueAtTime(0.3, this.ctx.currentTime);
    flowLFOGain.gain.setValueAtTime(200, this.ctx.currentTime);
    flowLFO.connect(flowLFOGain);
    flowLFOGain.connect(lowpass.frequency);
    flowLFO.start(this.ctx.currentTime);

    noiseSrc.connect(lowpass);
    lowpass.connect(noiseGain);
    noiseGain.connect(output);

    // Burbujeo granular
    const bubbleOutput = this.granular.bubbles(0.3, 0.25);
    bubbleOutput.connect(output);

    return output;
  }

  // ==========================================================
  // 2. FIRE CRACKLE — Fuego: pink noise + impulses granulares
  // ==========================================================
  fireCrackle(intensity = 0.6): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(intensity, this.ctx.currentTime);

    // Base: ruido brown/marrón (calidez)
    const { source: fireBase, gainNode: fireGain } = this.noise.createSource(2, 'brown', 0.6);
    const fireFilter = this.ctx.createBiquadFilter();
    fireFilter.type = 'bandpass';
    fireFilter.frequency.setValueAtTime(300, this.ctx.currentTime);
    fireFilter.Q.setValueAtTime(0.8, this.ctx.currentTime);

    fireBase.connect(fireFilter);
    fireFilter.connect(fireGain);
    fireGain.connect(output);

    // Crackle granular
    const crackleOutput = this.granular.crackle(intensity * 0.8, 0.4);
    crackleOutput.connect(output);

    return output;
  }

  // ==========================================================
  // 3. SMOKE BREATH — Humo: low-pass noise + envelope lento
  // ==========================================================
  smokeBreath(gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    const { source, gainNode } = this.noise.createSource(2, 'brown', 1);

    // Low-pass muy cerrado para sensación de humo
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(200, this.ctx.currentTime);
    filter.Q.setValueAtTime(0.3, this.ctx.currentTime);

    // Envelope lento tipo respiración
    const envGain = this.ctx.createGain();
    const env = new Envelope(this.ctx);
    env.applyToGain(envGain, { attack: 1.5, decay: 0.5, sustain: 0.4, release: 2.0 }, 1);

    // LFO de respiración
    const breathLFO = this.ctx.createOscillator();
    const breathLFOGain = this.ctx.createGain();
    breathLFO.frequency.setValueAtTime(0.25, this.ctx.currentTime);
    breathLFOGain.gain.setValueAtTime(0.15, this.ctx.currentTime);
    breathLFO.connect(breathLFOGain);
    breathLFOGain.connect(envGain.gain);
    breathLFO.start(this.ctx.currentTime);

    source.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(envGain);
    envGain.connect(output);

    return output;
  }

  // ==========================================================
  // 4. NEON HUM — Neón: 50/60 Hz hum + armónicos + flicker
  // ==========================================================
  neonHum(gain = 0.25): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Hum base 60Hz + armónico 120Hz
    for (const freq of [60, 120, 180]) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      g.gain.setValueAtTime(freq === 60 ? 0.6 : freq === 120 ? 0.3 : 0.15, this.ctx.currentTime);
      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
    }

    // Flicker ligado a Q-state
    const flicker = FilterUtil.flickerLFO(this.ctx, 8);
    const flickerFilter = this.ctx.createBiquadFilter();
    flickerFilter.type = 'bandpass';
    flickerFilter.frequency.setValueAtTime(60, this.ctx.currentTime);
    flickerFilter.Q.setValueAtTime(2, this.ctx.currentTime);
    flicker.lfo.connect(flickerFilter.frequency);

    output.connect(flickerFilter);

    return output;
  }

  // ==========================================================
  // 5. METAL HIT — Metal: resonador modal
  // ==========================================================
  metalHit(frequency = 800, gain = 0.5): GainNode {
    return this.modal.metalHit(frequency, gain);
  }

  // ==========================================================
  // 6. GLASS CRYSTAL — Vidrio: parciales inarmónicos + decay largo
  // ==========================================================
  glassCrystal(frequency = 1200, gain = 0.4): GainNode {
    return this.modal.glassHit(frequency, gain);
  }

  // ==========================================================
  // 7. STEAM PIPE — Vapor: filtered noise + pressure bursts
  // ==========================================================
  steamPipe(gain = 0.35): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Ruido base filtrado
    const { source, gainNode } = this.noise.createSource(2, 'pink', 1);
    const steamFilter = this.ctx.createBiquadFilter();
    steamFilter.type = 'bandpass';
    steamFilter.frequency.setValueAtTime(2000, this.ctx.currentTime);
    steamFilter.Q.setValueAtTime(2, this.ctx.currentTime);

    source.connect(steamFilter);
    steamFilter.connect(gainNode);
    gainNode.connect(output);

    // Bursts de presión
    const bursts = this.granular.steamBursts(0.3);
    bursts.connect(output);

    return output;
  }

  // ==========================================================
  // 8. ARCHIVE MACHINE — Archivo: ticks + servo + low drone
  // ==========================================================
  archiveMachine(gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Drone bajo del archivo
    const drone = this.additive.drone(55, 0.2);
    drone.connect(output);

    // Ticks mecánicos
    const tickGain = this.ctx.createGain();
    tickGain.gain.setValueAtTime(0.15, this.ctx.currentTime);

    const scheduleTick = () => {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(800 + Math.random() * 400, this.ctx.currentTime);
      g.gain.setValueAtTime(0.1, this.ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.01);
      osc.connect(g);
      g.connect(tickGain);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + 0.02);

      setTimeout(scheduleTick, 200 + Math.random() * 800);
    };
    scheduleTick();

    tickGain.connect(output);

    return output;
  }

  // ==========================================================
  // 9. GATE APPROVE — Intervalo consonante / campana verde
  // ==========================================================
  gateApprove(gain = 0.5): GainNode {
    // Quinta justa (3:2) + octava — consonancia estable
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    const root = 440;
    const fifth = root * 1.5;
    const octave = root * 2;

    for (const freq of [root, fifth, octave]) {
      const bell = this.fm.celesta(freq, 0.3);
      bell.connect(output);
    }

    return output;
  }

  // ==========================================================
  // 10. GATE REVIEW — Intervalo suspendido / tensión ámbar
  // ==========================================================
  gateReview(gain = 0.4): GainNode {
    // Segunda mayor + cuarta — tensión suspendida
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    const root = 330;
    const second = root * 1.125; // 9:8
    const fourth = root * 1.333; // 4:3

    for (const freq of [root, second, fourth]) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      const filter = this.ctx.createBiquadFilter();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(0.25, this.ctx.currentTime + 0.5);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 2, 0.5);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(1500, this.ctx.currentTime);

      osc.connect(g);
      g.connect(filter);
      filter.connect(output);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + 3);
    }

    return output;
  }

  // ==========================================================
  // 11. GATE BLOCK — Golpe grave + disonancia roja
  // ==========================================================
  gateBlock(gain = 0.6): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Golpe grave
    const hit = this.modal.stoneHit(80, 0.5);
    hit.connect(output);

    // Disonancia: tritono (augmented fourth)
    const root = 220;
    const tritone = root * 1.414; // √2 ≈ tritono

    for (const freq of [root, tritone]) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      g.gain.setValueAtTime(0.2, this.ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.5);
      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + 2);
    }

    return output;
  }

  // ==========================================================
  // 12. Q-STATE GLYPHS — Estados cuaternarios de audio
  // ==========================================================
  qStateGlyph(state: '00' | '01' | '10' | '11', gain = 0.3): GainNode | null {
    switch (state) {
      case '00': {
        // Silence / low hum — casi inaudible
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(50, this.ctx.currentTime);
        g.gain.setValueAtTime(0.02, this.ctx.currentTime);
        osc.connect(g);
        g.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime);
        return g;
      }

      case '01': {
        // Missing signal pulse — glitch corto
        const output = this.ctx.createGain();
        output.gain.setValueAtTime(gain * 0.5, this.ctx.currentTime);

        const bufferSize = Math.ceil(this.ctx.sampleRate * 0.1);
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = (Math.random() > 0.7 ? 1 : -1) * (1 - i / bufferSize);
        }
        const src = this.ctx.createBufferSource();
        src.buffer = buffer;
        src.connect(output);
        src.start(this.ctx.currentTime);
        return output;
      }

      case '10': {
        // Stable tone — tono limpio y estable
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, this.ctx.currentTime);
        g.gain.setValueAtTime(gain, this.ctx.currentTime);
        osc.connect(g);
        g.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime);
        return g;
      }

      case '11': {
        // Event burst — estallido de evento
        const output = this.ctx.createGain();
        output.gain.setValueAtTime(gain, this.ctx.currentTime);

        // Tono + ruido + decay rápido
        const osc = this.ctx.createOscillator();
        const oscGain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(880, this.ctx.currentTime);
        oscGain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        oscGain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.3);
        osc.connect(oscGain);
        oscGain.connect(output);
        osc.start(this.ctx.currentTime);
        osc.stop(this.ctx.currentTime + 0.4);

        // Burst de ruido
        const noise = this.noise.createSource(0.1, 'white', 0.3);
        noise.gainNode.gain.setValueAtTime(0.3, this.ctx.currentTime);
        noise.gainNode.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.1);
        noise.source.connect(output);

        return output;
      }

      default:
        return null;
    }
  }

  // ==========================================================
  // Utilidades
  // ==========================================================

  /** Reverb rápido */
  addReverb(input: GainNode, profile = 'catacomb' as const, wet = 0.3): GainNode {
    const { input: reverbInput, output: reverbOutput } = this.reverb.create(profile, wet);
    input.connect(reverbInput);
    const output = this.ctx.createGain();
    reverbOutput.connect(output);
    return output;
  }

  /** Pan por posición */
  pan(input: AudioNode, panValue: number): StereoPannerNode {
    const panner = this.ctx.createStereoPanner();
    panner.pan.setValueAtTime(panValue, this.ctx.currentTime);
    input.connect(panner);
    return panner;
  }

  /** Atenuación por distancia */
  attenuate(input: AudioNode, distance: number): GainNode {
    const gain = this.ctx.createGain();
    const att = SpatialAudio.distanceAttenuation(distance);
    gain.gain.setValueAtTime(att, this.ctx.currentTime);
    input.connect(gain);
    return gain;
  }

  dispose(): void {
    this.granular.dispose();
    this.modal.dispose();
    this.additive.dispose();
  }
}
