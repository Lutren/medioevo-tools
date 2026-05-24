# MODULE_BOUNDARY_MAP

## Regla central

DUAT no carga como nucleo el creador tipo Lovable. DUAT es simulador observable, mundo, cockpit y sandbox. El creador de juegos/apps queda separado como `MEDIOEVO_FORGE`, con integracion por contratos y preview, no por dependencia central.

## 1. WABI_SABI_CONTROL_PLANE

Responsabilidad:
- Orquestacion local, ActionGate, ProviderGate, diagnostico y planificacion.
- Captura multimodal metadata-only.
- Propuestas cloud como input revisable, no ejecucion directa.

Rutas:
- `apps/local/wabi-sabi`
- `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\04_WABI_SABI`
- `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui`

No debe:
- Renderizar DUAT como dependencia dura.
- Enviar canon privado o media bruto a nube.

## 2. DUAT_SIMULATOR_WORLD

Responsabilidad:
- WorldState, agentes, eventos, tarea/social graph/replay.
- Render web-first, cockpit, inspectors, overlays.
- Escenas ciudad 3D/iso, dungeon 2.5D, metroidvania 2D/2.5D.

Rutas:
- `artifacts/duat-city`
- `research/geodia-social-observatory`
- `research/duat-predictive-registry`
- `library/modules/duat_world_state.json`

No debe:
- Depender del builder Lovable como nucleo.
- Publicar o mezclar assets protegidos sin ficha.

## 3. MEDIOEVO_FORGE_APP_GAME_CREATOR

Responsabilidad:
- Crear apps/juegos, plantillas, event sheets, previews.
- Exportar specs que DUAT pueda simular o visualizar.

Rutas:
- `apps/local/wabi-sabi/wabi_sabi/engine`
- Zips Lovable bajo `99_ARCHIVE_REVIEW`
- Documentos de intake Lovable/Wabi/DUAT.

Contrato con DUAT:
- `ForgeProjectSpec -> DUATScenarioSpec -> PreviewSnapshot`
- Sin dependencia inversa de DUAT hacia Forge.

## 4. MEDIOEVO_SPACE_PUBLIC_PORTAL

Responsabilidad:
- Superficie publica, bajo claim, sin runtime privado.

Rutas:
- `website`
- `publish_staging/medioevo-duat-public-release`
- `docs/publishing`

## 5. SHARED_CONTRACTS

Responsabilidad:
- Esquemas JSON/Python/TS para ActionGate, WitnessEvent, ObservationEnvelope, ReplayHash, SourceCard, ScenarioSpec.

Rutas:
- `packages/open-dev/duat-genesis`
- `research/*/schemas`
- `apps/local/wabi-sabi/wabi_sabi/contracts`
- `artifacts/duat-city/src/core/types.ts`

## 6. PROTECTED_CANON_OR_ASSETS

Responsabilidad:
- Canon/libros/RPG/assets privados. Solo lectura local segura y metadata cuando haga falta.

Rutas:
- `06_BOOKS_RPG_PROTECTED`
- `game-private`
- `metaevo-tcg`
- `runtime/game_bridge`
- `DUAT ASSETS` hasta que exista ficha de adopcion.

## 7. DEPRECATED_OR_DUPLICATE

Responsabilidad:
- Fuentes historicas, zips duplicados, proyectos extraidos, backups, patches previos.

Rutas:
- `_archive`
- `09_ARCHIVE_REVIEW`
- `99_ARCHIVE_REVIEW`
- `99_INBOX_UNSORTED`
- zips con `.git` o builds vendorizados.

