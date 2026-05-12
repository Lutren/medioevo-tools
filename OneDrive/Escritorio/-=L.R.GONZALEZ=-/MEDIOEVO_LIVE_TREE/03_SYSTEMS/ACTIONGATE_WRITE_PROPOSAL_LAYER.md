# ACTIONGATE WRITE PROPOSAL LAYER

Fecha: 2026-05-12

Estado: VALIDADO_LOCAL_PROPOSAL_ONLY

## Proposito

ActionGate Run 7 crea una capa local donde agentes pueden proponer acciones de escritura, modificacion o publicacion sin ejecutarlas.

La regla central es: propuesta verificable si; accion real no.

## Implementacion

Ruta Node-only:

- `scripts/actiongate/actiongate-smoke.mjs`
- `scripts/actiongate/lib/actionProposalSchema.mjs`
- `scripts/actiongate/lib/actionProposalBuilder.mjs`
- `scripts/actiongate/lib/actionProposalValidator.mjs`
- `scripts/actiongate/lib/actionProposalSeal.mjs`
- `scripts/actiongate/lib/actionApprovalSimulator.mjs`
- `scripts/actiongate/lib/actionExecutionPlan.mjs`
- `scripts/actiongate/lib/actionGatePolicy.mjs`
- `scripts/actiongate/lib/actionGateLedger.mjs`
- `scripts/actiongate/lib/actionGateHealth.mjs`

Fixtures:

- `valid-append-message.proposal.json`
- `valid-create-task.proposal.json`
- `valid-update-handoff.proposal.json`
- `valid-publish-release.proposal.json`
- `rejected-delete.proposal.json`
- `blocked-deploy.proposal.json`
- `tampered.proposal.json`

## Proposal schema

Schema version: `actiongate.proposal.v1`.

Campos principales:

- `proposalId`
- `schemaVersion`
- `type`
- `title`
- `description`
- `proposedByAgent`
- `targetSystem`
- `riskLevel`
- `requiresOperatorApproval`
- `proposedAction`
- `expectedEffect`
- `forbiddenIf`
- `requiredEvidence`
- `evidence`
- `preconditions`
- `postconditions`
- `testPlan`
- `rollbackPlan`
- `createdAt`
- `expiresAt`
- `status`
- `prevProposalHash`
- `proposalHash`
- `seal`

Tipos soportados:

- `append_message`
- `create_task`
- `update_handoff`
- `publish_release`
- `modify_file`
- `delete_or_move`

`delete_or_move` existe para quedar bloqueado por defecto.

## Proposal seal

Modulo: `actionProposalSeal.mjs`.

El seal es un hash local de integridad basado en canonical JSON + SHA-256.

Campos:

- `canonicalPayloadHash`
- `proposalHash`
- `sealedAt`
- `sealedBy: actiongate-local`
- `sealAlgorithm: sha256-canonical-json`
- `seal`

No usa secretos. No crea claves privadas. No es una firma criptografica de identidad. Es un seal local de integridad para detectar tampering.

`verifySeal()` falla si cambia cualquier campo relevante del payload sellado.

## Policy

Modulo: `actionGatePolicy.mjs`.

Resultados:

- `ALLOW_PROPOSAL`
- `REQUIRE_OPERATOR_APPROVAL`
- `BLOCK`

Permitido como propuesta no ejecutable:

- `append_message`
- `create_task`
- `update_handoff`
- `publish_release`
- `modify_file`

Bloqueado por defecto:

- `delete`
- `move`
- `rename`
- `force_push`
- `deploy_without_gate`
- `publish_without_gate`
- `print_secret`
- `modify_dns`
- `extract_private_zip`
- `write_messagebus_without_approval`
- `external_network_write`
- `credential_creation`
- `destructive_shell`

## Approval simulator

Modulo: `actionApprovalSimulator.mjs`.

Decisiones simuladas:

- `approve`
- `reject`
- `block`

Salida:

- `decisionId`
- `proposalId`
- `decision`
- `decidedAt`
- `decidedBy: operator-simulator`
- `reason`
- `decisionHash`
- `resultingStatus`
- `actionExecuted: false`

El simulador no ejecuta acciones. Si la politica bloquea o el seal falla, la decision resultante queda `blocked`.

## Execution plan inerte

Modulo: `actionExecutionPlan.mjs`.

El plan declara:

- `wouldExecute: false`
- `commandsPreview`
- `filesAffectedPreview`
- `messagebusMutationPreview`
- `requiredApprovals`
- `requiredChecks`
- `stopConditions`
- `rollbackPlan`
- `executionStatus: not_executed`

Nunca ejecuta comandos. Nunca escribe al MessageBus principal.

## Ledger separado

Ledger:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/proposals/actiongate-proposals.jsonl`

Propiedades:

- JSONL separado del MessageBus principal.
- Hash-chain propio.
- Verificador propio.
- Reconstruye propuestas pending, approved, rejected, blocked y execution plans simulados.

Estado smoke Run 7:

- `totalEntries=8`
- `lastHash=sha256-5f2251ce964da357f04c3062d668e27f1d8d96217ec7b60bf30f9098de97a7b5`
- `pending=2`
- `approved=1`
- `rejected=1`
- `blocked=1`
- `simulatedExecutionPlans=1`

## Integracion Agent Bridge

`scripts/agents/lib/handoffSimulator.mjs` ahora agrega:

- `actionGate.mode`
- `actionGate.proposal`
- `actionGate.execution: disabled`

Ejemplos:

- `append a new handoff message` -> `append_message`
- `deploy to medioevo.space` -> `publish_release`
- `delete old zip files` -> `delete_or_move` bloqueado
- `update UI file` -> `modify_file`
- `create next task for Canon Auditor` -> `create_task`

## UI /telecom

`src/ui/TelecomCore.tsx` muestra:

- ActionGate Layer: READY
- Mode: proposal-only
- Write execution: disabled
- Operator approval: simulated
- Proposal types
- Proposal ledger separado
- Main MessageBus mutation disabled
- Last smoke PASS
- Next: operator-approved execution sandbox

React no importa `fs`, `path`, `crypto`, MCP SDK ni scripts Node-only.

## Que NO hace todavia

- No ejecuta propuestas.
- No aplica patches.
- No escribe al MessageBus principal.
- No publica.
- No hace push.
- No deploya.
- No borra, mueve ni renombra.
- No toca DNS.
- No crea credenciales.
- No toca Supabase/backend externo.

## Preparacion Run 8

Run 8 debe crear un sandbox de ejecucion aprobado por operador:

- dry-run executor;
- approval token manual local;
- ejecucion limitada a propuestas low-risk;
- no deploy/delete/move/DNS;
- tests de ejecucion segura;
- evidencia de rollback antes de permitir cualquier accion real.
