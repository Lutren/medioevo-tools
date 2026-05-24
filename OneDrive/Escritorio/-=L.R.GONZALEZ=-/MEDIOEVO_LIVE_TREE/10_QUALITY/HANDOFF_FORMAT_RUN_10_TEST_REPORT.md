# HANDOFF FORMAT RUN 10 TEST REPORT

Fecha: 2026-05-14T20:15:58-06:00

## Objetivo

Validar formato humano de handoff para DUAT Telecom Core:

- brief inteligente visible antes del detalle;
- `prompt_started_at` y `work_delivered_at` separados;
- escala R `0 verde -> 1 rojo/jamming`;
- dashboard `/telecom` con resumen humano y detalle completo.

## Evidencia local

- `npm test -- src/messagebus`: PASSED, 10 test files, 90 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: PASSED, `ok=true`, resources 10, tools 8.
- `npm run agents:bridge:smoke`: PASSED, `ok=true`, agents 6.
- `npm run actiongate:sandbox:smoke`: PASSED, `status=PASS`, `mainMessageBusMutation=NOT_DETECTED`, production writes false.
- Browser check: `http://127.0.0.1:5173/telecom` contiene `Brief humano`, `Lo importante`, `Prompt enviado`, `Trabajo entregado`, `0 verde`, `1 rojo/jamming` y `Detalle completo`.

## Archivos principales

- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\types.ts`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\service.ts`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\exporters.ts`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\lib\export-md.mjs`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\ui\TelecomCore.tsx`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\styles.css`

## Resultado

PASSED_LOCAL.

El formato queda local y documental. No hubo deploy, push, publicacion, DNS, delete, move ni rename.
