/**
 * Homeostasis / Resource Regulator Engine
 * 
 * El cerebro regula temperatura, glucosa, oxígeno.
 * El motor regula CPU, memoria, batería.
 * 
 * Mide R_cpu, R_ram, R_battery y ajusta LOD de todos los motores
 * para mantener el sistema vivo.
 * 
 * Principio: si el cuerpo muere, la mente no importa.
 */

import { ResourceState, SystemMetrics, MotorPriority } from '../../types';
import { emlEvaluate } from '../../core/eml';

export interface ResourceAlert {
  type: 'CPU' | 'MEMORY' | 'TEMPERATURE' | 'FPS';
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  current: number;
  threshold: number;
  recommendedAction: string;
}

export class ResourceRegulator {
  private thresholds = {
    cpu: { low: 30, medium: 60, high: 80, critical: 95 },
    memory: { low: 128, medium: 256, high: 400, critical: 480 },
    temperature: { low: 40, medium: 60, high: 75, critical: 85 },
    fps: { low: 60, medium: 45, high: 30, critical: 15 }
  };

  private alerts: ResourceAlert[] = [];
  private history: ResourceState[] = [];
  private maxHistory = 60; // 1 segundo a 60fps

  /**
   * Medir estado actual y generar alertas
   */
  measure(state: ResourceState): ResourceAlert[] {
    this.alerts = [];
    this.history.push(state);
    if (this.history.length > this.maxHistory) this.history.shift();

    // CPU
    if (state.cpuUsed > this.thresholds.cpu.critical) {
      this.alerts.push({ type: 'CPU', severity: 'CRITICAL', current: state.cpuUsed, threshold: this.thresholds.cpu.critical, recommendedAction: 'EMERGENCY_COMPRESS_ALL' });
    } else if (state.cpuUsed > this.thresholds.cpu.high) {
      this.alerts.push({ type: 'CPU', severity: 'HIGH', current: state.cpuUsed, threshold: this.thresholds.cpu.high, recommendedAction: 'REDUCE_RENDER_LOD' });
    }

    // Memory
    if (state.memoryUsed > this.thresholds.memory.critical) {
      this.alerts.push({ type: 'MEMORY', severity: 'CRITICAL', current: state.memoryUsed, threshold: this.thresholds.memory.critical, recommendedAction: 'FLUSH_CACHES' });
    } else if (state.memoryUsed > this.thresholds.memory.high) {
      this.alerts.push({ type: 'MEMORY', severity: 'HIGH', current: state.memoryUsed, threshold: this.thresholds.memory.high, recommendedAction: 'DISABLE_SIMULATION' });
    }

    // Temperature
    if (state.temperature > this.thresholds.temperature.critical) {
      this.alerts.push({ type: 'TEMPERATURE', severity: 'CRITICAL', current: state.temperature, threshold: this.thresholds.temperature.critical, recommendedAction: 'THROTTLE_ALL' });
    }

    // FPS
    if (state.fps < this.thresholds.fps.critical) {
      this.alerts.push({ type: 'FPS', severity: 'CRITICAL', current: state.fps, threshold: this.thresholds.fps.critical, recommendedAction: 'DROP_TO_30FPS' });
    } else if (state.fps < this.thresholds.fps.high) {
      this.alerts.push({ type: 'FPS', severity: 'HIGH', current: state.fps, threshold: this.thresholds.fps.high, recommendedAction: 'REDUCE_PHYSICS_SUBSTEPS' });
    }

    return this.alerts;
  }

  /**
   * Calcular métricas de recursos como R/Phi
   */
  computeResourceMetrics(): SystemMetrics {
    if (this.history.length < 2) {
      return { R: 0.1, Phi_eff: 0.9, J_c: 0.8, regime: 'OPTIMO' };
    }

    const recent = this.history.slice(-10);
    const avgCpu = recent.reduce((s, h) => s + h.cpuUsed, 0) / recent.length;
    const avgMem = recent.reduce((s, h) => s + h.memoryUsed, 0) / recent.length;
    const avgFps = recent.reduce((s, h) => s + h.fps, 0) / recent.length;

    // R: proporción de recursos usados (más alto = más saturado)
    const R = Math.min(1, (avgCpu / 100 + avgMem / 512) / 2);

    // Phi_eff: estabilidad de FPS (más estable = más eficiente)
    const fpsVariance = recent.reduce((s, h) => s + (h.fps - avgFps) ** 2, 0) / recent.length;
    const Phi_eff = Math.max(0, 1 - fpsVariance / 1000);

    // J_c: umbral de throttling
    const J_c = 0.85;

    let regime: SystemMetrics['regime'] = 'OPTIMO';
    if (R > 0.8) regime = 'JAMMED';
    else if (R > 0.5) regime = 'SATURADO';
    else if (Phi_eff < 0.5) regime = 'CRITICO';

    return { R, Phi_eff, J_c, regime };
  }

  /**
   * Ajustar motores basado en alertas
   */
  adjustMotors(motors: MotorPriority[]): MotorPriority[] {
    const critical = this.alerts.filter(a => a.severity === 'CRITICAL');
    const high = this.alerts.filter(a => a.severity === 'HIGH');

    for (const motor of motors) {
      if (critical.length > 0) {
        // Modo emergencia
        if (motor.name !== 'audio') {
          motor.currentLOD = 1;
          motor.enabled = false;
        }
      } else if (high.length > 0) {
        // Reducir según tipo de alerta
        const cpuAlert = this.alerts.find(a => a.type === 'CPU');
        const memAlert = this.alerts.find(a => a.type === 'MEMORY');

        if (cpuAlert && motor.name === 'render') {
          motor.currentLOD = Math.max(motor.minLOD, motor.currentLOD - 2);
        }
        if (memAlert && motor.name === 'simulation') {
          motor.enabled = false;
        }
      }
    }

    return motors;
  }

  getHistory(): ResourceState[] { return [...this.history]; }
  getAlerts(): ResourceAlert[] { return [...this.alerts]; }
}
