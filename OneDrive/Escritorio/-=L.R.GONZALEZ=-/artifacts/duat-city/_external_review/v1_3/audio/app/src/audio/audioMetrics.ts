// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Metrics — Métricas R_audio, Phi_audio y salud
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type AudioMetrics } from './audioTypes';

/** Colector de métricas del motor de audio */
export class AudioMetricsCollector {
  private metrics: AudioMetrics;
  private voiceCount = 0;
  private totalVoicesStarted = 0;
  private droppedVoiceCount = 0;
  private mockMode = false;
  private history: number[] = [];
  private maxHistory = 60; // 1 segundo a 60fps

  constructor() {
    this.metrics = this.getDefaultMetrics();
  }

  private getDefaultMetrics(): AudioMetrics {
    return {
      activeVoices: 0,
      cpuEstimate: 0,
      droppedVoices: 0,
      masterGain: 0.8,
      R_audio: 0.05,
      Phi_audio: 0.95,
      clippingDetected: false,
      silenceDetected: true,
      timestamp: Date.now(),
    };
  }

  /** Modo mock para entornos sin audio */
  setMockMode(enabled: boolean): void {
    this.mockMode = enabled;
    if (enabled) {
      this.metrics.activeVoices = 0;
      this.metrics.cpuEstimate = 0;
      this.metrics.silenceDetected = true;
    }
  }

  /** Registra inicio de voz */
  recordVoiceStart(): void {
    this.voiceCount++;
    this.totalVoicesStarted++;
    this.metrics.activeVoices = this.voiceCount;
    this.metrics.silenceDetected = false;
    this.recalculateMetrics();
  }

  /** Registra fin de voz */
  recordVoiceStop(): void {
    this.voiceCount = Math.max(0, this.voiceCount - 1);
    this.metrics.activeVoices = this.voiceCount;
    if (this.voiceCount === 0) {
      this.metrics.silenceDetected = true;
    }
    this.recalculateMetrics();
  }

  /** Registra voz dropeada */
  recordDroppedVoice(): void {
    this.droppedVoiceCount++;
    this.metrics.droppedVoices = this.droppedVoiceCount;
    this.metrics.R_audio = Math.min(1, this.metrics.R_audio + 0.1);
    this.recalculateMetrics();
  }

  /** Detecta clipping */
  detectClipping(value: number): void {
    if (value > 1.0 || value < -1.0) {
      this.metrics.clippingDetected = true;
      this.metrics.R_audio = Math.min(1, this.metrics.R_audio + 0.05);
    }
  }

  /** Update tick — recalcula métricas */
  update(): void {
    this.recalculateMetrics();
    this.history.push(this.voiceCount);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }
    this.metrics.timestamp = Date.now();
  }

  /** Recalcula R_audio y Phi_audio */
  private recalculateMetrics(): void {
    if (this.mockMode) {
      this.metrics.R_audio = 0.02;
      this.metrics.Phi_audio = 0.98;
      return;
    }

    // R_audio aumenta con: voces dropeadas, clipping, muchas voces
    const voiceLoad = this.voiceCount / 32; // normalizado a max 32
    const dropFactor = Math.min(1, this.droppedVoiceCount / 10);
    const clipFactor = this.metrics.clippingDetected ? 0.2 : 0;

    this.metrics.R_audio = Math.min(1, voiceLoad * 0.3 + dropFactor * 0.5 + clipFactor);

    // Phi_audio = eficiencia = 1 - R (simplificado)
    // Ajustado por: estabilidad de señal, no clipping, voces activas óptimas
    const optimalVoices = this.voiceCount > 0 && this.voiceCount < 24;
    const stabilityBonus = optimalVoices ? 0.1 : 0;
    this.metrics.Phi_audio = Math.min(1, Math.max(0, 1 - this.metrics.R_audio + stabilityBonus));

    // CPU estimate basado en voces activas
    this.metrics.cpuEstimate = Math.min(1, voiceLoad * 0.8);
  }

  /** Obtiene métricas actuales */
  getMetrics(): AudioMetrics {
    return { ...this.metrics };
  }

  /** Resetea métricas */
  reset(): void {
    this.voiceCount = 0;
    this.totalVoicesStarted = 0;
    this.droppedVoiceCount = 0;
    this.history = [];
    this.metrics = this.getDefaultMetrics();
  }
}
