# DIGITAL_INFORMATION_THEORY_UPDATE_MEDIOEVO_v0_1

Status: `PUBLIC_SAFE_THEORY_DRAFT`

Scope: digital information theory for agentic systems.

Boundary: this document is about software agents, language, memory, evidence,
coordination, communication, operational state, and permissioned action. It is
not a theoretical physics document.

## Thesis

MEDIOEVO updates digital information theory for systems where the receiver is
not a passive endpoint but an agent with memory, goals, permissions, tools,
coordination costs, and the ability to act.

Classic information theory gives a strong base:

- source;
- message;
- transmitter;
- channel;
- receiver;
- destination;
- noise;
- encoding;
- redundancy;
- compression;
- capacity.

MEDIOEVO keeps that base but extends the operational model. In agent systems,
the information problem is not only whether a message can be transmitted. The
problem is whether an agent can classify, verify, remember, coordinate, and act
on that message without increasing residue, losing evidence, or crossing an
unsafe boundary.

## This Is Not Theoretical Physics

This document does not claim to update quantum mechanics, relativity,
thermodynamics, spacetime physics, or physical ontology.

It updates digital information theory at the operational layer of agents,
software, language, coordination, memory, evidence, and action.

Any physics analogies are metaphors unless separately formalized and tested in
a physics-specific work. Physics-related material belongs outside this book and
should be marked `OUT_OF_SCOPE_FOR_THIS_BOOK` unless it is clearly labeled as
metaphor.

## Extended Agentic Channel

Classic channel:

```txt
source -> encoder/transmitter -> channel + noise -> receiver/decoder -> destination
```

MEDIOEVO agentic channel:

```txt
source -> message -> channel -> observer state -> claim classification
       -> evidence state -> Source Card -> GhostGate -> ActionGate
       -> action or hold -> WitnessLog -> Handoff -> next observer/session
```

The added layer is not decorative. It is the minimum required for information
to become operational in an agentic environment.

## Why Agentic Information Is Different

An agent does not only receive. It interprets from a state.

An agent has:

- a current memory;
- a task contract;
- permissions and blocked actions;
- tools with different blast radii;
- uncertain or stale evidence;
- coordination obligations;
- reversibility constraints;
- downstream users or agents that must continue the work.

Therefore, an information unit is not complete when it is syntactically
delivered. It is operationally complete only when its claim status, evidence
state, action permission, and handoff state are known.

## Formal Definitions - English

**Information atom**: the smallest operational unit that can be classified,
linked to evidence, acted upon, or handed off. It may be a claim, task,
constraint, observation, decision, or result.

**Observer**: an agent or human-agent session that receives information from a
specific state: memory, task context, permissions, tools, prior evidence, and
current uncertainty.

**Channel**: the medium and protocol through which an information atom moves
between source, observer, tool, agent, user, memory, or handoff.

**Noise**: any factor that reduces correct interpretation or safe action:
uncertainty, ambiguity, contradiction, missing evidence, stale state, excessive
context, permission confusion, or coordination overhead.

**Residue R**: accumulated operational noise that remains after observation,
classification, coordination, and attempted closure.

**Phi_eff**: effective informational efficiency; the ratio between verified
useful output and total coordination cost.

**Claim**: a statement that may be true, false, partial, uncertain, stale, or
out of scope, and therefore requires classification before use.

**Source Card**: a compact evidence anchor describing where a claim came from,
what kind of source it is, when it was captured, its confidence, and any
boundary that limits its use.

**WitnessLog**: an append-only record of observations, decisions, actions,
results, gates, and evidence summaries that makes agent work externally
verifiable without exposing private material.

**GhostGate**: a pre-action planning gate. It allows reading, listing,
searching, inspecting, and proposing, but blocks execution, writes, publication,
network actions, and destructive operations.

**ActionGate**: an execution gate that decides `APPROVE`, `REVIEW`, or `BLOCK`
based on evidence, reversibility, risk, privacy, and scope.

**Handoff**: the minimal sufficient state that lets another agent or session
resume without re-reading everything.

**TaskContract**: the explicit work episode boundary: objective, allowed
actions, blocked actions, evidence requirements, expected output, and closure
criteria.

**Agent protocol**: a repeatable rule set for how agents receive tasks,
classify claims, use tools, coordinate, log evidence, and close work.

**Institutional protocol**: a human-derived governance pattern adapted for
agents, such as TPS, Linux maintainers, Wikipedia, tribunal, guild, laboratory,
or commenda.

## Definiciones formales - Español

**Átomo de información**: la unidad operacional mínima que puede clasificarse,
vincularse a evidencia, usarse para actuar o transferirse por handoff. Puede
ser una afirmación, tarea, restricción, observación, decisión o resultado.

**Observador**: un agente o sesión humano-agente que recibe información desde
un estado específico: memoria, contexto de tarea, permisos, herramientas,
evidencia previa e incertidumbre actual.

**Canal**: el medio y protocolo por el cual un átomo de información se mueve
entre fuente, observador, herramienta, agente, usuario, memoria o handoff.

**Ruido**: cualquier factor que reduce la interpretación correcta o la acción
segura: incertidumbre, ambigüedad, contradicción, evidencia faltante, estado
obsoleto, exceso de contexto, confusión de permisos o costo de coordinación.

**Residuo R**: ruido operacional acumulado que queda después de observar,
clasificar, coordinar e intentar cerrar una tarea.

**Phi_eff**: eficiencia informacional efectiva; relación entre salida útil
verificada y costo total de coordinación.

**Afirmación**: enunciado que puede ser verdadero, falso, parcial, incierto,
obsoleto o fuera de alcance, y por eso debe clasificarse antes de usarse.

**Source Card**: ancla compacta de evidencia que describe de dónde viene una
afirmación, qué tipo de fuente es, cuándo se capturó, su confianza y los
límites de uso.

**WitnessLog**: registro append-only de observaciones, decisiones, acciones,
resultados, gates y resúmenes de evidencia que hace verificable el trabajo de
agentes sin exponer material privado.

**GhostGate**: compuerta de planificación previa a la acción. Permite leer,
listar, buscar, inspeccionar y proponer, pero bloquea ejecución, escrituras,
publicación, red y operaciones destructivas.

**ActionGate**: compuerta de ejecución que decide `APPROVE`, `REVIEW` o
`BLOCK` según evidencia, reversibilidad, riesgo, privacidad y alcance.

**Handoff**: estado mínimo suficiente para que otro agente o sesión continúe
sin releer todo.

**TaskContract**: frontera explícita de un episodio de trabajo: objetivo,
acciones permitidas, acciones bloqueadas, evidencia requerida, salida esperada
y criterios de cierre.

**Protocolo de agente**: reglas repetibles para que agentes reciban tareas,
clasifiquen afirmaciones, usen herramientas, coordinen, registren evidencia y
cierren trabajo.

**Protocolo institucional**: patrón de gobernanza humana adaptado a agentes,
como TPS, mantenedores de Linux, Wikipedia, tribunal, gremio, laboratorio o
commenda.

## Core Formulas

### 1. Residue

```txt
R_total =
  w_u * uncertainty
+ w_c * contradiction
+ w_m * missing_evidence
+ w_a * ambiguity
+ w_s * stale_state
+ w_i * irreversible_risk
+ w_o * coordination_overhead
```

Each term is normalized to `[0, 1]`. Weights depend on the task class. A
publication task weights evidence, privacy, and reversibility higher than a
local read-only analysis task.

### 2. Effective informational efficiency

```txt
Phi_eff = verified_useful_output / total_coordination_cost
```

Where `verified_useful_output` means output that can be traced to evidence,
task closure, or accepted handoff, and `total_coordination_cost` includes
tokens, time, retries, tool calls, clarifications, conflicts, review events,
and rollback burden.

### 3. ActionGate decision

```txt
APPROVE if:
  R <= threshold
  and evidence is sufficient
  and reversibility is sufficient
  and no blocked boundary is touched

REVIEW if:
  evidence is partial
  or reversibility is partial
  or scope is external/legal/publication/payment/provider/channel

BLOCK if:
  concrete technical risk exists
  or secrets/private data exposure is detected
  or destructive action is requested without gate
  or publication without review is detected
```

### 4. Handoff compression

```txt
Handoff = minimal sufficient state for another agent/session
          to resume without re-reading everything
```

Handoff is a continuity codec. It compresses the working state into decisions,
evidence, unresolved items, next action, and boundaries.

## Claim Classification

An agentic information system must classify claims before use:

- `CERTEZA`: directly verified with evidence;
- `INFERENCIA`: reasonable conclusion from evidence, marked as such;
- `INCOGNITA`: not known, not blocking unless it affects action;
- `BLOQUEO`: unsafe, private, destructive, externally consequential, or
  unsupported for the requested use.

This classification is an operational layer, not a metaphysical claim.

## Source Cards

A Source Card is not a full archive. It is a compact evidence anchor:

```txt
source_id:
source_type:
location:
captured_at:
claim_supported:
confidence:
boundary:
hash_or_excerpt:
```

The purpose is traceability without copying private or copyrighted material.

## Gates

GhostGate protects the planning stage. It lets the agent inspect, compare,
search, and propose.

ActionGate protects the execution stage. It separates local reversible action
from external, destructive, private, legal, or publication actions.

In `claudio-agent-runtime`, this is now connected to:

- `ghostgate tools`;
- `ghostgate check`;
- `permissions check`;
- `execute write`;
- `rollback restore`;
- `witness status`.

## WitnessLog

WitnessLog makes agent work observable. It should store summaries and hashes,
not private content. In the current runtime, WitnessLog is JSONL and redacted:

```txt
state_root/witness/witness_log.jsonl
```

It records command, status, ActionGate result, event id, timestamp, and a
redacted result summary.

## Handoff

Handoff prevents operator loss. It is not a memory dump. It is a compressed
continuation artifact:

- current status;
- verified facts;
- inferences;
- unknowns;
- actions taken;
- artifacts;
- next local step.

## Human Institutions as Agent Protocols

MEDIOEVO treats institutions as tested coordination patterns:

- TPS: standard work, visible problems, continuous improvement;
- Linux maintainers: patch review, ownership, maintainership, release gates;
- Wikipedia: citations, neutral tone, revision history, dispute handling;
- tribunal: evidence, claims, burden, adversarial review;
- guild: skill transmission, apprenticeship, quality norms;
- laboratory: hypothesis, experiment, record, replication;
- commenda: scoped risk, delegated agency, profit/loss accounting.

These are not decorative metaphors. They are protocol libraries for agentic
coordination.

## Runtime Connection

Current implementation target:

```txt
packages/open-dev/claudio-agent-runtime
```

Connected concepts:

- `doctor/status`: operational state and future R/Phi reporting;
- `WitnessLog JSONL`: externally verifiable state summaries;
- `memory`: Source Card and claim-memory substrate;
- `task board`: TaskContract and work episode state;
- `skills`: portable agent protocols;
- `GhostGate plan`: pre-action read-only gate;
- `ActionGate execute`: permissioned local write;
- `rollback restore`: reversibility enforcement;
- future `R/Phi budget`: residue and efficiency reporting.

## Provisional Scope

This v0.1 theory update is public-safe and operational. It deliberately avoids:

- private manuscripts;
- internal vaults;
- raw prompts;
- private datasets;
- secrets;
- protected product internals;
- physics claims.

## Next Implementation Step

Implement local `R/Phi` budget from:

- task board;
- memory;
- witness log;
- command outcomes;
- rollback usage;
- missing evidence counts;
- review/block events.

Do this only after the theory and book docs are created and validated.

