# Agent Message Schema

Implementacion TypeScript:

`C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\types.ts`

```ts
export type AgentId = string;
export type MessageId = string;
export type ChannelId = string;
export type Fingerprint = string;

export type MessagePriority = "P0" | "P1" | "P2" | "P3";
export type MessageStatus =
  | "draft"
  | "queued"
  | "sent"
  | "delivered"
  | "acknowledged"
  | "blocked"
  | "resolved"
  | "archived";

export type MessageKind =
  | "bulletin"
  | "handoff"
  | "task"
  | "question"
  | "answer"
  | "alert"
  | "decision"
  | "artifact"
  | "canon_update"
  | "security_review"
  | "build_report"
  | "test_report";

export interface AgentMessage {
  id: MessageId;
  parent_id?: MessageId;
  thread_id: string;
  channel_id: ChannelId;
  from_agent: AgentId;
  to_agents: AgentId[];
  cc_agents?: AgentId[];
  kind: MessageKind;
  priority: MessagePriority;
  status: MessageStatus;
  title: string;
  body: string;
  summary?: string;
  certeza: string[];
  inferencia: string[];
  incognita: string[];
  bloqueo: string[];
  action_required?: string;
  due_at?: string;
  evidence_refs: string[];
  artifact_refs: string[];
  handoff_fingerprint?: Fingerprint;
  witness_event_ids: string[];
  R_estimado: number;
  Phi_eff?: number;
  prompt_started_at?: string;
  work_delivered_at?: string;
  created_at: string;
  updated_at: string;
  expires_at?: string;
  ack_by: AgentId[];
  hash: string;
  prev_hash?: string;
}

export interface AgentRecord {
  id: AgentId;
  name: string;
  role: string;
  status: "offline" | "idle" | "working" | "blocked" | "reviewing";
  capabilities: string[];
  allowed_channels: ChannelId[];
  current_task_id?: string;
  last_handoff?: Fingerprint;
}

export interface AgentChannel {
  id: ChannelId;
  name: string;
  purpose: string;
  visibility: "system" | "team" | "private";
  allowed_kinds: MessageKind[];
  retention_policy: "ephemeral" | "session" | "project" | "permanent";
}

export interface WitnessEvent {
  id: string;
  actor: AgentId;
  action: string;
  result: string;
  R_before?: number;
  R_after?: number;
  evidence_refs: string[];
  created_at: string;
  prev_hash?: string;
  hash: string;
}
```

## Validaciones necesarias en Run 3

- `channel_id` existe.
- `kind` esta permitido por `AgentChannel.allowed_kinds`.
- `from_agent`, `to_agents`, `cc_agents`, `ack_by` existen.
- `R_estimado` esta entre 0 y 1.
- `Phi_eff`, si existe, esta entre 0 y 1.
- `prompt_started_at`, si existe, registra fecha/hora ISO del momento en que se mando el prompt o se inicio la solicitud.
- `work_delivered_at`, si existe, registra fecha/hora ISO del momento en que el agente entrega el trabajo.
- `summary`, si existe, es el brief humano visible antes del detalle completo.
- `hash` y `prev_hash` forman cadena verificable.
- `evidence_refs` no apuntan a secretos, ZIPs sin revisar ni rutas privadas sin gate.

## Contrato de lectura humana

Todo handoff o bulletin que vaya a ser leido por un humano debe poder renderizar:

- `BRIEF INTELIGENTE`: resumen, estado R, prompt enviado, trabajo entregado y siguiente accion.
- `DETALLE COMPLETO`: estado, cuerpo, certeza, inferencia, incognita, accion, artefactos y fingerprint.
- `Escala R`: `0 verde -> 1 rojo/jamming`; si el medio soporta color, la vista debe usar gradiente verde, amarillo, naranja, rojo.
