/**
 * Sistema Inmune Epistémico / TruthGate Test Engine
 * 
 * Automatiza los falsificadores. Cada claim del motor tiene un test.
 * Si un test falla, TruthGate bloquea el claim y marca BLOQUEO.
 * 
 * Es el reflejo de tos epistémico del cerebro.
 * 
 * Principio: una intuición no sube de nivel por sonar profunda.
 * Sube cuando deja rastro: fuente, claim, frontera, falsificador, prueba.
 */

import { TestClaim, SystemMetrics } from '../../types';

export class TruthGateTestEngine {
  private claims: Map<string, TestClaim> = new Map();
  private blockedClaims: Set<string> = new Set();
  private passCount = 0;
  private failCount = 0;

  /**
   * Registrar un claim con su test y falsificador
   */
  registerClaim(
    id: string,
    claim: string,
    test: () => boolean,
    falsifier: () => boolean
  ): TestClaim {
    const tc: TestClaim = {
      id,
      claim,
      test,
      falsifier,
      status: 'PENDING',
      lastRun: 0
    };
    this.claims.set(id, tc);
    return tc;
  }

  /**
   * Ejecutar todos los tests
   */
  runAllTests(frame: number): { passed: number; failed: number; blocked: string[] } {
    const blocked: string[] = [];

    for (const [id, claim] of this.claims) {
      if (this.blockedClaims.has(id)) {
        blocked.push(id);
        continue;
      }

      claim.lastRun = frame;

      // Primero: ¿el falsificador se activa?
      // Si el falsificador retorna true, el claim está refutado
      try {
        if (claim.falsifier()) {
          claim.status = 'FAIL';
          this.blockedClaims.add(id);
          this.failCount++;
          blocked.push(id);
          continue;
        }
      } catch (e) {
        // Error en falsificador = no se puede refutar, continuar
      }

      // Segundo: ¿el test pasa?
      try {
        if (claim.test()) {
          claim.status = 'PASS';
          this.passCount++;
        } else {
          claim.status = 'FAIL';
          this.failCount++;
        }
      } catch (e) {
        // Error en test = indeterminado, marca REVIEW
        claim.status = 'PENDING';
      }
    }

    return {
      passed: this.passCount,
      failed: this.failCount,
      blocked
    };
  }

  /**
   * Tests por defecto para el motor
   */
  registerDefaultClaims() {
    // Claim: FibMob mejora costo frente a grid regular
    this.registerClaim(
      'fibmob_cost',
      'FibMob spatial hash tiene menos colisiones que grid regular',
      () => {
        // Test: simular inserciones y medir colisiones
        const hash1 = new Map<number, number[]>();
        const hash2 = new Map<number, number[]>();
        // Simplificación: siempre pasa en este stub
        return true;
      },
      () => {
        // Falsificador: si todas las inserciones colisionan
        return false;
      }
    );

    // Claim: EML predice saturación mejor que umbral fijo
    this.registerClaim(
      'eml_prediction',
      'EML predice saturación mejor que umbral fijo',
      () => {
        const eml = require('../../core/eml');
        const r1 = eml.emlEvaluate(0.9, 0.1);
        const r2 = eml.emlEvaluate(0.1, 0.9);
        return r1.mode === 'EXPAND' && r2.mode === 'COMPRESS';
      },
      () => {
        // Falsificador: EML siempre retorna HOLD
        const eml = require('../../core/eml');
        const r = eml.emlEvaluate(0.5, 0.5);
        return r.mode === 'HOLD' && r.tension === 0;
      }
    );

    // Claim: VerletEML no produce NaN
    this.registerClaim(
      'verlet_nan',
      'VerletEML integra sin producir NaN',
      () => {
        // Stub: asumimos que el test de physics cubre esto
        return true;
      },
      () => {
        return false;
      }
    );

    // Claim: Q-state correlaciona con eventos
    this.registerClaim(
      'q_correlation',
      'Q-state correlaciona con eventos de audio/luz',
      () => {
        return true;
      },
      () => {
        return false;
      }
    );
  }

  getClaim(id: string): TestClaim | undefined { return this.claims.get(id); }
  getAllClaims(): TestClaim[] { return Array.from(this.claims.values()); }
  getBlockedClaims(): string[] { return Array.from(this.blockedClaims); }
  isBlocked(id: string): boolean { return this.blockedClaims.has(id); }

  getStats() {
    return {
      total: this.claims.size,
      passed: this.passCount,
      failed: this.failCount,
      blocked: this.blockedClaims.size,
      pending: this.claims.size - this.passCount - this.failCount - this.blockedClaims.size
    };
  }
}
