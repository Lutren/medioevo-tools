# MEDIOEVO: A Digital Information Theory for Agentic Systems

Status: `PUBLIC_SAFE_BOOK_DRAFT_v0_1`

This is a concise public-safe draft. It does not include private manuscripts,
private datasets, secrets, internal prompts, protected runtime material, or
unpublished canon.

## 1. Preface

Information theory gave computation a durable grammar: source, message,
channel, receiver, noise, redundancy, compression, and capacity. That grammar
still matters. It explains why signals degrade, why encoding matters, why
redundancy can be useful, and why every channel has constraints.

Agentic systems add a new practical problem. The receiver is no longer only a
receiver. It is an operator with memory, tools, permissions, goals, uncertainty,
and the ability to act. A software agent can read a message, classify it,
search for evidence, write a file, call a tool, delegate work, publish content,
or stop because the action is unsafe. In that setting, information is not
complete when it arrives. It becomes operational only when the system knows what
the message is, what evidence supports it, what actions are permitted, what
risks remain, and what state must be passed to the next agent or session.

MEDIOEVO is proposed here as a digital information theory extension for
agentic systems. It does not replace classic information theory. It extends the
operational layer around it.

The central idea is simple:

```txt
Information for agents = message + observer state + evidence + permission +
                         reversibility + residue + handoff.
```

This book is short by design. It defines the concepts, gives formulas,
connects them to a minimal runtime, and keeps strong claims out of scope.

## This Is Not Theoretical Physics

This book does not claim to update quantum mechanics, relativity,
thermodynamics, spacetime physics, or physical ontology.

It updates digital information theory at the operational layer of agents,
software, language, coordination, memory, evidence, and action.

Any physics analogies are metaphors unless separately formalized and tested in
a physics-specific work. If a future work uses physics terms, it must define a
separate scope, separate evidence, and separate falsification standards. That
work is not this book.

## 2. From Shannon to Agentic Information

The classic model treats communication as the movement of a message from a
source to a destination through a channel. Noise can corrupt the message.
Encoding, redundancy, and compression can improve delivery. Capacity limits the
amount that can be transmitted.

That model is still essential. A prompt, a file, a log, a user instruction, a
database row, and a tool result are all messages moving through channels. They
can be compressed, corrupted, truncated, duplicated, misunderstood, or delayed.

But agentic systems change the destination. The destination is not merely a
place where the message lands. It is an active observer. It carries state from
previous work. It has tools. It can mutate the environment. It can increase or
decrease risk.

In a passive receiver model, the main question is: did the message arrive?

In an agentic receiver model, the question becomes:

```txt
Can this observer use this information correctly, safely, and continuously?
```

That question requires more fields than the classic channel model:

- observer state;
- claim classification;
- evidence state;
- action permission;
- reversibility;
- residual noise R;
- effective efficiency Phi_eff;
- GhostGate before action;
- ActionGate before execution;
- WitnessLog for external verifiability;
- Source Cards for evidence anchoring;
- Handoff for continuity;
- TaskContract for scoped work episodes.

The extended channel is:

```txt
source -> message -> channel -> observer state -> claim classification
       -> evidence state -> Source Card -> GhostGate -> ActionGate
       -> action or hold -> WitnessLog -> Handoff -> next observer/session
```

## 3. The Observer as Operational Filter

An agent never observes from zero. It observes from a state.

The same message can produce different results depending on what the observer
already knows, what tools it can use, what permissions it has, which files are
in scope, what task is active, and what risks are blocked. This is not a
mystical statement. It is an operational fact.

An observer state includes:

- memory available to the agent;
- current task contract;
- available tools;
- blocked tools;
- local file scope;
- prior evidence;
- unresolved unknowns;
- expected output format;
- handoff obligations.

If the observer state is unclear, the system may act on stale assumptions. If
the tool scope is unclear, the system may perform an unsafe write. If evidence
is unclear, the system may promote inference as fact.

MEDIOEVO treats the observer as a filter between message and action. The filter
does not merely decode. It classifies and gates.

## Formal Definitions

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
searching, inspecting, and proposing, but blocks execution, writes,
publication, network actions, and destructive operations.

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

## 4. R: Informational Residue

Residue is what remains when information has not been fully resolved into
verified state, safe action, or useful closure.

Residue is not simply error. It includes uncertainty, contradiction, missing
evidence, ambiguity, stale state, irreversible risk, and coordination overhead.
An answer may be syntactically fluent and still produce high residue if it
cannot be verified, if it ignores a permission boundary, or if it leaves the
next agent unable to continue.

MEDIOEVO uses R as an operational warning. High R means: stop opening new
features and close the loop. Verify, document, reduce scope, produce handoff,
or ask for review.

The basic formula is:

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

Every term is normalized to `[0, 1]`. The weights depend on the task. A local
read-only analysis can tolerate more uncertainty than an external publication,
payment action, credential change, or destructive cleanup.

R is useful because it converts vague discomfort into a measurable operating
signal.

## 5. Phi_eff: Effective Informational Efficiency

Classic efficiency often measures compression, throughput, or cost. Agentic
efficiency must measure verified usefulness relative to coordination cost.

```txt
Phi_eff = verified_useful_output / total_coordination_cost
```

Verified useful output includes:

- files created or updated with evidence;
- tests that pass;
- decisions recorded with reasons;
- claims linked to Source Cards;
- tasks closed with acceptance criteria;
- handoff that lets another session continue.

Coordination cost includes:

- tokens;
- time;
- tool calls;
- retries;
- clarification loops;
- review events;
- failed commands;
- rollback burden;
- conflict between agents.

Phi_eff is not a universal score. It is a runtime signal. If it drops, the
system should stop producing volume and return to verified closure.

## 6. Claims, Evidence, and Source Cards

Agent systems are claim machines. They summarize, infer, plan, classify, and
recommend. Without a claim layer, they can mix verified facts, guesses, stale
memory, and unsupported assertions.

MEDIOEVO uses four operational categories:

- `CERTEZA`: directly verified with evidence;
- `INFERENCIA`: a reasonable conclusion from evidence, clearly marked;
- `INCOGNITA`: unknown or unverified state;
- `BLOQUEO`: unsafe, private, destructive, externally consequential, or out of
  scope.

A Source Card anchors a claim without copying a full source. It can contain:

```txt
source_id
source_type
location
captured_at
claim_supported
confidence
boundary
hash_or_excerpt
```

The Source Card is small, but it changes the behavior of the system. It forces
the agent to distinguish what it knows from where it knows it.

## 7. GhostGate and ActionGate

GhostGate is the pre-action gate. It is allowed to plan. It is not allowed to
execute. It can read, list, search, inspect, compare, and propose. It cannot
write, publish, run shell commands, push code, use credentials, or trigger
external effects.

ActionGate is the execution gate. It decides whether a concrete action can
proceed.

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

In `claudio-agent-runtime`, this appears as:

- `ghostgate tools`;
- `ghostgate check`;
- `permissions check`;
- `execute write`;
- `rollback restore`.

The current implementation is intentionally limited: local reversible writes
only. Shell, git writes, network actions, publication, scheduler, daemon, and
external channels remain out of scope until separately gated.

## 8. WitnessLog and Verifiable State

Agent work should be observable without exposing private material. WitnessLog
is the append-only state record for that purpose.

It records:

- command;
- event id;
- timestamp;
- ActionGate decision;
- status;
- redacted result summary;
- digest of output, where useful.

WitnessLog does not need to store full private content. In fact, it should not.
It should store enough to verify that the action happened, what gate applied,
and how another operator can audit the path.

This is how agent work becomes externally inspectable without becoming a leak.

## 9. Handoff as Continuity Codec

Handoff is compression for operational continuity.

```txt
Handoff = minimal sufficient state for another agent/session
          to resume without re-reading everything
```

The goal is not to preserve every token. The goal is to preserve the state
needed to continue safely:

- current status;
- verified facts;
- inferences;
- unknowns;
- files touched;
- tests run;
- gates applied;
- next action.

Handoff prevents operator loss. The data persists. The operator does not.

## 10. Human Institutions as Agent Protocols

Human institutions are coordination technologies. MEDIOEVO uses them as a
library of agent protocols.

TPS contributes standard work, visible problems, and improvement loops.
Linux maintainership contributes patch ownership, code review, release
discipline, and trust over time. Wikipedia contributes citation norms, neutral
framing, revision history, and dispute handling. Tribunal logic contributes
claims, evidence, burden, and adversarial review. Guilds contribute skill
transmission and craft standards. Laboratories contribute hypothesis,
experiment, record, and replication. Commenda contributes scoped delegation of
risk, capital, and agency.

The point is practical: agents need institutions, not just prompts.

## 11. DUAT Operator Shell

DUAT Operator Shell is the human/product layer for operating agents. The
technical kernel is `claudio-agent-runtime`.

The shell should expose:

- `doctor/status` reporting;
- permission state;
- GhostGate plan state;
- ActionGate execution state;
- WitnessLog status;
- memory status;
- task board state;
- skills registry;
- rollback state;
- future R/Phi budget.

The shell is not a mystical interface. It is an operational console for
agentic information.

## 12. Minimal Implementation Path

The minimal path is:

1. create a local runtime root;
2. implement permission checks;
3. implement GhostGate plan mode;
4. implement ActionGate execute for local reversible writes;
5. implement rollback;
6. implement WitnessLog JSONL;
7. implement memory summaries;
8. implement task board;
9. implement skills metadata loading;
10. implement handoff;
11. implement R/Phi budget from runtime evidence.

The current kernel already covers the first practical layer. The next step is
local R/Phi calculation from task board, memory, witness log, command outcomes,
rollback usage, missing evidence, and review/block events.

## 13. Falsifiability and Benchmarks

This theory should be tested operationally.

Possible benchmarks:

- Does R decrease after Source Cards are added?
- Does Phi_eff increase after handoff quality improves?
- Do agents make fewer unsafe writes with GhostGate?
- Are review/block decisions consistent across similar tasks?
- Can a second session resume faster from handoff than from raw logs?
- Does WitnessLog allow audit without exposing private content?
- Does rollback reduce irreversible risk?

If these tests fail, the system must be revised. A useful theory of agentic
information must improve work, not only describe it.

## 14. Conclusion

MEDIOEVO extends digital information theory for agents by adding the missing
operational layer: observer state, claim classification, evidence anchoring,
permission, reversibility, residue, efficiency, witness, and handoff.

The result is not theoretical physics. It is a practical theory for software
agents that read, decide, coordinate, and act.

The core principle is:

```txt
Do not maximize output. Maximize verified closure.
```

In agentic systems, information is not complete when it is transmitted. It is
complete when it can be verified, acted on safely, recorded, and handed off.

