# PROJECT_INVENTORY DUAT WEB-FIRST ENGINE 2026-05-20

## Alcance auditado

- Root principal: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`
- Root operativo visible: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-`
- Politica aplicada: lectura local segura, sin push, sin deploy, sin commit, sin publicar, sin imprimir secretos.

## Modulos reales encontrados

### Wabi-Sabi control plane

- `apps/local/wabi-sabi`
  - `wabi_sabi/core/geodia_math_core.py`: nucleo matematico OSIT/GEODIA con `R`, `Phi_eff`, `epsilon`, `EML`, regimen y random inyectable.
  - `wabi_sabi/core/multimodal_intake.py`: captura metadata-only para camara/microfono; no guarda imagen/audio bruto.
  - `wabi_sabi/core/graphics_bridge.py`: bridge plan-only hacia graficos DUAT; no publica ni llama servicios externos.
  - `wabi_sabi/engine/modular_engine.py`: motor modular tipo app/game creator clean-room.
  - `wabi_sabi/engine/project_runtime.py`: sandbox local para specs/event sheets.
- `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui`
  - Cockpit local conversacional, API local `127.0.0.1:8787`, multimodal v0.3 estrecho y metadata/hash-only.

### DUAT simulator world

- `artifacts/duat-city`
  - App web-first Vite/React/Canvas.
  - Simulacion en `src/sim`.
  - Render Canvas en `src/render` y `src/graphics`.
  - Iluminacion en `src/graphics/lightEngine.ts`, `src/light/lightPropagation.ts`, `src/iso3d/vermeerIsoLighting.ts`.
  - Fisica en `src/physics` y `src/physicsField`.
  - RPG/metroidvania en `src/rpg`.
  - Audio procedural en `src/audio/proceduralSynth.ts`.
- `research/geodia-social-observatory`
  - Lab Smallville/DUAT CPU-only, sintetico, determinista, con replay verifier.
- `research/duat-predictive-registry`
  - Registro de prediccion, scoring, benchmarks y esquemas de corrida/remoto.
- `library/modules/duat_world_state.json`
  - Modulo de estado mundo DUAT.

### Forge / creador de juegos y apps

- `apps/local/wabi-sabi/wabi_sabi/engine/*`
- `docs/intake/LOVABLE_TO_WABI_DUAT_INTEGRATION_TASKS.md`
- Zips Lovable bajo BRAIN_OS archive review.

### Portal publico

- `website`
- `publish_staging/medioevo-duat-public-release`
- `docs/publishing`

### Canon y assets protegidos

- `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\06_BOOKS_RPG_PROTECTED`
- `game-private`, `metaevo-tcg`, `runtime/game_bridge` segun AGENTS.
- `DUAT ASSETS` requiere ficha antes de adopcion cruda.

## ZIPs inspeccionados sin extraccion

- `PRODUCTOS_MEDIOEVO\claudio_os_blueprint.zip`: 26 KB, 43 entradas; docs, contratos y blueprint Claudio OS.
- `ASSETS\WABI_VISUALS\duat-physics-light-engine-v1.3.0.zip`: 41 KB, 34 entradas; motor TS con fisica/light field.
- `ASSETS\WABI_VISUALS\duat-brain-os-v1.4.0.zip`: 23 KB, 29 entradas; brain/action-gate/attention TS.
- `99_ARCHIVE_REVIEW\2026-05-20_ROOT_TECH_SOURCE_CANDIDATES\Duat-Fibmob-Lab.zip`: 221 MB, 32143 entradas; incluye `.git`, requiere intake selectivo.
- `99_ARCHIVE_REVIEW\2026-05-20_ROOT_TECH_SOURCE_CANDIDATES\lovable-project-...2026-05-20.zip`: 176 KB, 119 entradas; proyecto Lovable, fuente de Forge, no nucleo DUAT.

## Hallazgos de inventario

- Existe un motor web-first real: `artifacts/duat-city`.
- Existe un sim-core local-first real: GEODIA/Smallville y DUAT predictive registry.
- Existe Wabi como control plane local con multimodal metadata-only.
- No se encontro un proyecto Godot activo (`project.godot`, `.tscn`, `.gd`) en las rutas auditadas no protegidas.
- El creador tipo Lovable existe como material de Forge/intake, no debe ser nucleo DUAT.

