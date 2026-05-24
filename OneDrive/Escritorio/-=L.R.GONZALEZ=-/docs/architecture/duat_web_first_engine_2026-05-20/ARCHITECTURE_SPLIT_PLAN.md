# ARCHITECTURE_SPLIT_PLAN

## Recomendacion

Ruta principal: RUTA C HIBRIDA.

- Sim-core compartido, local-first y determinista.
- Frontend web-first ligero como cliente principal.
- Godot opcional como cliente avanzado despues de estabilizar contratos.
- Forge separado del simulador.

Ruta fallback: RUTA B CUSTOM WEB ENGINE.

- Si Godot agrega peso o deuda, continuar con web engine propio.
- Mantener Canvas low tier y sumar WebGL/Three.js high tier cuando haya benchmark.

## Arquitectura objetivo

```txt
WABI_SABI_CONTROL_PLANE
  -> ActionGate / ProviderGate / cloud proposals / multimodal metadata

SHARED_CONTRACTS
  -> WorldState / AgentState / ObservationEnvelope / WitnessEvent / ReplayHash

DUAT_SIM_CORE
  -> deterministic tick / tasks / social graph / memory / planning / replay

DUAT_WEB_RENDERER
  -> Canvas low tier / WebGL high tier / camera streaming / inspectors

MEDIOEVO_FORGE
  -> app-game creator / templates / preview specs

OPTIONAL_CLIENTS
  -> Godot client / static cinematic export / cloud batch runner
```

## Fases

### Fase 1: estabilizar contratos

- Crear `DUAT_SIM_CORE_SPEC`.
- Alinear GEODIA/DUAT City/registry con `WorldState` y `ReplayHash`.
- Separar tipos shared de tipos UI.

### Fase 2: extraer sim-core

- Mover tick determinista a paquete sin React.
- Worker-ready fixed timestep.
- Replay hash por tick.

### Fase 3: renderer web-first eficiente

- Mantener Canvas low-tier.
- Introducir `RenderSnapshot` inmutable.
- Usar camera chunks, dirty regions, static layer cache.

### Fase 4: Forge separado

- Wabi modular engine produce `ForgeProjectSpec`.
- DUAT solo preview/simula si recibe `DUATScenarioSpec` validado.

### Fase 5: Godot opcional

- Solo cliente de consumo de `WorldState`/`ReplayLedger`.
- No porta la logica canonica de simulacion.

## ActionGate

- APPROVE: docs, tests, sim deterministic fixes, local-only contracts.
- REVIEW: adopcion selectiva de ZIPs, nuevas dependencias, cloud providers.
- BLOCK: publicar, exponer secretos, mover/borrar protegido, usar zips como import crudo.
