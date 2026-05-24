# DUAT Physics + Light + Mechanics Engine v1.3.0
## Fingerprint: DUAT-v1.3.0-PHYSICS-LIGHT-MECHANICS-CPU

**Estado:** INTERNO_LOCAL / NO_PUBLICAR_SIN_GATE  
**ActionGate:** REVIEW → local reversible  
**R estimado:** 0.15 | **Régimen:** ÓPTIMO

---

## Propósito

Motor unificado de física, luz y mecánicas para DUAT/MEDIOEVO.
CPU-first. Residue-first. No simula todo; propaga deltas de estado.

Este documento traduce la ciencia de MEDIOEVO/OSIT a implementación operativa.

---

## Ciencia Aplicada

### Fibonacci-Möbius (FibMob)

**Teoría canon 07b:** `f(n)=F_n` no es multiplicativa. FibMob activo es
`mu_F`, el inverso de Dirichlet de `f(n)=F_n`, definido porque `f(1)=1`. Su
utilidad de motor queda `INCOGNITA` hasta benchmark F5.

**Uso en motor:**
- **Spatial Hash:** Distribución Fibonacci para indexación uniforme (`fibMobSpatialHash`). Reduce colisiones de hash en clusters.
- **Propagación Lumínica:** Convolución con pesos FM (`fibMobConvolution`). La luz no se difumina con inversa cuadrada; se AGREGA con Möbius, como si cada pared fuera un divisor que modula la señal.
- **LOD:** Selector de nivel de detalle basado en distancia (`fibMobLOD`). Lejos, el mundo se resume; cerca, se expande. Es nivel de detalle narrativo, no solo gráfico.

### EML — selector sigmoidal 07b

**Teoría:** `EML(s,c; alpha,beta,theta) = sigma(alpha*s - beta*log(1+c) - theta)`.
La formula `Exp(x) - Ln(y)` queda `DEPRECATED` y solo sirve como historico.

**Uso en motor:**
- **Substepping de física:** `emlSubsteps(energía, residuo)`. Más pasos donde hay tensión; menos donde hay calma.
- **LOD de render/luz:** `emlLOD(complejidad, residuo)`. Comprime en zonas oscuras/estáticas; expande en zonas de evento.
- **Gate de integración:** `emlGate(claridad, residuo)`. Decide si una celda entra en simulación completa, test o bloqueo.

### OSIT — Observación con Estado

**Teoría:** `Observation = f(State, Signal, Channel, Memory, Noise, Goal, Gate)`

**Uso en motor:**
- Cada celda es un observador (`OSITObserver`).
- No observa desde cero; observa desde estado previo.
- Memoria de 4 muestras (`Float32Array(4)`).
- Trend + Volatility → Q-state.
- Gate lógico: APPROVE/REVIEW/BLOCK según señal filtrada.

### Q-State Unificado

| Q | Audio | Luz | Física | Mecánicas |
|---|-------|-----|--------|-----------|
| 00 | silence/low hum | oscuridad esperada | equilibrio | zona segura |
| 01 | missing signal | anomalía lumínica | inestabilidad | quest hook |
| 10 | tono sostenido | iluminación estable | predecible | progresión |
| 11 | event burst | flash/revelación | colisión/transición | gate trigger |

### Conway-Material

Materiales como personajes con reglas locales:
- **Agua:** fluye, olvida (difumina estado anterior).
- **Fuego:** insiste (propagación con memoria corta).
- **Metal:** resiste hasta `J_c`, luego cede de golpe.
- **Humo:** miente (oculta sin borrar).
- **Cristal:** refracta/distorsiona (parciales inarmónicos).

---

## Arquitectura

```
GameMechanics
├── PhysicsEngine
│   ├── SpatialHashFib
│   ├── CellStateManager (Conway-Material)
│   └── VerletEML
├── LightFieldFM
│   ├── Propagación FM
│   ├── Q-State Light
│   └── LightEML Selector
├── NPCStateManager (OSIT)
├── QuestEngine (Residuo)
├── CPURenderer
│   ├── DeltaFramebuffer
│   └── IndexedPalette
└── Bridges
    ├── LightAudioBridge
    └── PhysicsAudioBridge
```

---

## Reglas del Mundo (Leyes Narrativas)

1. Dos cuerpos de obsidiana que chocan no rebotan; reconocen parentesco y se detienen.
2. El agua no fluye; olvida.
3. El fuego no quema; insiste.
4. El metal resiste hasta J_c, luego cede de golpe.
5. El humo miente: oculta sin borrar.
6. El cristal refracta la intención: la luz que entra Q=10 sale fragmentada en Q=01 y Q=11.
7. La luz no ilumina; anuncia.
8. El mundo no redibuja todo; solo describe lo que cambia.

---

## Falsificadores

El modelo falla si:
- FibMob no mejora costo frente a grid regular.
- EML no predice saturación mejor que umbral fijo.
- VerletEML produce NaN bajo presión extrema.
- Q-state no correlaciona con eventos de audio/luz.
- NPCs no reaccionan a cambios de Q-state.
- Render delta no reduce carga de CPU.

---

## Handoff

**Fingerprint:** DUAT-v1.3.0-PHYSICS-LIGHT-MECHANICS-CPU  
**Brief:** Motor unificado implementado. Física residue-first con Conway-Material, Verlet+EML, SpatialHash FM. Luz con propagación FM Q-state, EML selector, bridge audio. Mecánicas con NPC OSIT y Quest Engine. Render CPU delta con paleta indexada.  
**NextAction:** Integrar con audio engine v1.2.1 existente. Validar en escena de prueba.
