# L1 To ObservationEnvelope v0.1

Status: `ADAPTER_CONTRACT`

Adapter: `research/observacionismo-lab/l1_to_envelope.py`

## Flujo

```text
L1 script
  -> parse_l1
  -> ObsBitMachine run
  -> checks / residue / phi_eff
  -> ObservationEnvelope
  -> ActionGate
```

El adaptador no ejecuta acciones. Solo compila, clasifica y propone gates.

## Mapeo De Verbos

| L1 | ObservationEnvelope | ActionGate |
|---|---|---|
| `observar` | Agrega claim operacional sobre fuente/estado observado. | No habilita escritura. |
| `documentar` | Agrega evidencia/artifacto y salida del VM. | Puede apoyar `APPROVE` si hay evidencia declarada. |
| `verificar` | Agrega falsadores/checks y residuo. | Falla de check produce `REVIEW`. |
| `actuar` | Se registra como propuesta de accion. | Escritura -> `REVIEW`; externa -> `BLOCK`. |
| `handoff` | Crea snapshot de transferencia y cierra programa. | Handoff -> `REVIEW` si otro agente debe consumirlo. |

## ObservationEnvelope Emitido

Campos compatibles con `COMMS/schemas/observation-envelope.schema.json`:

```json
{
  "envelope_version": "seto-observation-v1",
  "source_path": "research/observacionismo-lab/examples/document_task.obs",
  "source_kind": "generated_artifact",
  "sha256": "script-sha256",
  "size_bytes": 100,
  "evidence": ["docs/language/OBS_LANGUAGE_V0_1.md"],
  "psi_state": "CERTEZA",
  "claim_level": "operational",
  "falsifiers": ["..."],
  "risk_flags": [],
  "action_gate": "APPROVE",
  "decision": "KEEP_L1_ENVELOPE_LOCAL",
  "fingerprint": "OBS_LANGUAGE_L1_ENVELOPE_V01_2026-05-06_<hash>"
}
```

## ActionGate Derivado

Campos principales:

```json
{
  "schema": "medioevo.seto.action_gate.from_l1.v0_1",
  "decision": "REVIEW",
  "risk_flags": ["write_requires_action_gate"],
  "required_evidence": ["explicit write target approval"],
  "no_delete": true,
  "no_move": true,
  "no_external_action": true,
  "no_write_to_concurrent_lane": true
}
```

## Falsadores v0.1

1. Programa sin `HANDOFF` debe fallar en parser.
2. Pasos despues de `HANDOFF` deben fallar.
3. `VERIFICAR` fallido produce `REVIEW`.
4. Missing evidence produce `REVIEW`.
5. Write intent produce `REVIEW`.
6. External action produce `BLOCK`.
7. Envelope con riesgo externo manipulado produce `BLOCK`.

Implementados en:

```text
research/observacionismo-lab/tests/test_l1_to_envelope.py
```

## Ejemplos

| Archivo | Resultado esperado |
|---|---|
| `examples/document_task.obs` | `APPROVE`, document-only. |
| `examples/gated_patch.obs` | `REVIEW`, write intent local. |
| `examples/handoff.obs` | `REVIEW`, handoff a Wabi-Sabi. |
| `examples/blocked_external_action.obs` | `BLOCK`, accion externa. |
| `examples/missing_evidence.obs` | `REVIEW`, claim sin evidencia. |

## Contrato Para Agente Programador

El agente programador puede leer el packet y preparar un patch, pero no puede
aplicarlo por el simple hecho de que L1 diga `actuar`. Debe verificar:

- `action_gate.decision == APPROVE`;
- no hay `blocked_external_action`;
- no hay `missing_evidence`;
- no hay escritura sobre carril concurrente;
- existen pruebas y post-validacion.

Si cualquiera falla, el agente debe emitir handoff o pedir gate humano.

Para convertir el packet en workpack seco:

```powershell
python research\observacionismo-lab\l1_programmer_workpack.py research\observacionismo-lab\examples\gated_patch.obs --pretty
```

Contrato detallado:

- `docs/language/L1_PROGRAMMER_AGENT_PROTOCOL.md`

Para emitir COMMS local append-only:

```powershell
python research\observacionismo-lab\l1_programmer_workpack.py research\observacionismo-lab\examples\gated_patch.obs --comms-inbox .\COMMS\inbox\claudio-local-agent.jsonl --pretty
```

Esta escritura es opt-in. El mensaje no autoriza ejecucion; solo entrega un
workpack seco al consumidor COMMS.

Para consumir ese inbox sin ejecutar acciones:

```powershell
python research\observacionismo-lab\l1_comms_diff_consumer.py .\COMMS\inbox\claudio-local-agent.jsonl --repo-root . --pretty
```

Contrato detallado:

- `docs/language/L1_COMMS_DIFF_CONSUMER.md`

El resultado es un plan seco con `dry_run=true`, `applied=false`,
`may_apply_patch=false` y `application_gate.status=REVIEW`.
