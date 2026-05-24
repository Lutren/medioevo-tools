# REPLIT DUAT/GEODIA MODULE CANDIDATES 2026-05-07

## ESTADO

- Fuente: `-=CEREBRO=-\-=PSI=-\ReplitExport-lutren.tar.gz`
- Intake: `runtime/cerebro_archive_intake/ReplitExport-lutren_tar_ccac616e3076`
- SHA256 fuente: `ccac616e3076026284b3e3b5ad25e331fb66340d4ed992831ad5d8059e9aabe2`
- Gate: `REVIEW_BEFORE_IMPORT`
- Limpieza/import ejecutado: `false`

## CERTEZA

- El tar contiene un monorepo `Duat-Geodia` con frontend React/Vite, API Express, Drizzle/PostgreSQL, OpenAPI/Zod y motor TypeScript de simulación.
- El intake indexó `215` archivos textuales en cuarentena y bloqueó `.git`, caches y metadata.
- Los archivos revisados declaran postura `SYNTHETIC_ONLY`, `SIMULACIÓN`, `DEMO_ONLY` o `REVIEW_REQUIRED`.
- No se importó código al runtime activo ni se movió la fuente.

## INFERENCIA

- Hay tecnología reutilizable para Claudio/Wabi, pero debe entrar por contratos, no copiando el repo completo.
- El valor técnico P0 está en separar un núcleo matemático/simulador pequeño de la UI y del backend original.

## INCOGNITA

- Licencia/origen del paquete Replit no está cerrado.
- El código TypeScript no fue ejecutado en su stack original durante esta sesión.
- Las dependencias Node/PostgreSQL no deben instalarse ni activarse sin gate específico.

## CANDIDATOS P0

| Prioridad | Módulo | Fuente cuarentenada | Contrato mínimo | Prueba mínima | Gate |
|---|---|---|---|---|---|
| P0 | `geodia_math_core` | `text/33915915fcb5_geodia_ts.txt` | `computePhiEff`, `computeEpsilon`, `observeSignal`, `computeRegime`, `computePSI`; inputs numéricos normalizados; outputs acotados `[0,1]` y régimen | tests de monotonicidad: `Phi_eff` baja cuando sube `R`; `epsilon` sube con `R`; `R>=Jc => Phi_eff=0`; celda vacía devuelve estado óptimo | `APPROVE_LOCAL_REIMPLEMENT_WITH_TESTS` |
| P0 | `falsifier_matrix_synthetic` | `text/bfcbdfcc7bd0_physics_ts.txt` | controles negativos `shuffle_velocity`, `permute_radius`, `flat_noise`, `mirror_curve`; salida `PASS/WARN/FAIL/N/A` | fixtures sintéticos; baseline siempre `N/A`; perturbación debe degradar modelos sensibles; labels no publicables como física real | `REVIEW_CLAIMS_APPROVE_SYNTHETIC_ONLY` |
| P1 | `witness_api_contract` | `text/aad859aaf939_witness_ts.txt` | append/list recent witness events con `previous_hash` y `hash` | dos eventos encadenados; hash cambia si cambia payload; payload inválido => 400 | `APPROVE_IF_LOCAL_DB_ONLY` |
| P1 | `geodia_ui_panels` | `OperatorInventory`, `ReplayPanel`, `WitnessPanel`, `BootScreen`, `MainLab` en cuarentena | UI de observación para PSI, replay, witness y handoff | screenshot/local render solo después de elegir stack; sin claims fuertes | `REVIEW_UI_IMPORT` |
| P2 | `openapi_zod_bridge` | `text/f46de9456190_openapi_yaml.txt` | OpenAPI como contrato de API local | validar schema contra endpoints reales si se crea API | `REVIEW_DEPENDENCIES` |

## REGLAS DE IMPORT

- No copiar el repo entero.
- No copiar `.git`, lockfiles, generated clients o `node_modules`.
- No instalar dependencias de red sin ficha.
- No presentar `physics.ts` como validación científica; solo simulación sintética.
- Preferir reimplementación pequeña en `wabi_sabi/core` o contrato en `docs/intake` antes de tocar Claudio.
- Todo import debe tener test antes de marcarlo funcional.

## ACCION SIGUIENTE

`geodia_math_core` ya fue implementado como módulo pequeño, sin dependencias, en `apps/local/wabi-sabi/wabi_sabi/core/geodia_math_core.py`.

Siguiente acción: integrar `geodia_math_core` solo en superficies que puedan mostrarlo como `SYNTHETIC_ONLY`, sin convertir `physics.ts` en claim fuerte. Mantener `physics.ts` como `REVIEW_CLAIMS_APPROVE_SYNTHETIC_ONLY` hasta que exista claim contract y falsador numérico.

## ARTEFACTO

- Este archivo convierte el tar de Replit en backlog técnico trazable.
- El siguiente agente no necesita releer el tar completo para saber qué importar primero.
- Tests actuales: `apps/local/wabi-sabi` -> `131 passed`.
