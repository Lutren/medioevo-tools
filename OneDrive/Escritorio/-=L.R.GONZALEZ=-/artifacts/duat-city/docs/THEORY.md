# DUAT Agent City — Theory Reference

> Math canon update 2026-05-20: this artifact contains pre-07b formulas.
> Active math must use `07b_MATEMATICAS_RIGUROSO.md`. The `muK`/`fibKMult`
> section below is historical implementation context, not active OSIT canon.
> Use `mu_F` as Dirichlet inverse of `f(n)=F_n`; practical utility remains
> `INCOGNITA` until benchmark F5.

## Fibonacci-Möbius Arithmetic

The core math engine is identical to DUAT FibMob Lab. All functions operate over
the integers and have no physical interpretation.

### muK (DEPRECATED generalized Möbius function)
```
muK(n, k):
  - if n=1: return 1
  - factorize n = p1^e1 * p2^e2 * ... 
  - if any ei > 2: return 0   (compressed tick / void zone)
  - omega  = total prime factors
  - omegaBar = count of primes with exponent = 1
  - return (-1)^omega * k^omegaBar
```

### fibK (k-Fibonacci sequence)
```
fibK(1,k) = 1, fibK(2,k) = k
fibK(n,k) = k * fibK(n-1,k) + fibK(n-2,k)
```

### fibKMult (multiplicative Dirichlet inverse of muK)
```
fibKMult(n, k) = product over prime powers p^e in factorization of n:
    fibK(e+1, k)
```
This is the exact Dirichlet inverse: sum_{d|n} muK(d,k) * fibKMult(n/d,k) = [n=1].

### mobiusField (tile data)
Each tile at position (x,y) receives id = y*W + x + 1.
mobiusField(id, k=1) returns:
- mu: muK(id, 1)
- lodFactor: 0.2 (void), 0.65 (compressed), 1.0 (expanded)
- polarity: positive / negative / void
- rarity: fibK((omega % 12) + 1, k) / 100

## Global Metrics

### Residue R
Global R must be computed with 07b forms:

```
R_or = 1 - Π_i(1-r_i)        # compounded risk
R_lin = Σ_i(w_i*r_i)/Σ_i w_i # UI/admin average only
```

Legacy artifact context used weighted average of:
- Average agent R (from individual need deficits)
- Task failure rate
- Resource shortage penalties
- Ruin count * 0.04

### Effective Throughput Φ_eff
Φ_eff = (1 - R) + adjustment based on avg mood & trust

### Regime Classification
| Regime    | R       | Φ_eff  |
|-----------|---------|--------|
| OPTIMO    | ≤ 0.15  | ≥ 0.75 |
| FUNCIONAL | ≤ 0.30  | ≥ 0.60 |
| CARGADO   | ≤ 0.60  | any    |
| SATURADO  | > 0.60  | any    |

### Gate
- APPROVE: R ≤ 0.35
- REVIEW: 0.35 < R ≤ 0.60
- BLOCK: R > 0.60

## EML Operator
```
EML(s,c; alpha,beta,theta) = sigma(alpha*s - beta*log(1+c) - theta)
sigma(z) = 1 / (1 + exp(-z))
```
Used to classify city expansion direction: EXPAND / HOLD / COMPRESS.

## Agent Needs (6 dimensions)
1. energy — depletes fastest; restored at residential, clinic
2. hunger — food-related; restored at garden, market  
3. social — community; restored at plaza, temple, market
4. purpose — role fulfillment; restored by role-matched tasks
5. safety — restored at clinic, gatehouse
6. curiosity — exploration drive; restored at observatory, archive

When a need drops below 0.30, a task is automatically scheduled.

## LOD Control
- lodFactor from mobiusField controls visual detail level
- Compressed ticks (mu=0): lodFactor=0.2, reduced detail
- Camera zoom also affects LOD rendering
