/**
 * Fibonacci-Möbius (FibMob) — Core Matemático
 * 
 * FibMob se entiende como inversa de Dirichlet de una función 
 * aritmética multiplicativa inducida por recurrencia lineal de orden 2.
 * 
 * Uso operacional en el motor:
 * - Agregados estructurados (LOD físico/lumínico)
 * - Propagación con pesos que respetan jerarquía de divisores
 * - Reconstrucción desde sumas parciales (residue-first)
 */

/**
 * Genera secuencia de Fibonacci hasta n
 */
export function fibonacciSequence(n: number): number[] {
  const fib = [0, 1];
  for (let i = 2; i <= n; i++) {
    fib[i] = fib[i - 1] + fib[i - 2];
  }
  return fib;
}

/**
 * Función de Möbius clásica (para referencia)
 * μ(n): 1 si n=1, 0 si n tiene factor cuadrado, (-1)^k si n producto de k primos distintos
 */
export function mobius(n: number): number {
  if (n === 1) return 1;
  let p = 0;
  let temp = n;
  for (let i = 2; i * i <= temp; i++) {
    if (temp % i === 0) {
      let count = 0;
      while (temp % i === 0) {
        temp /= i;
        count++;
      }
      if (count > 1) return 0;
      p++;
    }
  }
  if (temp > 1) p++;
  return p % 2 === 0 ? 1 : -1;
}

/**
 * FibMob Weight: peso para agregación basado en divisores estructurados
 * 
 * Para un índice de distancia d, calcula peso usando función 
 * multiplicativa inducida por recurrencia de orden 2.
 * 
 * Uso: en LOD, propagación lumínica, y spatial hash.
 */
export function fibMobWeight(d: number, order: number = 2): number {
  if (d <= 0) return 1.0;
  // Aproximación operacional: peso decreciente con estructura FM
  const fib = fibonacciSequence(order + 3);
  const base = fib[order + 2] || 2;
  // Función multiplicativa: producto sobre divisores con estructura de recurrencia
  let weight = 1.0;
  let temp = d;
  for (let i = 2; i * i <= temp; i++) {
    if (temp % i === 0) {
      let exp = 0;
      while (temp % i === 0) {
        temp /= i;
        exp++;
      }
      // Aplicar recurrencia de orden 2 al exponente
      const f = fibonacciSequence(exp + 2);
      weight *= f[exp + 1] / Math.pow(base, exp);
    }
  }
  if (temp > 1) {
    weight *= 1.0 / base;
  }
  return Math.max(0, Math.min(1, weight));
}

/**
 * FibMob Convolution: convolución discreta con pesos FM
 * 
 * Usada para propagación de luz, presión de fluidos, y difusión térmica.
 * La convolución respeta jerarquía de distancia (divisores estructurados).
 */
export function fibMobConvolution(
  values: Float32Array,
  radius: number,
  centerIndex: number
): number {
  let sum = 0;
  let weightSum = 0;
  const len = values.length;

  for (let i = -radius; i <= radius; i++) {
    const idx = centerIndex + i;
    if (idx < 0 || idx >= len) continue;
    const d = Math.abs(i);
    const w = fibMobWeight(d, 2);
    sum += values[idx] * w;
    weightSum += w;
  }

  return weightSum > 0 ? sum / weightSum : 0;
}

/**
 * FibMob LOD Selector: decide nivel de detalle basado en distancia
 * 
 * Retorna factor de agregación: 1 = full detail, >1 = agregado
 */
export function fibMobLOD(distance: number, baseLOD: number = 16): number {
  if (distance <= 0) return 1;
  // Usar propiedad de agregados estructurados de FM
  const fib = fibonacciSequence(8);
  let lod = 1;
  for (let i = fib.length - 1; i >= 2; i--) {
    if (distance > baseLOD * fib[i]) {
      lod = fib[i - 1];
      break;
    }
  }
  return Math.max(1, lod);
}

/**
 * FibMob Spatial Index: índice de hash espacial con distribución Fibonacci
 * 
 * Proporciona cobertura más uniforme que grid regular.
 */
export function fibMobSpatialHash(x: number, y: number, gridSize: number): number {
  const phi = 1.618033988749895; // golden ratio
  const n = Math.floor(x / gridSize) * 73856093 
          ^ Math.floor(y / gridSize) * 19349663;
  // Mezcla con proporción áurea para dispersión uniforme
  return Math.abs(Math.floor(n * phi) % 2147483647);
}
