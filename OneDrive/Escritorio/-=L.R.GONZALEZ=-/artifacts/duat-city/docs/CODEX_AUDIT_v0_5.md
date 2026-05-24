# CODEX_AUDIT_v0_5

Fecha: 2026-05-19
Fingerprint: DUAT-CITY-PHYSICS-WABI-MCP-v0.5-PROMPT

## Que existe

- Proyecto React/Vite `@workspace/duat-city` con Canvas 2D, modos CITY/AGENT/RPG/OSIT, simulacion de ciudad, agentes, tareas, recursos, eventos, RPG export, handoff y witnesslog.
- Codigo base separado en `src/core`, `src/sim`, `src/render`, `src/rpg`, `src/components` y `src/tests`.
- FibMob y EML ya existen como operadores computacionales/procedurales.
- `Duat-Fibmob-Lab.zip` contiene tambien `.git`, `.local/skills` y material de transporte que no debe adoptarse completo.

## Intake aplicado

- Source: `releases/partner_transportista_wabi_duat_2026-05-19/MEDIOEVO_WABI_DUAT_SOCIEDAD_TECNICA_2026-05-19/Duat-Fibmob-Lab.zip`.
- SHA256 zip principal: `B098F37BA568D6135FFFFF069C8C078ABB00C71C6A0EC15D05E80651AC5EA8F0`.
- SHA256 `files.zip`: `6D7CA1077A14DBEBD01172B210FC5B7D22955FAAF0C2C302475A97419A5F48F4`.
- Curador preflight: `DENIED_OR_SECRET_LIKE_DO_NOT_COPY`, `registered=false`, por lo que se aplico extraccion selectiva local.
- Extraido: `artifacts/duat-city/**`, `lib/api-client-react/**`, `lib/api-spec/**`, `lib/api-zod/**`, `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `tsconfig.base.json`.
- Excluido: `.git/**`, `.local/**`, stores, skills, y cualquier material no necesario para compilar el paquete.

## Baseline

Comandos pedidos:

```powershell
pnpm --filter @workspace/duat-city run test
pnpm --filter @workspace/duat-city run build
pnpm --filter @workspace/duat-city run typecheck
```

Resultado inicial:

- `pnpm` no estaba en PATH; se uso `corepack pnpm`.
- La primera resolucion de dependencias uso cache local (`downloaded 0`) y fallo por `preinstall` POSIX (`sh` no disponible en Windows).
- `corepack pnpm install --ignore-scripts --offline` paso.
- `test` y `build` fallaron por `Cannot find module @rollup/rollup-win32-x64-msvc`; causa: overrides importados excluyen paquetes nativos Windows de Rollup.
- `typecheck` fallo primero por `tsconfig.base.json` faltante; el archivo fue extraido selectivamente desde el zip.

Resultado tras soporte local Windows:

- `corepack pnpm --filter @workspace/duat-city run test`: PASS, 15 suites, 106 tests.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: PASS.
- `corepack pnpm --filter @workspace/duat-city run build`: PASS.
- Workaround local sin red: `node_modules` sincronizado con caches locales para Rollup/esbuild Windows; Tailwind Vite queda opt-in por falta de `lightningcss` Windows local.

## Que no debe tocarse

- No borrar ni reemplazar la simulacion base.
- No convertir en landing page.
- No romper RPG export.
- No activar backend, cloud, deploy, push, pagos, secretos, APIs externas ni MCP real.
- No adoptar `.git`, `.local`, stores o skills del zip.
- No afirmar fisica real, magnetismo o claims teoricos no medidos.

## Mayor R tecnico

- La base importada fue generada en entorno Replit/Linux y trae una configuracion de workspace que excluye binarios Windows de Rollup.
- El estado critico de ciudad se persiste en `localStorage`; debe quedar solo como export/import JSON explicito, manteniendo `localStorage` como maximo para preferencias UI no criticas.
- El motor de agentes actual usa movimiento lineal directo y no bloquea edificios solidos.

## Plan reversible

1. Corregir soporte local Windows sin agregar dependencias nuevas: quitar exclusiones Windows de Rollup en `pnpm-workspace.yaml` solo si la cache local permite instalar el paquete opcional.
2. Mantener el movimiento previo detras de flag y agregar fisica como adaptador.
3. Extender render Canvas por capas sin reemplazar `canvasRenderer.ts`.
4. Agregar Wabi v0.5 design-only como generador de JSON, sin ejecucion.
5. Extender RPG export con perfiles fisicos/graficos sin tocar carriles RPG privados.
6. Cerrar con tests, build, typecheck y handoff JSON local.
