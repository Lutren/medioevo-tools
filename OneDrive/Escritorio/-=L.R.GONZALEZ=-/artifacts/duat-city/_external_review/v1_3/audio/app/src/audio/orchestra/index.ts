// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Orchestra Index — Motor orquestal completo
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type MoodType } from '../audioTypes';
import { SyntheticStrings } from './syntheticStrings';
import { SyntheticBrass } from './syntheticBrass';
import { SyntheticChoir } from './syntheticChoir';
import { SyntheticPercussion } from './syntheticPercussion';
import { MotifGenerator } from './motifGenerator';
import { HarmonyEngine } from './harmonyEngine';
import { TensionEngine } from './tensionEngine';

export {
  SyntheticStrings,
  SyntheticBrass,
  SyntheticChoir,
  SyntheticPercussion,
  MotifGenerator,
  HarmonyEngine,
  TensionEngine,
};

/** Motor orquestal completo */
export class OrchestraEngine {
  private ctx: AudioContext;
  strings: SyntheticStrings;
  brass: SyntheticBrass;
  choir: SyntheticChoir;
  percussion: SyntheticPercussion;
  motif: MotifGenerator;
  harmony: HarmonyEngine;
  tension: TensionEngine;

  constructor(ctx: AudioContext, seed = Date.now()) {
    this.ctx = ctx;
    this.strings = new SyntheticStrings(ctx);
    this.brass = new SyntheticBrass(ctx);
    this.choir = new SyntheticChoir(ctx);
    this.percussion = new SyntheticPercussion(ctx);
    this.motif = new MotifGenerator(seed);
    this.harmony = new HarmonyEngine(seed);
    this.tension = new TensionEngine();
  }

  // ==========================================================
  // Mood-based orchestration
  // ==========================================================

  /** Toca mood completo */
  playMood(mood: MoodType, gain = 0.4): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    switch (mood) {
      case 'archive':
        this.playArchive(output);
        break;
      case 'forge':
        this.playForge(output);
        break;
      case 'garden':
        this.playGarden(output);
        break;
      case 'market':
        this.playMarket(output);
        break;
      case 'ruin':
        this.playRuin(output);
        break;
      case 'gate_review':
        this.playGateReview(output);
        break;
      case 'gate_block':
        this.playGateBlock(output);
        break;
      default:
        this.playSilence(output);
    }

    return output;
  }

  /** Archive = coro + cristal + cuerdas graves */
  private playArchive(output: GainNode): void {
    const choir = this.choir.pad(220, 'o', 0.3);
    const strings = this.strings.lowDrone(110, 0.2);
    const bell = this.percussion.bell(880, 0.15);

    choir.connect(output);
    strings.connect(output);
    bell.connect(output);
  }

  /** Forge = bronces + percusión grave + fuego */
  private playForge(output: GainNode): void {
    const brass = this.brass.swell(200, 0.3);
    const perc = this.percussion.lowPercussion(0.25);
    const bell = this.percussion.bowedMetal(150, 0.15);

    brass.connect(output);
    perc.connect(output);
    bell.connect(output);
  }

  /** Garden = cuerdas brillantes + agua + campanas */
  private playGarden(output: GainNode): void {
    const shimmer = this.strings.highShimmer(660, 0.2);
    const bell = this.percussion.bell(1320, 0.15);

    shimmer.connect(output);
    bell.connect(output);
  }

  /** Market = pulsos + chatter granular + neón */
  private playMarket(output: GainNode): void {
    const hit = this.percussion.staccatoHit(400, 0.2);
    const bell = this.percussion.bell(660, 0.15);

    hit.connect(output);
    bell.connect(output);
  }

  /** Ruin = drone + campana reversa + señal perdida */
  private playRuin(output: GainNode): void {
    const drone = this.choir.drone(146, 0.3);
    const bell = this.percussion.bell(440, 0.1);

    drone.connect(output);
    bell.connect(output);
  }

  /** Gate Review = armonía suspendida */
  private playGateReview(output: GainNode): void {
    const strings = this.strings.lowDrone(247, 0.3);
    const choir = this.choir.breath(0.15);

    strings.connect(output);
    choir.connect(output);
  }

  /** Gate Block = disonancia */
  private playGateBlock(output: GainNode): void {
    const hit = this.percussion.lowPercussion(0.4);
    const brass = this.brass.staccatoHit(150, 0.3);

    hit.connect(output);
    brass.connect(output);
  }

  /** Silence */
  private playSilence(_output: GainNode): void {
    // Intencionalmente vacío
  }

  /** Update de tensión */
  updateTension(R: number, PhiEff: number, dt: number): void {
    const tensionR = this.tension.tensionFromR(R);
    const tensionPhi = this.tension.tensionFromPhiEff(PhiEff);
    this.tension.setTargetTension((tensionR + tensionPhi) / 2);
    this.tension.update(dt);
  }
}
