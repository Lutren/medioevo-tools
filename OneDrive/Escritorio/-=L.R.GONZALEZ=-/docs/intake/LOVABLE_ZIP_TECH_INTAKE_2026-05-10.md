# Lovable ZIP Tech Intake 2026-05-10

## Estado

Tres ZIPs de `Formal` fueron revisados como intake, sin ejecutar codigo, sin instalar dependencias, sin extraer proyectos completos a paquetes publicos y sin modificar los ZIPs originales.

ActionGate:

- `APPROVE`: lectura local, hashes, inventario, source map y reporte.
- `REVIEW`: extraer codigo puntual hacia Wabi/Sabi, Claudio o paquetes open-dev.
- `BLOCK`: copiar `.env`, publicar ZIPs crudos, hacer push/deploy, o convertir mocks en claims publicos.

## Fuentes

| id | ruta | SHA256 | archivos | decision |
|---|---|---:|---:|---|
| `lovable_claudio_surface_dff2f093` | `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\lovable-project-dff2f093-e843-43ad-94f5-91f91f8cec15-2026-05-10.zip` | `E2753462500D0EE8840FACCCD39AF77ABCDA889F50795A79CA6D508CC32A4E21` | 86 | `KEEP_REVIEW` |
| `lovable_forge_surface_15e48d05` | `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\lovable-project-15e48d05-7be7-4ec9-ab77-5af7c665fb3c-2026-05-10.zip` | `48350CBB474ECD7A3DC392EF0E591CF4073E9144343E356A21F6404A83A7BBEC` | 159 | `PRIVATE_REVIEW` |
| `lovable_duat_console_f60723f6` | `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\lovable-project-f60723f6-2a07-4b63-9cd8-1c1734b15597-2026-05-10.zip` | `9CC67E39166ABDA3B99770CFD4D3498B9B7B4BD2229A8D449C7E5D2D5FA8D7A5` | 87 | `KEEP_REVIEW` |

Preflight de curador: los tres retornaron `NEEDS_FICHA_BEFORE_USE`.

## Hallazgos utiles

### 1. Claudio Surface

Rol probable: landing/shell visual para agente local de codigo.

Util para integrar:

- Pipeline visual: `SCAN -> GRAPH -> INTENT -> PATCH -> VERIFY -> GATE -> WITNESS -> HANDOFF`.
- Vocabulario correcto para el producto: `ActionGate`, `WitnessLog`, `Fingerprint`, `handoff`.
- Copy tecnico public-safe si se baja el claim: local-first, evidencia antes de accion, cambios minimos, logs encadenados.
- Componentes propios relevantes:
  - `src/components/claudio/ActionGate.tsx`
  - `src/components/claudio/StagePanels.tsx`
  - `src/components/claudio/WitnessLog.tsx`
  - `src/components/claudio/Fingerprint.tsx`
  - `src/components/claudio/Principles.tsx`

No integrar directo:

- Claim fuerte de parche determinista byte-identico sin backend real que lo demuestre.
- Componentes shadcn genericos.

### 2. Forge Surface

Rol probable: tablero "Agent Forge / Neurostate Habitat" para prompts, agentes, codigo, blueprints, claims, DUAT memory y handoff.

Util para integrar:

- Domain model de artefactos: `Agent`, `PromptArtifact`, `CodeArtifact`, `AppBlueprint`, `Claim`, `Handoff`, `ProjectNode`, `GateResult`.
- Motores deterministas que conviene convertir en specs/tests antes de copiar:
  - `src/lib/agentEngine.ts`
  - `src/lib/appBlueprintEngine.ts`
  - `src/lib/codeEngine.ts`
  - `src/lib/duatMemory.ts`
  - `src/lib/epistemic.ts`
  - `src/lib/gates.ts`
  - `src/lib/handoff.ts`
  - `src/lib/psi-math.ts`
  - `src/lib/oe-runtime.ts`
- Tests utiles:
  - `src/test/psi-math.test.ts`
  - `src/test/oe-runtime.test.ts`
- Visualizacion interna:
  - `src/components/forge/duat/DuatCity.tsx`
  - `src/components/forge/instruments/*`

Riesgo:

- Contiene `.env` con `VITE_SUPABASE_PROJECT_ID`, `VITE_SUPABASE_PUBLISHABLE_KEY`, `VITE_SUPABASE_URL`.
- Contiene `src/integrations/supabase/client.ts`.
- No copiar estos archivos a ningun carril publico o comercial hasta revisar credenciales, privacidad, tenancy y rotacion.

### 3. DUAT Console

Rol probable: WebUI local para un agente DUAT/Claudio determinista.

Util para integrar:

- `useDuat` como prototipo de store operativo: chat, comandos, planes, backups, witness, handoff, approve/rollback.
- Comandos de UX: `scan`, `plan`, `verify`, `handoff`, `status`, `approve`.
- `ApproveDialog` como patron correcto: confirmacion explicita antes de aplicar parche.
- `VisualizerPanel` como pantalla util: preview, diff, graph, test, witness, handoff.
- `StatusBar` para `R`, `Phi_eff`, `J_c`, regimen y fingerprint.

No integrar directo:

- Estado mock como verdad runtime.
- Reset destructivo de `localStorage` sin ActionGate.
- Texto de "sin nube" si el runtime real permite cloud opt-in.

## Diferencias de formula que requieren cierre

Hay dos variantes:

- `src/lib/psi-math.ts`: `J_c = 0.65`, `nu = 0.85`, `Phi_0 = 1.0`.
- `src/lib/medioevoCore.ts`: `J_C = 0.85`, `NU = 1.0`.

Decision recomendada:

- No elegir por fecha ni por Lovable.
- Comparar contra canon `MEDIOEVO_CORPUS_UNIFICADO` y paquetes existentes.
- Si se integra a Wabi/Sabi, hacer un adaptador con `params` explicitos y tests que documenten ambos regimenes.

## Plan de integracion

P0 - Registro y frontera:

- Mantener los ZIPs en `Formal` como fuente original.
- Registrar esta ficha en `SOURCE_INTAKE_REGISTER.md`.
- Bloquear `.env` y Supabase hasta revision.

P1 - Especificacion antes de codigo:

- Crear una tarea interna `lovable-to-wabi-duat`.
- Traducir `DUAT Console` a un spec de Mission Control: rutas, estado, comandos, ActionGate y evidencia.
- Convertir `psi-math.ts` y `oe-runtime.ts` en pruebas comparativas contra el nucleo canonico actual.

P2 - Integracion tecnica:

- Si se toca Wabi/Sabi, integrar solo patrones:
  - `wabi status` -> panel StatusBar.
  - `wabi task` -> ChatPanel.
  - `ActionGate` -> ApproveDialog.
  - logs/handoff -> VisualizerPanel tabs.
- No copiar el proyecto Lovable entero.

P3 - Superficie publica segura:

- Usar `Claudio Surface` como inspiracion de copy/landing.
- Reescribir claims a bajo riesgo: "helps make agent work auditable" en vez de "same input, same patch every time" salvo prueba reproducible.

## Source map minimo

| concepto | fuente | miembro | lineas aprox | estado |
|---|---|---|---:|---|
| ActionGate UI/policy | `dff2f093` | `src/components/claudio/ActionGate.tsx` | 1-48 | `CERTEZA` |
| Pipeline scan/graph/intent/patch/verify/gate/witness/handoff | `dff2f093` | `src/components/claudio/StagePanels.tsx` | 1-107 | `CERTEZA` |
| Witness log visual | `dff2f093` | `src/components/claudio/WitnessLog.tsx` | 1-43 | `CERTEZA` |
| Phi_eff, H_eff, EML y score observacionista | `15e48d05` | `src/lib/psi-math.ts` | 7-138 | `CERTEZA` |
| ResidueScorer, RegimeAutomaton, ActionGate, GhostGate | `15e48d05` | `src/lib/oe-runtime.ts` | 7-162 | `CERTEZA` |
| Gate simple para consola Wabi | `15e48d05` | `src/lib/gates.ts` | 5-45 | `CERTEZA` |
| Handoff markdown | `15e48d05` | `src/lib/handoff.ts` | 4-55 | `CERTEZA` |
| Store DUAT artefactos | `15e48d05` | `src/store/useDuatStore.ts` | 12-83 | `CERTEZA` |
| Supabase material | `15e48d05` | `.env`, `src/integrations/supabase/client.ts` | all | `BLOQUEO` |
| DUAT command/runtime mock | `f60723f6` | `src/hooks/duat/useDuat.ts` | 10-239 | `CERTEZA` |
| Explicit patch approval | `f60723f6` | `src/components/duat/ApproveDialog.tsx` | 3-43 | `CERTEZA` |
| DUAT visual tabs | `f60723f6` | `src/components/duat/VisualizerPanel.tsx` | 6-264 | `CERTEZA` |

## Decision

- `KEEP_REVIEW`: los tres ZIPs son fuentes utiles.
- `INTEGRATE_SELECTIVELY`: patrones, formulas parametrizadas, tests y UI flows.
- `DO_NOT_VENDOR`: no copiar scaffolding Lovable completo.
- `BLOCK_COPY`: `.env`, Supabase config, claves publicables/JWT-like, cualquier credential material.

## Proxima accion verificable

Crear un spec interno `LOVABLE_TO_WABI_DUAT_INTEGRATION_TASKS.md` y luego implementar solo una pieza pequena: `ActionGate approval packet` en Wabi/Sabi, con test que bloquee acciones destructivas y genere witness/handoff.
