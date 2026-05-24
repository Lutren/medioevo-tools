// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Clock — Reloj de audio con Quaternary Timing
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Reloj de audio que mantiene tempo y timing */
export class AudioClock {
  private startTime = 0;
  private isRunning = false;
  private bpm = 120;
  private qState: '00' | '01' | '10' | '11' = '00';

  constructor(_sampleRate = 44100) {
    // sampleRate stored for future use
  }

  /** Inicia el reloj */
  start(ctx: AudioContext): void {
    this.startTime = ctx.currentTime;
    this.isRunning = true;
  }

  /** Detiene el reloj */
  stop(): void {
    this.isRunning = false;
  }

  /** Obtiene tiempo actual */
  getCurrentTime(ctx?: AudioContext): number {
    if (ctx) return ctx.currentTime - this.startTime;
    return (Date.now() / 1000) - this.startTime;
  }

  /** Establece BPM */
  setBPM(bpm: number): void {
    this.bpm = Math.max(30, Math.min(300, bpm));
  }

  /** Obtiene BPM */
  getBPM(): number {
    return this.bpm;
  }

  /** Calcula tempo basado en R y Phi_eff */
  calculateTempo(R: number, PhiEff: number): number {
    // Tempo oscila alrededor de 120 BPM
    // R alto = inestable = variación mayor
    // Phi_eff alto = estable = acercarse a 120
    const stability = PhiEff / (1 + R);
    const variation = (Math.sin(this.getCurrentTime() * stability) * R * 30);
    return 120 + variation;
  }

  /** Beat actual */
  getCurrentBeat(ctx?: AudioContext): number {
    const elapsed = this.getCurrentTime(ctx);
    return (elapsed * this.bpm) / 60;
  }

  /** Establece Q-state */
  setQState(state: '00' | '01' | '10' | '11'): void {
    this.qState = state;
  }

  /** Obtiene Q-state */
  getQState(): string {
    return this.qState;
  }

  /** Cada cuántos segundos ocurre un beat */
  getBeatDuration(): number {
    return 60 / this.bpm;
  }

  /** Siguiente beat time */
  getNextBeatTime(ctx: AudioContext): number {
    const beatDur = this.getBeatDuration();
    const elapsed = ctx.currentTime - this.startTime;
    const nextBeat = Math.ceil(elapsed / beatDur) * beatDur;
    return this.startTime + nextBeat;
  }

  /** Está corriendo? */
  isClockRunning(): boolean {
    return this.isRunning;
  }
}
