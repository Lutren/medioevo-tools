import type { Direction } from "./types";

export interface EMLResult {
  value: number;
  direction: Direction;
}

export interface EMLOptions {
  alpha?: number;
  beta?: number;
  theta?: number;
}

export function safeEml(signal: number, complexity: number, options: EMLOptions = {}): EMLResult {
  const alpha = finiteOr(options.alpha, 1);
  const beta = finiteOr(options.beta, 1);
  const theta = finiteOr(options.theta, 0);
  const s = Math.max(-20, Math.min(20, finiteOr(signal, 0)));
  const c = Math.max(0, finiteOr(complexity, 0));
  const z = Math.max(-60, Math.min(60, alpha * s - beta * Math.log1p(c) - theta));
  const value = 1 / (1 + Math.exp(-z));

  let direction: Direction;
  if (value > 0.65) direction = "EXPAND";
  else if (value < 0.35) direction = "COMPRESS";
  else direction = "HOLD";

  return { value, direction };
}

export function emlForCity(Phi_eff: number, R: number): EMLResult {
  return safeEml(Phi_eff, R);
}

function finiteOr(value: number | undefined, fallback: number): number {
  return Number.isFinite(value) ? value as number : fallback;
}
