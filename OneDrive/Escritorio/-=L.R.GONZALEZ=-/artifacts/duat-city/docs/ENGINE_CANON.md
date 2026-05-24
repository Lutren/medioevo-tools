# ENGINE CANON

Fecha: 2026-05-22

## Declaracion

`artifacts/duat-city` es el motor canonico vivo de MEDIOEVO para DUAT Agent City y GlomoRender.

Nombre operativo:

- MEDIOEVO Engine
- DUAT Agent City Engine
- GlomoRender, cuando se habla del carril render/fisica/LOD

No crear `duat-city-v2`. No mover este paquete. No absorber ZIPs, copias stale ni fuentes crudas al runtime.

## Relacion Con Motores Vivos

| Motor | Ruta | Rol | Estado |
|---|---|---|---|
| DUAT City / GlomoRender | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\artifacts\duat-city` | Simulacion web/TS, fisica por cuerpo, fisica de campos, renderer, agentes, ciudad, modos, brain runtime y export RPG | Canon vivo para este carril |
| MEDIOEVO RPG Godot | `E:\Medioevo_RPG` | Juego privado jugable de la saga, fisica Godot, escenas, assets, lore y validadores privados | Motor vivo complementario, no rival |

`duat-city` exporta estado/mundo hacia el RPG por contratos como `src/rpg/worldExport.ts`. El RPG no debe copiarse ni mezclarse en este arbol; se verifica por su propia frontera privada.

## Fronteras

- PublicationGate: BLOCK.
- RuntimeImportGate para ZIPs/copia stale: BLOCK.
- RawAdoption: BLOCK.
- Extraccion selectiva: REVIEW hasta ficha, procedencia, target lane, test/evidencia y claim boundary.
- Claims de fisica/IA/consciencia: low-claim, engineering/game-system only.

## Evidencia Actual

Ultima verificacion local de Fase 0:

```powershell
npm test
npm run typecheck
npm run build
```

Resultado:

- `npm test`: 106 archivos de test / 314 tests passed.
- `npm run typecheck`: PASS.
- `npm run build`: PASS; Vite 5.4.21, 249 modules transformed.

Inventario vivo:

- `docs/ENGINE_TRUTH_INVENTORY_2026-05-21.md`
- `docs/CODEX_FINAL_HANDOFF_v1_5.md`
- `docs/TEST_REPORT_v1_5.md`
- `docs/PHYSICS_ENGINE.md`
- `docs/THEORY.md`

## Estado De Implementacion

Existe:

- Fisica por cuerpo en `src/physics`.
- Fisica de campos en `src/physicsField`.
- Ciudad/agentes/tareas/buildings en `src/sim` y `src/core`.
- Renderer y pixel realism en `src/render`, `src/graphics`, `src/iso3d`, `src/pixelRealism`.
- Modos de juego en `src/gameModes`.
- Brain/runtime surfaces en `src/brain`.
- Generadores procedurales en `src/generative`.
- Puente RPG en `src/rpg/worldExport.ts`.

Huecos confirmados para Fase 2:

1. Linaje de 2 generaciones y `originStory`.
2. Teatro para crear perfiles completos.
3. Academia con skill packs instalables.
4. Psicologo/reparacion de agentes que desvarian.

## Regla Operativa

La consolidacion canonica ocurre en sitio: documentar, testear y extender `artifacts/duat-city`. Cualquier copia historica debe apuntar hacia este arbol vivo y quedar marcada como stale, sin borrado directo.
