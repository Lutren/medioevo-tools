# MESSAGEBUS DURABLE JSONL

Fecha: 2026-05-12

Producto: DUAT Telecom Core

Nombre tecnico: MEDIOEVO MessageBus

Estado: DURABLE_JSONL_LOCAL_VALIDADO

## Modelo append-only

Run 4 agrega una fuente durable local en disco para el MessageBus. El navegador no escribe a disco. La UI `/telecom` sigue usando `localStorage` y export/import browser-side; los scripts Node-only operan el ledger JSONL local.

Ruta principal:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/messagebus/logs/messagebus-main.jsonl`

Regla:

- Append agrega una linea.
- No se sobrescriben entradas existentes.
- IDs duplicados son rechazados.
- Cada entrada apunta al `prevHash` de la entrada anterior.
- El primer registro usa `prevHash: null`.

## Formato JSONL

Cada linea es un envelope:

```json
{
  "schemaVersion": "medioevo.messagebus.jsonl.v1",
  "id": "msg-run4-jsonl-...",
  "channel": "#codex_runs",
  "kind": "build_report",
  "from": "codex_engineer",
  "to": ["human_operator"],
  "createdAt": "2026-05-12T10:09:04.690Z",
  "payload": {},
  "prevHash": null,
  "canonicalData": "...",
  "hash": "sha256-..."
}
```

El `payload` conserva el contrato `AgentMessage` del cliente TypeScript.

## Hash-chain

Implementacion Node-only:

- `scripts/messagebus/lib/hash.mjs`
- Algoritmo: `sha256` de Node `crypto`, solo fuera del bundle React.
- `canonicalData` se calcula excluyendo `hash` y `canonicalData`.
- `prevHash` si participa en la canonicalizacion.

## Replay

Implementacion:

- `scripts/messagebus/lib/replay.mjs`

Reconstruye:

- estado por canal;
- inbox por agente;
- outbox por agente;
- task queue;
- artifact registry;
- replay summary.

## Verificacion

Implementacion:

- `scripts/messagebus/lib/verify-log.mjs`

Checks:

- JSONL syntax;
- schema;
- allowed channels;
- hash-chain;
- append-only continuity;
- duplicate ids;
- timestamps monotonic or warning.

## CLI local

Scripts npm:

- `messagebus:append-sample`
- `messagebus:verify`
- `messagebus:replay`
- `messagebus:export-md`
- `messagebus:stats`

## Diferencia UI vs durable

| Superficie | Persistencia | Uso |
|---|---|---|
| `/telecom` | `localStorage` | Operacion visual local, export JSONL desde browser |
| Node CLI | JSONL en disco | Ledger durable verificable |
| Run 5 MCP | JSONL en disco | Resources read-only |

## Habilitacion MCP read-only

Run 5 puede servir recursos MCP desde JSONL sin tocar el cliente React:

- `messagebus://logs`
- `messagebus://channels`
- `messagebus://agents`
- `messagebus://tasks`
- `messagebus://handoffs`
- `messagebus://witnesslog`

Las tools write siguen bloqueadas por ActionGate.
