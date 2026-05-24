// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Event Audio — Audio para eventos del mundo
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type WorldAudioEvent, type MaterialType } from './audioTypes';
import { SynthesisEngine } from './synthesis';

/** Procesa eventos del mundo a audio */
export class EventAudio {
  private ctx: AudioContext;
  private synth: SynthesisEngine;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.synth = new SynthesisEngine(ctx);
  }

  /** Procesa evento */
  process(event: WorldAudioEvent): GainNode | null {
    switch (event.type) {
      case 'material':
        return this.processMaterialAudio(event.material);
      case 'gate':
        return event.gate ? this.processGate(event.gate) : null;
      default:
        return null;
    }
  }

  private processMaterialAudio(material?: MaterialType): GainNode | null {
    if (!material) return null;
    // Map material to sound via synthesis engine
    const soundMap: Record<string, () => GainNode> = {
      water: () => this.synth.waterFlow(0.3),
      fire: () => this.synth.fireCrackle(0.3),
      metal: () => this.synth.metalHit(800, 0.3),
      glass: () => this.synth.glassCrystal(1200, 0.3),
    };
    const fn = soundMap[material];
    return fn ? fn() : null;
  }

  private processGate(gateName: string): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(0.4, this.ctx.currentTime);

    switch (gateName) {
      case 'APPROVE': {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, this.ctx.currentTime);
        g.gain.setValueAtTime(0.3, this.ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1);
        osc.connect(g);
        g.connect(output);
        osc.start(this.ctx.currentTime);
        osc.stop(this.ctx.currentTime + 1.2);
        break;
      }
      case 'REVIEW': {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(392, this.ctx.currentTime);
        g.gain.setValueAtTime(0.2, this.ctx.currentTime);
        g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 1.5, 0.3);
        osc.connect(g);
        g.connect(output);
        osc.start(this.ctx.currentTime);
        osc.stop(this.ctx.currentTime + 2);
        break;
      }
      case 'BLOCK': {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(146.83, this.ctx.currentTime);
        g.gain.setValueAtTime(0.3, this.ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.8);
        osc.connect(g);
        g.connect(output);
        osc.start(this.ctx.currentTime);
        osc.stop(this.ctx.currentTime + 1);
        break;
      }
    }

    return output;
  }

  dispose(): void {
    this.synth.dispose();
  }
}

// No module extensions - kept clean for TypeScript
