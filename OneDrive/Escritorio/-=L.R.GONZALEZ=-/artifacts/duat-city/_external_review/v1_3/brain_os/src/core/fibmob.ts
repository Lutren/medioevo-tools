/**
 * Fibonacci-Möbius Core
 */
export function fibonacciSequence(n: number): number[] {
  const fib = [0, 1];
  for (let i = 2; i <= n; i++) fib[i] = fib[i-1] + fib[i-2];
  return fib;
}

export function fibMobWeight(d: number, order: number = 2): number {
  if (d <= 0) return 1.0;
  const fib = fibonacciSequence(order + 3);
  const base = fib[order + 2] || 2;
  let weight = 1.0, temp = d;
  for (let i = 2; i * i <= temp; i++) {
    if (temp % i === 0) {
      let exp = 0;
      while (temp % i === 0) { temp /= i; exp++; }
      const f = fibonacciSequence(exp + 2);
      weight *= f[exp + 1] / Math.pow(base, exp);
    }
  }
  if (temp > 1) weight *= 1.0 / base;
  return Math.max(0, Math.min(1, weight));
}
