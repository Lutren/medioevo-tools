# TEST_REPORT DUAT WEB-FIRST ENGINE 2026-05-20

## Comandos

```txt
npm run typecheck
```

Resultado: PASS.

```txt
npm run build
```

Resultado: PASS. Vite build produjo `dist/public`.

```txt
npm run test -- src/tests/engine.test.ts src/tests/rpgExport.test.ts src/tests/rpgWorldV2.test.ts
```

Resultado: PASS, 3 test files, 20 tests.

```txt
rg -n "Math.random" src
```

Resultado:
- `src/components/ui/sidebar.tsx`: placeholder visual no-core.

```txt
SESSION_FINGERPRINT.json | ConvertFrom-Json
```

Resultado: PASS.

```txt
rg -n -i "<basic credential patterns>" <archivos_tocados>
```

Resultado: sin matches.

## Intentos bloqueados

```txt
pnpm run test src/tests/engine.test.ts
pnpm run typecheck
```

Resultado: FAIL por runner ausente: `pnpm` no reconocido.

## Notas

- El build completo paso despues del parche.
- No se ejecuto benchmark FPS/memoria vivo; queda en cola.
- No se imprimieron secretos.
