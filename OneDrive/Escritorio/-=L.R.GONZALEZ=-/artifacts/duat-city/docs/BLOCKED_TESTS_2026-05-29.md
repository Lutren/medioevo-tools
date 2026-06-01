# BLOCKED_TESTS — 2026-05-29

## Bloqueo Técnico

Tests y build de `duat-city` no pueden ejecutarse en el entorno Windows actual.

## Causa Raíz

El monorepo fue instalado originalmente en Linux/WSL (OneDrive compartido). Los artefactos nativos de Rollup para Windows no fueron descargados.

## Síntomas

- `npx vitest run` → `Cannot find module @rollup/rollup-win32-x64-msvc`
- `npm test` → `Unsupported URL Type "catalog:"` (workspace usa pnpm catalogs)
- `pnpm install --no-frozen-lockfile` → `sh: command not found` (script `preinstall` bloquea en Windows)

## Solución Requerida (REVISIÓN)

1. Reinstalar dependencias nativas:
   ```powershell
   cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
   # Opción A: Usar Git Bash/MSYS2 para tener `sh` disponible
   # Opción B: Desactivar temporalmente el script preinstall y forzar plataforma
   pnpm install --no-frozen-lockfile --platform=win32 --arch=x64
   ```

2. Alternativa sin red: Copiar artefacto desde instalación Windows existente (otra máquina).

## Estado del Código

- Código fuente completo disponible y sin modificar.
- Tests preparados en `src/tests/*`.
- Build/typecheck pendientes de validación tras resolver dependencias.
