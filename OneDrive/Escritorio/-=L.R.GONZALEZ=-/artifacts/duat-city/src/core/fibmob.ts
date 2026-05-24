export interface Factor { p: number; exponent: number; }

export function factorize(n: number): Factor[] {
  if (n <= 1) return [];
  const factors: Factor[] = [];
  let rem = n;
  for (let p = 2; p * p <= rem; p++) {
    if (rem % p === 0) {
      let e = 0;
      while (rem % p === 0) { e++; rem = Math.floor(rem / p); }
      factors.push({ p, exponent: e });
    }
  }
  if (rem > 1) factors.push({ p: rem, exponent: 1 });
  return factors;
}

export function muK(n: number, k = 1): number {
  if (n <= 0) return 0;
  if (n === 1) return 1;
  const factors = factorize(n);
  for (const f of factors) { if (f.exponent > 2) return 0; }
  const omega = factors.length;
  const omegaBar = factors.filter(f => f.exponent === 1).length;
  const sign = omega % 2 === 0 ? 1 : -1;
  return sign * Math.pow(k, omegaBar);
}

const fibCache = new Map<string, number>();

export function fibK(n: number, k = 1): number {
  if (n <= 0) return 0;
  if (n === 1) return 1;
  if (n === 2) return k;
  const key = `${k}:${n}`;
  if (fibCache.has(key)) return fibCache.get(key)!;
  let a = 1, b = k;
  for (let i = 3; i <= n; i++) { const c = k * b + a; a = b; b = c; }
  fibCache.set(key, b);
  return b;
}

export function fibKMult(n: number, k = 1): number {
  if (n <= 0) return 0;
  if (n === 1) return 1;
  const factors = factorize(n);
  let result = 1;
  for (const f of factors) result *= fibK(f.exponent + 1, k);
  return result;
}

export interface MobiusFieldResult {
  mu: number;
  lodFactor: number;
  polarity: "positive" | "negative" | "void";
  rarity: number;
  emlValue: number;
}

export function mobiusField(n: number, k = 1): MobiusFieldResult {
  const factors = factorize(n);
  const omega = factors.length;
  const bigOmega = factors.reduce((a, f) => a + f.exponent, 0);
  const mu = muK(n, k);
  const rarity = fibK((omega % 12) + 1, k) / 100;

  const emlVal = Math.exp(Math.min(20, omega)) - Math.log(Math.max(1, bigOmega));
  const emlValue = isFinite(emlVal) ? emlVal : 1;

  let lodFactor: number;
  if (mu === 0) lodFactor = 0.2;
  else if (Math.abs(mu) >= 2) lodFactor = 1.0;
  else lodFactor = 0.65;

  let polarity: "positive" | "negative" | "void";
  if (mu > 0) polarity = "positive";
  else if (mu < 0) polarity = "negative";
  else polarity = "void";

  return { mu, lodFactor, polarity, rarity, emlValue };
}
