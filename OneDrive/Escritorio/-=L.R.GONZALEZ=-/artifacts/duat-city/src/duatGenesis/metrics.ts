import type {
  LGModeSpectrum,
  SimulationMetrics,
  CosmologyState,
  DuatEngineParams,
} from "./types";

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0));
}

function normalizeBand(value: number, low: number, high: number): number {
  if (value <= low) return 0;
  if (value >= high) return 1;
  return (value - low) / (high - low);
}

function normalizedEntropy(values: number[]): number {
  const total = values.reduce((acc, value) => acc + Math.max(0, value), 0);
  if (total <= 1e-12) return 0;
  const entropy = values.reduce((acc, value) => {
    const p = Math.max(0, value) / total;
    return p > 0 ? acc - p * Math.log(p) : acc;
  }, 0);
  return clamp01(entropy / Math.log(values.length));
}

export { type LGModeSpectrum, type SimulationMetrics };

export class MetricsTracker {
  private persistentFrames = 0;
  private previousCentroid = { x: 0, y: 0 };
  private previousMean = 0;

  update(
    psi: Float32Array,
    previous: Float32Array,
    gravity: Float32Array,
    light: Float32Array,
    width: number,
    height: number,
    params: DuatEngineParams,
    clipArtifactRatio = 0,
  ): SimulationMetrics {
    const base = computeBaseMetrics(psi, previous, gravity, light, width, height, params);
    const lgSpectrum = computeLGModeSpectrum(psi, gravity, light, width, height);
    const obs = computeDimObsAndAtum(lgSpectrum, base.entropy, base.edge);
    const centroidShift = Math.hypot(
      base.centroidX - this.previousCentroid.x,
      base.centroidY - this.previousCentroid.y,
    );
    const meanShift = Math.abs(base.mean - this.previousMean);
    const persistent =
      base.mean > 0.035 &&
      base.mean < 0.86 &&
      base.variance > 0.002 &&
      base.activity < 0.15 &&
      centroidShift < 9 &&
      meanShift < 0.08;

    this.persistentFrames = persistent ? this.persistentFrames + 1 : 0;
    this.previousCentroid = { x: base.centroidX, y: base.centroidY };
    this.previousMean = base.mean;

    const persistenceScore = Math.min(1, this.persistentFrames / 36);
    const liveness = clamp01(
      0.23 * normalizeBand(base.mean, 0.035, 0.42) +
        0.2 * normalizeBand(base.variance, 0.002, 0.09) +
        0.17 * normalizeBand(base.entropy, 0.12, 0.68) +
        0.16 * normalizeBand(base.edge, 0.004, 0.19) +
        0.1 * base.balance +
        0.04 * lgSpectrum.lgBalance +
        0.1 * persistenceScore,
    );

    const osirisScore = clamp01(
      0.45 * liveness + 0.22 * persistenceScore + 0.2 * base.balance + 0.13 * (1 - Math.min(1, base.activity / 0.15)),
    );
    const residue = clamp01(
      0.46 * (Math.abs(params.chi - CHI_STAR) / 0.43) +
        0.25 * base.activity +
        0.19 * (1 - base.balance) +
        0.1 * clipArtifactRatio,
    );
    const phiEff = clamp01(1 - residue ** 1.097);
    const cosmologyState = classifyCosmology(base, liveness, this.persistentFrames);

    return {
      ...base,
      lgBalance: lgSpectrum.lgBalance,
      spectralEntropy: lgSpectrum.spectralEntropy,
      dimObs: obs.dimObs,
      atumScore: obs.atumScore,
      osirisScore,
      clipArtifactRatio,
      liveness,
      residue,
      phiEff,
      persistentFrames: this.persistentFrames,
      cosmologyState,
    };
  }

  reset(): void {
    this.persistentFrames = 0;
    this.previousCentroid = { x: 0, y: 0 };
    this.previousMean = 0;
  }
}

export function computeBaseMetrics(
  psi: Float32Array,
  previous: Float32Array,
  gravity: Float32Array,
  light: Float32Array,
  width: number,
  height: number,
  params: DuatEngineParams,
) {
  let sum = 0;
  let sum2 = 0;
  let activity = 0;
  let edge = 0;
  let gx = 0;
  let gy = 0;
  let gSum = 0;
  let lSum = 0;

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const value = psi[id];
      sum += value;
      sum2 += value * value;
      activity += Math.abs(value - previous[id]);
      edge += Math.abs(value - psi[id + 1]) + Math.abs(value - psi[(id + width) % psi.length]);
      gx += x * value;
      gy += y * value;
      gSum += gravity[id];
      lSum += light[id];
    }
  }

  const n = psi.length;
  const mean = sum / n;
  const variance = Math.max(0, sum2 / n - mean * mean);
  const entropy = -mean * Math.log(mean + 1e-9) - (1 - mean) * Math.log(1 - mean + 1e-9);
  const gMean = gSum / n;
  const lMean = lSum / n;
  const balance = clamp01(1 - (Math.abs(gMean - lMean) * 8 + Math.abs(params.chi - CHI_STAR) * 1.4));

  return {
    mean,
    variance,
    entropy,
    activity: activity / n,
    edge: edge / (n * 2),
    gMean,
    lMean,
    balance,
    centroidX: sum > 0 ? gx / sum : width / 2,
    centroidY: sum > 0 ? gy / sum : height / 2,
  };
}

export function computeRestrictionMatrixG(psi: Float32Array, width: number, height: number): Float32Array {
  const restriction = new Float32Array(psi.length);
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const center = psi[id];
      const neighborMean =
        (psi[(y * width + (x - 1 + width) % width)] +
          psi[(y * width + (x + 1) % width)] +
          psi[(((y - 1 + height) % height) * width + x)] +
          psi[(((y + 1) % height) * width + x)]) / 4;
      restriction[id] = clamp01(Math.abs(center - neighborMean) * 4 + center * 0.12);
    }
  }
  return restriction;
}

export function computeFisherL(psi: Float32Array, width: number, height: number): Float32Array {
  const distinguishability = new Float32Array(psi.length);
  let max = 0;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const id = y * width + x;
      const dx = (psi[y * width + ((x + 1) % width)] - psi[y * width + ((x - 1 + width) % width)]) / 2;
      const dy =
        (psi[(((y + 1) % height) * width + x)] - psi[(((y - 1 + height) % height) * width + x)]) / 2;
      const varianceFloor = psi[id] * (1 - psi[id]) + 1e-4;
      const value = (dx * dx + dy * dy) / varianceFloor;
      distinguishability[id] = value;
      if (value > max) max = value;
    }
  }
  if (max > 0) {
    for (let i = 0; i < distinguishability.length; i += 1) {
      distinguishability[i] = clamp01(distinguishability[i] / max);
    }
  }
  return distinguishability;
}

export function computeLGModeSpectrum(
  psi: Float32Array,
  gravity: Float32Array,
  light: Float32Array,
  width: number,
  height: number,
): LGModeSpectrum {
  const restriction = computeRestrictionMatrixG(psi, width, height);
  const distinguishability = computeFisherL(psi, width, height);
  let sum = 0;
  let sum2 = 0;
  let rSum = 0;
  let lSum = 0;
  let coupling = 0;
  for (let i = 0; i < psi.length; i += 1) {
    const value = psi[i];
    const r = clamp01((restriction[i] + gravity[i]) / 2);
    const l = clamp01((distinguishability[i] + light[i]) / 2);
    sum += value;
    sum2 += value * value;
    rSum += r;
    lSum += l;
    coupling += Math.sqrt(r * l);
  }
  const n = psi.length || 1;
  const mean = sum / n;
  const variance = Math.max(0, sum2 / n - mean * mean);
  const rMean = rSum / n;
  const lMean = lSum / n;
  const couplingMean = coupling / n;
  const modes: [number, number, number, number, number] = [
    clamp01(mean * 2),
    clamp01(variance * 18),
    clamp01(rMean * 3),
    clamp01(lMean * 3),
    clamp01(couplingMean * 4),
  ];
  const lgBalance = clamp01(1 - Math.abs(rMean - lMean) / Math.max(0.08, rMean + lMean));
  return {
    modes,
    threshold: 0.075,
    lgBalance,
    spectralEntropy: normalizedEntropy(modes),
  };
}

export function computeDimObsAndAtum(
  spectrum: LGModeSpectrum,
  entropy: number,
  edge: number,
): { dimObs: number; atumScore: number; activeModes: number } {
  const activeModes = spectrum.modes.filter((mode) => mode > spectrum.threshold).length;
  const dimObs = Math.max(1, activeModes);
  const atumScore = clamp01(
    0.35 * (activeModes / spectrum.modes.length) +
      0.3 * spectrum.spectralEntropy +
      0.2 * normalizeBand(entropy, 0.02, 0.36) +
      0.15 * normalizeBand(edge, 0.002, 0.08),
  );
  return { dimObs, atumScore, activeModes };
}

export function classifyCosmology(
  metrics: ReturnType<typeof computeBaseMetrics>,
  liveness: number,
  persistentFrames: number,
): CosmologyState {
  if (metrics.mean < 0.018 && metrics.activity < 0.018) return "NU";
  if (metrics.mean > 0.88 || (metrics.mean > 0.62 && metrics.variance < 0.006)) return "COLAPSO";
  if (persistentFrames >= 24 && liveness > 0.58 && metrics.activity < 0.08) return "OSIRIS";
  if (metrics.balance > 0.68 && metrics.variance > 0.01 && metrics.entropy > 0.22) return "MAAT";
  if (metrics.entropy > 0.34 && metrics.edge > 0.015) return "DUAT";
  return "ATUM";
}

export const CHI_STAR = 0.5671432904097838;
