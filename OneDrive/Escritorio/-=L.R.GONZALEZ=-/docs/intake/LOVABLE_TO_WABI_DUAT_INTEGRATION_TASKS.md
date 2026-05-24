# Lovable To Wabi/Duat Integration Tasks

Fecha: 2026-05-10

## Objetivo

Convertir los tres ZIPs Lovable de `Formal` en tecnologia util sin importar proyectos crudos, sin usar `.env`, sin publicar y sin mezclar mock UI con runtime real.

## Regla de integracion

No copiar proyecto completo. Integrar por contrato:

1. extraer concepto;
2. mapear a ruta canonica;
3. escribir test;
4. implementar minimo;
5. generar witness/handoff.

## P0 - Bloqueos y frontera

ActionGate:

- `BLOCK`: `.env`, `VITE_SUPABASE_PUBLISHABLE_KEY`, `VITE_SUPABASE_URL`, `src/integrations/supabase/client.ts`.
- `BLOCK`: publicar los ZIPs o copiarlos a `packages/open-dev`.
- `REVIEW`: cualquier extraccion de codigo TSX propia hacia apps activas.
- `APPROVE`: crear specs, tests y adaptadores locales sin secretos.

## P1 - Primer modulo a integrar

Nombre: `ActionGate approval packet`

Destino probable:

- `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi`

Fuente Lovable:

- `lovable_duat_console_f60723f6`: `src/components/duat/ApproveDialog.tsx`
- `lovable_duat_console_f60723f6`: `src/hooks/duat/useDuat.ts`
- `lovable_claudio_surface_dff2f093`: `src/components/claudio/ActionGate.tsx`

Comportamiento esperado:

- Recibe un `TaskPacket` o comando.
- Clasifica accion como `APPROVE`, `REVIEW` o `BLOCK`.
- Si requiere apply/execute, produce `pending_approval=true`.
- Antes de ejecutar, exige confirmacion explicita.
- En dry-run, genera witness con hash y `next_action`.

Test minimo:

- accion lectura local -> `APPROVE`;
- patch reversible con evidencia -> `REVIEW` o `APPROVE_MONITORED` segun politica vigente;
- delete/publish/secret/env -> `BLOCK`;
- todo resultado produce artifact path o razon.

## P2 - Segundo modulo

Nombre: `Duat command console state model`

Destino probable:

- Wabi/Sabi runtime local o Mission Control interno.

Fuente Lovable:

- `lovable_duat_console_f60723f6`: `src/hooks/duat/useDuat.ts`
- `lovable_duat_console_f60723f6`: `src/lib/duat/types.ts`
- `lovable_duat_console_f60723f6`: `src/lib/duat/mock.ts`

Port recomendado:

- No portar Zustand directo al backend.
- Convertir a schema Python/JSON:
  - `AgentStatus`
  - `InventoryItem`
  - `ChatMessage`
  - `ChatBlock`
  - `PatchPlan`
  - `WitnessRow`
  - `Backup`
- Mapear comandos:
  - `scan`
  - `plan`
  - `verify`
  - `handoff`
  - `status`
  - `approve`
  - `rollback`

## P3 - Tercer modulo

Nombre: `Forge deterministic specs`

Fuente Lovable:

- `lovable_forge_surface_15e48d05`: `src/lib/psi-math.ts`
- `lovable_forge_surface_15e48d05`: `src/lib/oe-runtime.ts`
- `lovable_forge_surface_15e48d05`: `src/test/psi-math.test.ts`
- `lovable_forge_surface_15e48d05`: `src/test/oe-runtime.test.ts`

Destino probable:

- `packages/open-dev/obsai-core` si es public-safe.
- `apps/local/wabi-sabi` si queda como runtime interno.

Cierre requerido antes de portar:

- Resolver variantes `J_c=0.65` vs `J_C=0.85`.
- Verificar si `PRE_JAMMING` / `JAMMING_TEMPRANO` existen en el tipo canonico del destino.
- Decidir si `ActionGate` permite `APPROVE_MONITORED` o solo `APPROVE/REVIEW/BLOCK`.
- Mantener formulas como parametrizables.

## P4 - UI interna

Nombre: `Mission Control Duat panels`

Fuente Lovable:

- `src/components/duat/StatusBar.tsx`
- `src/components/duat/ChatPanel.tsx`
- `src/components/duat/VisualizerPanel.tsx`
- `src/components/forge/duat/DuatCity.tsx`

Destino probable:

- app interna Claudio/Mission Control, no public package.

Condicion:

- UI solo debe leer runtime real.
- Si un dato viene de mock, mostrar `MOCK`.
- Si una accion no tiene backend, mostrar `NO_BACKEND_CONNECTED`.

## P5 - Public-safe extraction

Se puede usar de forma publica:

- lenguaje de "evidence before action";
- diagramas de pipeline;
- copy bajo en claims;
- prompts sanitizados;
- screenshots si no muestran secretos/rutas privadas.

No se puede usar publicamente:

- Supabase config;
- corpus privado;
- formulas internas no decididas;
- claims de determinismo total;
- runtime Claudio/Wabi privado;
- GEODIA interno.

## Done criteria

- Ficha intake existe.
- JSON inventory existe.
- Task packet existe.
- Secret material queda bloqueado.
- Primer modulo integrado tiene test local.
- Handoff actualizado con hash y proxima accion.

