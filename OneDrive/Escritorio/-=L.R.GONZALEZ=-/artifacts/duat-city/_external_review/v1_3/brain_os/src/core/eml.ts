/**
 * EML — Selector Expansión/Compresión
 * EML(x, y) = exp(x) - ln(y)
 */
export interface EMLResult {
  value: number;
  mode: 'EXPAND' | 'COMPRESS' | 'HOLD';
  tension: number;
}

export function emlEvaluate(signal: number, residue: number): EMLResult {
  const s = Math.max(0.001, Math.min(1, signal));
  const r = Math.max(0.001, Math.min(1, residue));
  const value = Math.exp(s) - Math.log(r);
  const tension = value / (Math.E + Math.log(1000));
  let mode: EMLResult['mode'] = 'HOLD';
  if (value > 2.5) mode = 'EXPAND';
  else if (value < 1.5) mode = 'COMPRESS';
  return { value, mode, tension };
}

export function emlGate(clarity: number, residue: number): 'INTEGRATE' | 'TEST' | 'HOLD' | 'BLOCK' {
  const eml = emlEvaluate(clarity, residue);
  if (eml.mode === 'EXPAND' && clarity > 0.7) return 'INTEGRATE';
  if (eml.mode === 'EXPAND' && clarity <= 0.7) return 'TEST';
  if (eml.mode === 'HOLD') return 'HOLD';
  return 'BLOCK';
}
