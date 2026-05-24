// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Graph — Grafo de nodos de audio
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type SoundDescriptor, type AudioNodeDescriptor } from './audioTypes';
import { AudioBus } from './audioBus';

/** Nodo ejecutable del grafo */
interface ExecutableNode {
  descriptor: AudioNodeDescriptor;
  webNode: AudioNode | null;
  gainNode: GainNode | null;
  started: boolean;
  startTime: number;
}

/** Grafo de audio que construye y ejecuta descriptores */
export class AudioGraph {
  private nodes: Map<string, ExecutableNode> = new Map();
  private sounds: Map<string, Set<string>> = new Map(); // soundId -> nodeIds

  /** Construye el grafo para un descriptor de sonido */
  build(descriptor: SoundDescriptor, ctx: AudioContext, targetBus?: AudioBus): void {
    const nodeIds: string[] = [];

    for (const nodeDesc of descriptor.nodes) {
      const node = this.createWebAudioNode(nodeDesc, ctx);
      if (node) {
        this.nodes.set(nodeDesc.id, {
          descriptor: nodeDesc,
          webNode: node.audioNode,
          gainNode: node.gainNode,
          started: false,
          startTime: ctx.currentTime,
        });
        nodeIds.push(nodeDesc.id);

        // Connect to bus if specified
        if (node.gainNode && targetBus) {
          targetBus.connectSource(node.gainNode);
        } else if (node.gainNode) {
          node.gainNode.connect(ctx.destination);
        }
      }
    }

    this.sounds.set(descriptor.name, new Set(nodeIds));
  }

  /** Crea nodo WebAudio según tipo */
  private createWebAudioNode(
    desc: AudioNodeDescriptor,
    ctx: AudioContext
  ): { audioNode: AudioNode; gainNode: GainNode } | null {
    try {
      const gainNode = ctx.createGain();
      gainNode.gain.setValueAtTime(desc.outputGain, ctx.currentTime);

      let audioNode: AudioNode;

      switch (desc.type) {
        case 'oscillator': {
          const osc = ctx.createOscillator();
          osc.type = (desc.params.waveform as OscillatorType) || 'sine';
          osc.frequency.setValueAtTime(
            Number(desc.params.frequency) || 440,
            ctx.currentTime
          );
          osc.connect(gainNode);
          if (desc.params.detune) {
            osc.detune.setValueAtTime(Number(desc.params.detune), ctx.currentTime);
          }
          osc.start(ctx.currentTime);
          audioNode = osc;
          break;
        }

        case 'noise': {
          // Create noise buffer
          const bufferSize = ctx.sampleRate * 2; // 2 seconds
          const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
          const data = buffer.getChannelData(0);
          const noiseType = (desc.params.noiseType as string) || 'white';

          for (let i = 0; i < bufferSize; i++) {
            let val = Math.random() * 2 - 1;
            if (noiseType === 'pink') {
              // Simple pink noise approximation
              val = (val + (i > 0 ? data[i - 1] : 0) * 0.5) / 1.5;
            } else if (noiseType === 'brown') {
              // Brown noise
              val = (val + (i > 0 ? data[i - 1] : 0) * 0.95) / 1.95;
            }
            data[i] = val;
          }

          const source = ctx.createBufferSource();
          source.buffer = buffer;
          source.loop = true;
          source.connect(gainNode);
          source.start(ctx.currentTime);
          audioNode = source;
          break;
        }

        case 'fm': {
          const carrier = ctx.createOscillator();
          const modulator = ctx.createOscillator();
          const modGain = ctx.createGain();

          carrier.type = (desc.params.carrierWave as OscillatorType) || 'sine';
          carrier.frequency.setValueAtTime(
            Number(desc.params.carrierFreq) || 440,
            ctx.currentTime
          );

          modulator.type = (desc.params.modWave as OscillatorType) || 'sine';
          modulator.frequency.setValueAtTime(
            Number(desc.params.modFreq) || 110,
            ctx.currentTime
          );

          const modIndex = Number(desc.params.modIndex) || 100;
          modGain.gain.setValueAtTime(modIndex, ctx.currentTime);

          modulator.connect(modGain);
          modGain.connect(carrier.frequency);
          carrier.connect(gainNode);

          modulator.start(ctx.currentTime);
          carrier.start(ctx.currentTime);
          audioNode = carrier;
          break;
        }

        case 'additive': {
          // Create a composite node with multiple partials
          const fundamental = Number(desc.params.fundamental) || 220;
          const partials = Number(desc.params.partials) || 4;
          const detune = Number(desc.params.detune) || 0;

          const merger = ctx.createChannelMerger(1);
          for (let i = 1; i <= partials; i++) {
            const osc = ctx.createOscillator();
            const partialGain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(fundamental * i, ctx.currentTime);
            if (detune !== 0) {
              osc.detune.setValueAtTime(detune * i, ctx.currentTime);
            }
            partialGain.gain.setValueAtTime(1 / i, ctx.currentTime);
            osc.connect(partialGain);
            partialGain.connect(merger);
            osc.start(ctx.currentTime);
          }
          merger.connect(gainNode);
          audioNode = merger;
          break;
        }

        case 'reverb': {
          // Simple convolution reverb using delay nodes
          const inputGain = ctx.createGain();
          const delay = ctx.createDelay();
          const feedback = ctx.createGain();
          const wetGain = ctx.createGain();

          const duration = Number(desc.params.duration) || 1.0;
          const decay = Number(desc.params.decay) || 0.5;

          delay.delayTime.setValueAtTime(duration, ctx.currentTime);
          feedback.gain.setValueAtTime(decay, ctx.currentTime);
          wetGain.gain.setValueAtTime(Number(desc.params.wet) || 0.3, ctx.currentTime);

          // Pass-through
          inputGain.connect(gainNode);
          // Reverb path
          inputGain.connect(delay);
          delay.connect(feedback);
          feedback.connect(delay);
          delay.connect(wetGain);
          wetGain.connect(gainNode);

          audioNode = inputGain;
          break;
        }

        default: {
          // Default fallback: oscillator
          const osc = ctx.createOscillator();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(440, ctx.currentTime);
          osc.connect(gainNode);
          osc.start(ctx.currentTime);
          audioNode = osc;
        }
      }

      return { audioNode, gainNode };
    } catch (err) {
      console.warn('[DUAT-AUDIO] Error creando nodo:', desc.type, err);
      return null;
    }
  }

  /** Libera un sonido */
  release(soundId: string, currentTime: number): void {
    const nodeIds = this.sounds.get(soundId);
    if (!nodeIds) return;

    for (const nodeId of nodeIds) {
      const node = this.nodes.get(nodeId);
      if (node?.gainNode) {
        // Fade out
        node.gainNode.gain.setTargetAtTime(0, currentTime, 0.05);
        // Stop after fade
        setTimeout(() => {
          if (node.webNode && 'stop' in node.webNode) {
            (node.webNode as OscillatorNode).stop();
          }
        }, 100);
      }
      this.nodes.delete(nodeId);
    }
    this.sounds.delete(soundId);
  }

  /** Update tick */
  update(currentTime: number): void {
    // Clean up finished nodes
    for (const [id, node] of this.nodes) {
      if (node.started && currentTime > node.startTime + 10) {
        // Auto-cleanup old nodes
        this.nodes.delete(id);
      }
    }
  }

  /** Limpia todo */
  clear(): void {
    for (const [, node] of this.nodes) {
      if (node.webNode && 'stop' in node.webNode) {
        try {
          (node.webNode as OscillatorNode).stop();
        } catch {
          // Ignore
        }
      }
      node.gainNode?.disconnect();
    }
    this.nodes.clear();
    this.sounds.clear();
  }

  /** Número de nodos activos */
  getActiveNodeCount(): number {
    return this.nodes.size;
  }
}
