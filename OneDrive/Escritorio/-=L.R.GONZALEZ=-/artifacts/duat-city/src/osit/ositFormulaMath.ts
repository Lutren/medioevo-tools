export function shannonEntropy(probabilities: number[]): number {
  const normalized = normalize(probabilities);
  return round(normalized.reduce((sum, p) => p > 0 ? sum - p * Math.log2(p) : sum, 0));
}

export function boltzmannResidue(microstateCount: number): number {
  return round(Math.log(Math.max(1, finite(microstateCount))) / 12);
}

export function fourierSignalEnergy(samples: number[]): number {
  if (samples.length === 0) return 0;
  const mean = samples.reduce((sum, value) => sum + finite(value), 0) / samples.length;
  const energy = samples.reduce((sum, value) => sum + Math.abs(finite(value) - mean), 0) / samples.length;
  return round(energy);
}

export function gaussianEvidenceWeight(value: number, mean = 0, sigma = 1): number {
  const safeSigma = Math.max(0.0001, Math.abs(finite(sigma)));
  const z = (finite(value) - finite(mean)) / safeSigma;
  return round(Math.exp(-0.5 * z * z));
}

export function eulerStep(value: number, derivative: number, dt: number): number {
  return round(finite(value) + finite(derivative) * Math.max(0, finite(dt)));
}

export function newtonMotionProxy(position: number, velocity: number, acceleration: number, dt: number): number {
  const t = Math.max(0, finite(dt));
  return round(finite(position) + finite(velocity) * t + 0.5 * finite(acceleration) * t * t);
}

export function navierStokesFlowProxy(velocity: number, density: number, viscosity: number): number {
  return round(Math.abs(finite(velocity)) * Math.max(0, finite(density)) / (1 + Math.max(0, finite(viscosity))));
}

export function maxwellFieldProxy(electric: number, magnetic: number): number {
  return round(Math.sqrt(finite(electric) ** 2 + finite(magnetic) ** 2));
}

export function schrodingerProbabilityBoundary(real: number, imaginary: number): number {
  return round(finite(real) ** 2 + finite(imaginary) ** 2);
}

export function blackScholesRiskProxy(volatility: number, timeToExpiry: number, moneyness: number): number {
  return round(Math.abs(finite(volatility)) * Math.sqrt(Math.max(0, finite(timeToExpiry))) + Math.abs(finite(moneyness) - 1) * 0.25);
}

function normalize(values: number[]): number[] {
  const clean = values.map(value => Math.max(0, finite(value)));
  const sum = clean.reduce((acc, value) => acc + value, 0);
  if (sum <= 0) return values.map(() => 0);
  return clean.map(value => value / sum);
}

function finite(value: number): number {
  return Number.isFinite(value) ? value : 0;
}

function round(value: number): number {
  return Number(Math.max(0, Number.isFinite(value) ? value : 0).toFixed(6));
}
