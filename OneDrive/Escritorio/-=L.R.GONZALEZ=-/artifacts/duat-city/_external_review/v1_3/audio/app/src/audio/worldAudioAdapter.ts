// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// World Audio Adapter — Audio desde estado del mundo
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import {
  type WorldAudioEvent,
  type MaterialType,
  type MoodType,
  type QState,
  type ActionGate,
} from './audioTypes';
import { SynthesisEngine } from './synthesis';

/** Adaptador de audio del mundo */
export class WorldAudioAdapter {
  private ctx: AudioContext;
  private synth: SynthesisEngine;
  private materialMap: Map<string, () => GainNode> = new Map();

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.synth = new SynthesisEngine(ctx);
    this.initMaterialMap();
  }

  private initMaterialMap(): void {
    this.materialMap.set('water', () => this.synth.waterFlow());
    this.materialMap.set('fire', () => this.synth.fireCrackle());
    this.materialMap.set('smoke', () => this.synth.smokeBreath());
    this.materialMap.set('neon', () => this.synth.neonHum());
    this.materialMap.set('metal', () => this.synth.metalHit());
    this.materialMap.set('glass', () => this.synth.glassCrystal());
    this.materialMap.set('crystal', () => this.synth.glassCrystal(1500));
    this.materialMap.set('steam', () => this.synth.steamPipe());
    this.materialMap.set('stone', () => this.synth.metalHit(400, 0.3));
    this.materialMap.set('wet_stone', () => this.synth.waterFlow(0.2));
    this.materialMap.set('wood', () => this.synth.metalHit(600, 0.25));
    this.materialMap.set('sand', () => this.synth.smokeBreath(0.15));
  }

  /** Procesa evento del mundo y genera audio */
  processEvent(event: WorldAudioEvent): GainNode | null {
    switch (event.type) {
      case 'material':
        return this.processMaterial(event.material, event.intensity);
      case 'light':
        return this.processLight(event.intensity, event.mood);
      case 'npc':
        return this.processNPC(event);
      case 'weather':
        return this.processWeather(event.mood, event.intensity);
      case 'gate':
        return this.processGate(event.gate);
      case 'quest':
        return this.processQuest(event.mood);
      case 'osit':
        return this.processOSIT(event.qState, event.intensity);
      default:
        return null;
    }
  }

  /** Material -> sonido */
  processMaterial(material?: MaterialType, intensity = 0.5): GainNode | null {
    if (!material) return null;
    const generator = this.materialMap.get(material);
    if (!generator) return null;

    const node = generator();
    node.gain.setValueAtTime(intensity, this.ctx.currentTime);
    return node;
  }

  /** Luz -> sonido */
  processLight(intensity: number, mood?: MoodType): GainNode | null {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(intensity * 0.3, this.ctx.currentTime);

    if (intensity > 0.8) {
      // Alta emisividad -> hum/shimmer
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(200 + intensity * 400, this.ctx.currentTime);
      g.gain.setValueAtTime(intensity * 0.2, this.ctx.currentTime);
      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
    } else if (mood === 'ruin') {
      // Luz anómala -> cluster desafinado
      for (let i = 0; i < 4; i++) {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300 + i * 50 + Math.random() * 30, this.ctx.currentTime);
        osc.detune.setValueAtTime((Math.random() - 0.5) * 50, this.ctx.currentTime);
        g.gain.setValueAtTime(0.05, this.ctx.currentTime);
        osc.connect(g);
        g.connect(output);
        osc.start(this.ctx.currentTime);
      }
    }

    return output;
  }

  /** NPC -> sonido */
  processNPC(event: WorldAudioEvent): GainNode | null {
    if (!event.npcState) return null;

    const output = this.ctx.createGain();
    const { emotionalMotif, proximity } = event.npcState;

    // Gain por proximidad
    output.gain.setValueAtTime((1 - proximity) * 0.3, this.ctx.currentTime);

    // Breath/cloth
    if (proximity < 0.3) {
      const breath = this.synth.smokeBreath(0.1);
      breath.connect(output);
    }

    // Motif emocional
    if (emotionalMotif) {
      const motifGain = this.ctx.createGain();
      motifGain.gain.setValueAtTime(0.15, this.ctx.currentTime);

      // Tono según emoción
      const emotionFreqs: Record<string, number> = {
        calm: 330, alert: 440, agitated: 220, fearful: 185,
        curious: 370, hostile: 146, mystical: 280,
      };
      const freq = emotionFreqs[emotionalMotif] || 330;

      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      g.gain.setValueAtTime(0.1, this.ctx.currentTime);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 2, 0.5);
      osc.connect(g);
      g.connect(motifGain);
      motifGain.connect(output);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + 3);
    }

    return output;
  }

  /** Clima -> sonido */
  processWeather(mood?: MoodType, intensity = 0.5): GainNode | null {
    if (!mood) return null;

    switch (mood) {
      case 'garden':
        return this.synth.waterFlow(intensity * 0.5);
      case 'forge':
        return this.synth.fireCrackle(intensity * 0.4);
      case 'ruin':
        return this.synth.smokeBreath(intensity * 0.3);
      default:
        return null;
    }
  }

  /** Gate -> sonido */
  processGate(gate?: ActionGate): GainNode | null {
    switch (gate) {
      case 'APPROVE':
        return this.synth.gateApprove();
      case 'REVIEW':
        return this.synth.gateReview();
      case 'BLOCK':
        return this.synth.gateBlock();
      default:
        return null;
    }
  }

  /** Quest -> sonido */
  processQuest(mood?: MoodType): GainNode | null {
    if (!mood) return null;
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(0.2, this.ctx.currentTime);

    // Motif según mood de quest
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    osc.type = 'sine';

    const questFreqs: Record<string, number> = {
      archive: 264, forge: 196, garden: 330, market: 392,
      ruin: 146, gate_review: 247, gate_block: 110, silence: 440,
    };

    osc.frequency.setValueAtTime(questFreqs[mood] || 330, this.ctx.currentTime);
    g.gain.setValueAtTime(0, this.ctx.currentTime);
    g.gain.linearRampToValueAtTime(0.15, this.ctx.currentTime + 0.5);
    g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 3, 0.8);

    osc.connect(g);
    g.connect(output);
    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 4);

    return output;
  }

  /** OSIT state -> sonido */
  processOSIT(qState?: QState, intensity = 0.5): GainNode | null {
    if (qState) {
      return this.synth.qStateGlyph(qState, intensity);
    }
    return null;
  }

  dispose(): void {
    this.synth.dispose();
  }
}
