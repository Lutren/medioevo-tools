/**
 * EML — Selector Expansión/Compresión
 * 
 * EML(x, y) = exp(x) - ln(y)
 * 
 * Lectura operacional:
 * - expande si la señal tiene baja saturación
 * - comprime si el costo/residuo crece
 * - gate de complejidad para handoff
 */

export interface EMLResult {
  value: number;
  mode: 'EXPAND' | 'COMPRESS' | 'HOLD';
  tension: number;
}

/**
 * Evalúa EML para decidir modo operativo
 * @param signal — intensidad de señal (0-1)
 * @param residue — residuo/costo (0-1)
 */
export function emlEvaluate(signal: number, residue: number): EMLResult {
  const s = Math.max(0.001, Math.min(1, signal));
  const r = Math.max(0.001, Math.min(1, residue));

  const value = Math.exp(s) - Math.log(r);
  const tension = value / (Math.E + Math.log(1000)); // normalizado aprox

  let mode: EMLResult['mode'] = 'HOLD';
  if (value > 2.5) mode = 'EXPAND';
  else if (value < 1.5) mode = 'COMPRESS';

  return { value, mode, tension };
}

/**
 * EML para substepping de física:
 * si tensión alta → más pasos locales (expand)
 * si residuo bajo → menos pasos (compress)
 */
export function emlSubsteps(
  energy: number, 
  localResidue: number, 
  maxSteps: number = 8
): number {
  const eml = emlEvaluate(energy, localResidue);
  switch (eml.mode) {
    case 'EXPAND': return Math.ceil(maxSteps * 0.8);
    case 'COMPRESS': return Math.max(1, Math.floor(maxSteps * 0.3));
    case 'HOLD': return Math.ceil(maxSteps * 0.5);
  }
}

/**
 * EML para LOD de render/luz:
 * decide si dibujar/computar a resolución completa o agregada
 */
export function emlLOD(
  localComplexity: number,
  sceneResidue: number,
  baseLOD: number = 16
): number {
  const eml = emlEvaluate(localComplexity, sceneResidue);
  if (eml.mode === 'EXPAND') return 1; // full detail
  if (eml.mode === 'COMPRESS') return Math.max(2, Math.floor(baseLOD / eml.tension));
  return Math.max(1, Math.floor(baseLOD / (2 * eml.tension)));
}

/**
 * EML Gate: decide si integrar, testear, mantener o bloquear
 * basado en claridad de comunicación y residuo
 */
export function emlGate(
  clarity: number,
  residue: number
): 'INTEGRATE' | 'TEST' | 'HOLD' | 'BLOCK' {
  const eml = emlEvaluate(clarity, residue);
  if (eml.mode === 'EXPAND' && clarity > 0.7) return 'INTEGRATE';
  if (eml.mode === 'EXPAND' && clarity <= 0.7) return 'TEST';
  if (eml.mode === 'HOLD') return 'HOLD';
  return 'BLOCK';
}
