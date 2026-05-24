/**
 * OSIT — Observación con Estado
 * 
 * Observation = f(State, Signal, Channel, Memory, Noise, Goal, Gate)
 * 
 * El observador no observa desde cero. Observa desde estado.
 */

import { OSITState, QState, SystemMetrics } from '../types';

/**
 * Observador genérico: puede ser celda, NPC, sensor, runtime
 */
export class OSITObserver {
  private state: OSITState;
  private history: OSITState[] = [];
  private maxHistory = 8;

  constructor(initialGoal: string = 'survive') {
    this.state = {
      state: '10', // estable por defecto
      memory: new Float32Array(4),
      calibration: 0.5,
      noise: 0.1,
      goal: initialGoal,
      gate: 'APPROVE',
      lastUpdate: 0
    };
  }

  /**
   * Observar: recibir señal y actualizar estado
   */
  observe(
    signal: number,
    channel: string,
    noise: number,
    frame: number
  ): OSITState {
    // Guardar historia
    this.history.push({ ...this.state, memory: new Float32Array(this.state.memory) });
    if (this.history.length > this.maxHistory) this.history.shift();

    // Actualizar memoria con señal filtrada
    const filteredSignal = signal * (1 - this.state.noise) * this.state.calibration;
    this.state.memory[0] = this.state.memory[1]; // shift
    this.state.memory[1] = this.state.memory[2];
    this.state.memory[2] = this.state.memory[3];
    this.state.memory[3] = filteredSignal;

    // Determinar Q-state desde memoria
    const trend = this.detectTrend();
    const volatility = this.detectVolatility();

    let newQ: QState = '10';
    if (trend === 'down' && volatility === 'low') newQ = '00';
    else if (trend === 'down' && volatility === 'high') newQ = '01';
    else if (trend === 'up' && volatility === 'low') newQ = '10';
    else if (trend === 'up' && volatility === 'high') newQ = '11';

    this.state.state = newQ;
    this.state.noise = noise;
    this.state.lastUpdate = frame;

    // Gate lógico
    if (filteredSignal < -0.5) this.state.gate = 'BLOCK';
    else if (filteredSignal < 0) this.state.gate = 'REVIEW';
    else this.state.gate = 'APPROVE';

    return this.state;
  }

  private detectTrend(): 'up' | 'down' | 'flat' {
    const m = this.state.memory;
    const diff = m[3] - m[0];
    if (diff > 0.01) return 'up';
    if (diff < -0.01) return 'down';
    return 'flat';
  }

  private detectVolatility(): 'low' | 'high' {
    const m = this.state.memory;
    let sum = 0;
    for (let i = 1; i < m.length; i++) {
      sum += Math.abs(m[i] - m[i-1]);
    }
    return sum > 0.1 ? 'high' : 'low';
  }

  getState(): OSITState { return this.state; }
  getHistory(): OSITState[] { return this.history; }
}

/**
 * Métricas del sistema observador
 */
export function computeSystemMetrics(
  observers: OSITObserver[],
  jammingThreshold: number
): SystemMetrics {
  let totalR = 0;
  let totalPhi = 0;
  let jammedCount = 0;

  for (const obs of observers) {
    const s = obs.getState();
    // R: proporción de observers en gate BLOCK/REVIEW
    if (s.gate === 'BLOCK' || s.gate === 'REVIEW') totalR += 1;
    // Phi_eff: correlación entre memoria y estado actual
    const mem = s.memory;
    const coherence = mem[3] / (Math.abs(mem[0]) + 0.001);
    totalPhi += Math.min(1, Math.max(0, coherence));
    if (s.noise > jammingThreshold) jammedCount++;
  }

  const n = observers.length || 1;
  const R = totalR / n;
  const Phi_eff = totalPhi / n;
  const ratio = jammedCount / n;

  let regime: SystemMetrics['regime'] = 'OPTIMO';
  if (ratio > 0.5) regime = 'JAMMED';
  else if (R > 0.4) regime = 'SATURADO';
  else if (Phi_eff < 0.3) regime = 'CRITICO';

  return { R, Phi_eff, J_c: jammingThreshold, regime };
}
