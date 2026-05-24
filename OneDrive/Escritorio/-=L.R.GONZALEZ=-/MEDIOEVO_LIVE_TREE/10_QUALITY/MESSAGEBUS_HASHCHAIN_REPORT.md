# MESSAGEBUS HASHCHAIN REPORT

Fecha: 2026-05-12

## Estado

Estado: PASSED_LOCAL.

Hash mode observado en Node: `WEB_CRYPTO_SHA256`.

Fallback implementado: `fnv1a-NOT_CRYPTOGRAPHIC-*`, solo para runtimes sin Web Crypto y tests/local unsupported.

## Implementacion

Archivo: `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\hashChain.ts`

Funciones:

- `canonicalizeMessage(message)`
- `computeMessageHash(message)`
- `verifyMessageHash(message)`
- `verifyHashChain(messages)`
- `appendHash(message, prevHash)`
- `getHashMode()`

## Reglas

- El hash excluye el propio campo `hash`.
- El hash incluye `prev_hash`.
- La canonicalizacion ordena claves de forma estable.
- `verifyHashChain()` valida `prev_hash` contra el hash previo.
- La cadena se evalua en orden de log, no por reordenamiento implicito.

## Tests

| Test | Resultado |
|---|---|
| hash valido pasa | PASSED |
| hash alterado falla | PASSED |
| cadena valida pasa | PASSED |
| cadena rota falla | PASSED |

## Riesgo residual

- `localStorage` no es almacenamiento anti-manipulacion; el hash-chain detecta alteraciones si se valida, pero no impide escritura local manual.
- La persistencia durable debe pasar a JSONL/SQLite con backups y verificacion de import/export.
