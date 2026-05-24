# Fibonacci-Möbius en el Motor

**Fingerprint:** DUAT-v1.3.0-FIBMOB-ENGINE

## Definición Operacional

FibMob = inversa de Dirichlet de función aritmética multiplicativa inducida por recurrencia lineal de orden 2.

## Aplicaciones

### 1. Spatial Hash
```
hash(x, y) = floor(x/grid) * 73856093 XOR floor(y/grid) * 19349663
hash = abs(floor(hash * φ) % 2^31)
```
La proporción áurea φ dispersa clusters uniformemente.

### 2. Propagación Lumínica
```
L(x,y) = Σ L(x+dx, y+dy) * fibMobWeight(dist) * transmission
```
La luz se agrega con pesos que respetan jerarquía de divisores.

### 3. LOD (Level of Detail)
```
lod(d) = Fibonacci(i-1) si d > baseLOD * Fibonacci(i)
```
Agregados estructurados: lejos se suman celdas con pesos FM.

### 4. Dithering
```
dither(x,y) = (fib[(x*3 + y*5) % 8] / 21 - 0.5) * intensity
```
Secuencia de Fibonacci para distribución de ruido espacial.

## Propiedad Clave

FibMob respeta **estructura multiplicativa** del espacio.
No asume independencia entre celdas vecinas;
asume que la distancia tiene divisores que modulan la interacción.
