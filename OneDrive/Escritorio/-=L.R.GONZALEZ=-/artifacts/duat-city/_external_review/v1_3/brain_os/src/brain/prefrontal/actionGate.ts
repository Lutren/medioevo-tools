/**
 * Corteza Prefrontal / ActionGate Executive Engine
 * 
 * Gobierno operativo del cerebro. Decide qué motor corre,
 * cuándo, y con qué recursos.
 * 
 * Si R_system > 0.5 → bloquea nuevas tareas, activa recuperación.
 * Si Phi_eff bajo → comprime LOD de todos los motores.
 * Si CPU > 80% → baja prioridad de render, sube prioridad de audio.
 * 
 * Principio: no ejecutar sin gate. No gastar sin presupuesto.
 */

import { ActionDecision, ResourceBudget, SystemMetrics, Gate, Regime } from '../../types';
import { emlEvaluate, emlGate } from '../../core/eml';

export interface MotorPriority {
  name: string;
  baseCpu: number;
  baseMemory: number;
  currentLOD: number;
  minLOD: number;
  maxLOD: number;
  enabled: boolean;
}

export class ActionGateExecutive {
  private motors: Map<string, MotorPriority> = new Map();
  private decisions: ActionDecision[] = [];
  private globalBudget: ResourceBudget = { cpuPercent: 100, memoryMB: 512, timeMs: 16.67 };

  registerMotor(name: string, baseCpu: number, baseMemory: number, maxLOD: number = 8) {
    this.motors.set(name, {
      name, baseCpu, baseMemory,
      currentLOD: maxLOD, minLOD: 1, maxLOD,
      enabled: true
    });
  }

  /**
   * Decidir acciones para este frame basado en métricas globales
   */
  decide(metrics: SystemMetrics, resources: { cpu: number; memory: number }): ActionDecision[] {
    this.decisions = [];

    // Evaluar EML del sistema
    const eml = emlEvaluate(metrics.Phi_eff, metrics.R);

    // Si sistema saturado, comprimir todo
    if (eml.mode === 'COMPRESS' || metrics.regime === 'SATURADO') {
      this.compressAllMotors();
    }

    // Si sistema óptimo, expandir motores críticos
    if (eml.mode === 'EXPAND' && metrics.regime === 'OPTIMO') {
      this.expandCriticalMotors();
    }

    // Si JAMMED, bloquear todo excepto recuperación
    if (metrics.regime === 'JAMMED') {
      this.emergencyMode();
    }

    // Ajustar por recursos reales
    if (resources.cpu > 80) {
      this.reduceMotorLOD('render', 2);
      this.reduceMotorLOD('physics', 1);
    }
    if (resources.memory > 400) {
      this.disableMotor('simulation');
    }

    // Generar decisiones
    for (const [name, motor] of this.motors) {
      if (!motor.enabled) continue;

      const decision: ActionDecision = {
        action: motor.enabled ? 'RUN' : 'SKIP',
        target: name,
        priority: this.computePriority(name, metrics),
        resourceBudget: {
          cpuPercent: motor.baseCpu * (motor.currentLOD / motor.maxLOD),
          memoryMB: motor.baseMemory,
          timeMs: this.globalBudget.timeMs / this.motors.size
        },
        gate: this.computeGate(metrics, motor),
        rationale: `R=${metrics.R.toFixed(2)} Phi=${metrics.Phi_eff.toFixed(2)} LOD=${motor.currentLOD}`
      };

      this.decisions.push(decision);
    }

    // Ordenar por prioridad
    this.decisions.sort((a, b) => b.priority - a.priority);

    return this.decisions;
  }

  private computePriority(name: string, metrics: SystemMetrics): number {
    const priorities: Record<string, number> = {
      'audio': 10,      // audio nunca se corta (feedback crítico)
      'physics': 8,     // física base del mundo
      'light': 6,       // luz ambiental
      'render': 5,      // visual (puede bajar LOD)
      'npc': 7,         // NPCs inteligentes
      'quest': 4,       // misiones
      'simulation': 3   // simulación social
    };
    let p = priorities[name] || 5;
    if (metrics.R > 0.5) p *= 0.5; // penalizar si hay mucho residuo
    return p;
  }

  private computeGate(metrics: SystemMetrics, motor: MotorPriority): Gate {
    if (metrics.regime === 'JAMMED') return 'BLOCK';
    if (metrics.regime === 'SATURADO' && motor.name !== 'audio') return 'REVIEW';
    if (motor.currentLOD < motor.minLOD) return 'BLOCK';
    return 'APPROVE';
  }

  private compressAllMotors() {
    for (const motor of this.motors.values()) {
      motor.currentLOD = Math.max(motor.minLOD, Math.floor(motor.currentLOD * 0.7));
    }
  }

  private expandCriticalMotors() {
    for (const motor of this.motors.values()) {
      if (motor.name === 'audio' || motor.name === 'physics') {
        motor.currentLOD = Math.min(motor.maxLOD, motor.currentLOD + 1);
      }
    }
  }

  private emergencyMode() {
    for (const motor of this.motors.values()) {
      if (motor.name !== 'audio') {
        motor.enabled = false;
      } else {
        motor.currentLOD = 1; // audio mínimo
      }
    }
  }

  private reduceMotorLOD(name: string, amount: number) {
    const motor = this.motors.get(name);
    if (motor) {
      motor.currentLOD = Math.max(motor.minLOD, motor.currentLOD - amount);
    }
  }

  private disableMotor(name: string) {
    const motor = this.motors.get(name);
    if (motor) motor.enabled = false;
  }

  getMotor(name: string): MotorPriority | undefined { return this.motors.get(name); }
  getAllMotors(): MotorPriority[] { return Array.from(this.motors.values()); }
  getDecisions(): ActionDecision[] { return this.decisions; }
}
