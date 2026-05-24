# MEDIOEVO_DIGITAL_INFORMATION_THEORY_BOOK_PLAN_v0_1

Status: `PUBLIC_SAFE_BOOK_PLAN`

English title: **MEDIOEVO: A Digital Information Theory for Agentic Systems**

Spanish title: **MEDIOEVO: Una teoría de información digital para sistemas agentes**

Chinese version: planned, not generated in v0.1.

## Boundary

This book is about digital information theory, communication, computation,
language, agents, coordination, evidence, memory, state, permissions, and
handoff.

It is not a theoretical physics book. Physics-related claims are
`OUT_OF_SCOPE_FOR_THIS_BOOK` unless clearly labeled as metaphor.

## Public-Safe Policy

The book must not include:

- private manuscripts;
- unpublished protected book material;
- internal vault content;
- private datasets;
- secrets;
- raw internal prompts;
- private runtime details;
- RPG/TCG or protected lore.

It may include:

- public-safe operational theory;
- high-level definitions;
- formulas;
- implementation connections to `claudio-agent-runtime`;
- institutional protocol analogies;
- examples that do not expose protected content.

## Target Length

Maximum: 70 pages equivalent.

Approximation: 1 page = 450 English words.

Absolute maximum: 31,500 English words per book file.

Target v0.1: concise stabilization draft, well below the maximum.

## Required Structure

1. Preface
2. From Shannon to Agentic Information
3. The Observer as Operational Filter
4. R: Informational Residue
5. Phi_eff: Effective Informational Efficiency
6. Claims, Evidence, and Source Cards
7. GhostGate and ActionGate
8. WitnessLog and Verifiable State
9. Handoff as Continuity Codec
10. Human Institutions as Agent Protocols
11. DUAT Operator Shell
12. Minimal Implementation Path
13. Falsifiability and Benchmarks
14. Conclusion

Required inserted section:

- `This Is Not Theoretical Physics`

The section may appear after the preface or near the end, but it must be
present exactly under that title.

## Core Definitions

Both English and Spanish versions must define:

- Information atom / Átomo de información
- Observer / Observador
- Channel / Canal
- Noise / Ruido
- Residue R / Residuo R
- Phi_eff
- Claim / Afirmación
- Source Card
- WitnessLog
- GhostGate
- ActionGate
- Handoff
- TaskContract
- Agent protocol / Protocolo de agente
- Institutional protocol / Protocolo institucional

## Required Formulas

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

```txt
Phi_eff = verified_useful_output / total_coordination_cost
```

ActionGate:

```txt
APPROVE if R <= threshold and reversibility/evidence are sufficient.
REVIEW if evidence or reversibility is partial.
BLOCK if concrete technical risk, secrets/private data exposure,
destructive action, or publication without review is detected.
```

Handoff:

```txt
Handoff = minimal sufficient state for another agent/session
          to resume without re-reading everything.
```

## Implementation Connection

The book must connect the theory to:

- `claudio-agent-runtime`;
- DUAT Operator Shell;
- `doctor/status` reporting;
- WitnessLog JSONL;
- memory;
- task board;
- skills;
- GhostGate plan;
- ActionGate execute;
- rollback restore;
- future R/Phi budget.

## Versioning

- English v0.1: generated now.
- Spanish v0.1: generated now.
- Chinese v0.1: `PLANNED_NOT_GENERATED`.

## Next Step After Book

Implement local R/Phi budget from task board, memory, witness log, command
outcomes, rollback usage, missing evidence counts, and review/block events.

