# CODEX_CHANGELOG_v0_5

## Added

- `src/physics/*`: motor fisico 2D ligero, spatial hash, colisiones, integrador, metricas y adaptador de agentes.
- `src/graphics/*`: budget grafico determinista, sparse chunks, FibMob procedural, particulas y SDF helpers.
- `src/render/lod-controller-v2.ts` y `src/render/renderAdapter.ts`.
- `src/wabi/*`: bridge Wabi MCP v0.5 design-only.
- `src/components/WabiPanel.tsx`.
- Tests v0.5 para fisica, adaptador, graphics budget, Wabi bridge, RPG profiles, persistencia e integracion 1000 ticks/50 agentes.

## Modified

- `src/sim/engine.ts`: opcion `enableAgentPhysics` sin romper default previo.
- `src/core/types.ts`: metricas opcionales de fisica/graficos en `CityState`.
- `src/core/persistence.ts`: estado critico ya no se guarda en `localStorage`.
- `src/App.tsx`, `Toolbar.tsx`, `MainCanvas.tsx`, `OSITPanel.tsx`: toggles/paneles/metricas.
- `src/rpg/*`: perfiles fisicos/graficos y quest hooks.
- `vite.config.ts`: build local sin `PORT/BASE_PATH`, Tailwind Vite opt-in.
- `package.json`: Vite fijado a 5.4.21 para compatibilidad Windows local; `dev/serve` ahora usan `127.0.0.1`.

## Tests

Resultado final de esta sesion:

```powershell
corepack pnpm --filter @workspace/duat-city run test
# 15 test files passed, 106 tests passed

corepack pnpm --filter @workspace/duat-city run typecheck
# passed

corepack pnpm --filter @workspace/duat-city run build
# passed, dist/public generated

Dev server local:

```text
http://127.0.0.1:18519/duat-city/
```
```

## Risks

- `node_modules` requirio sincronizar dependencias nativas Windows desde caches locales previas: Rollup 4.24 y esbuild 0.27.4.
- Tailwind Vite queda opt-in por falta de `lightningcss.win32-x64-msvc` local; la app usa `styles.css` propio para la experiencia DUAT.
- No hay benchmark real de FPS; solo smoke funcional y metricas deterministas.

## Next Steps

- Playtest local con Browser si se arranca dev server.
- Benchmark de render con 100 agentes y debug overlays.
- A* o flow fields si el layout de caminos se vuelve una regla central.
