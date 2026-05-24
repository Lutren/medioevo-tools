# MESSAGEBUS LOCALSTORAGE TO JSONL MIGRATION

Fecha: 2026-05-13

Estado: DESIGN_READY / NO_IMPORT_EXECUTED

## Objetivo

Migrar historial browser `localStorage` del MessageBus hacia el ledger durable
`02_RUNTIME/messagebus/logs/messagebus-main.jsonl` sin imprimir secretos, sin
mutar produccion automaticamente y sin romper la UI legacy.

## Frontera

- El navegador no escribe directo a disco.
- El ledger principal no se reemplaza por glob ni copia cruda.
- La migracion real requiere ActionGate y respaldo previo.
- Los valores secret-like en `evidence_refs` y `artifact_refs` se redactan antes
  de mostrarse en resources MCP o exports.

## Flujo propuesto

1. Exportar estado browser desde UI como JSON descargable local.
2. Validar schema de `MessageBusState`: agentes, canales, mensajes y
   `witness_events`.
3. Convertir cada mensaje a envelope JSONL con:
   - `schemaVersion=medioevo.messagebus.jsonl.v1`;
   - `id`, `channel`, `kind`, `from`, `to`, `createdAt`;
   - `payload` preservado;
   - `canonicalData`, `prevHash`, `hash`.
4. Convertir `witness_events` a mensajes `kind=decision` o `kind=artifact` solo
   si tienen evidencia suficiente; si no, mantenerlos en reporte de migracion.
5. Ejecutar dry-run contra un ledger temporal.
6. Ejecutar `verifyLog()` / `node scripts\messagebus\verify.mjs` sobre temporal.
7. Ejecutar replay y comparar conteos:
   - total mensajes;
   - canales;
   - P0 abiertos;
   - handoffs;
   - artifacts.
8. Generar reporte con hashes y diferencias.
9. Solo con ActionGate APPROVE local, anexar al ledger principal como append-only
   y guardar rollback.

## Criterios de aceptacion

- `npm test -- src/messagebus` pasa.
- `npm run messagebus:mcp:smoke` pasa.
- `messagebus://health` reporta `hashChain=OK`.
- `messagebus://artifacts`, `messagebus://bulletin/latest` y
  `messagebus://security/p0` no imprimen refs secret-like en claro.
- No hay `mainMessageBusMutation` durante dry-run.

## Bloqueos

- No ejecutar import real sin ActionGate local.
- No imprimir `.env`, token, secret, credential, provider key, `banananana`,
  Gumroad, Stripe, Discord, YouTube, DashScope, Qwen, Aliyun ni OpenAI refs en
  claro.
- No borrar `localStorage` hasta verificar ledger, replay y rollback.

## Siguiente implementacion segura

Crear script dry-run:

```powershell
node scripts\messagebus\migrate-localstorage-export.mjs --input <export.json> --dry-run
```

El script debe escribir solo a `runtime/messagebus_migration_dry_run/` y debe
fallar si detecta refs sensibles no redactadas en el reporte.
