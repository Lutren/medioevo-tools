# Formal Code Insights - 2026-05-08

## Scope

This pass reviewed code-bearing files only as source evidence. No script was executed, imported, installed, copied to runtime or used to change host state.

## Code Candidates

| Source | Decision | Useful pattern | Blockers |
|---|---|---|---|
| `medioevo_agent_core.py` | `CODE_INSIGHT` | Offline control agent with `Observation`, `DOResult`, `Plan`, `GhostSimulation`, `GateDecision`, `AgentOutput`, R/Phi_eff scoring and handoff. | Needs comparison with existing Wabi/Sabi `ActionGate`, `GhostGate`, `safe_executor`, `rollback_store` before reuse. |
| `medioevo_core_v01.py` | `CODE_INSIGHT` | Minimal DO/IOI kernel with `Signal`, `State`, `Task`, `Plan`, `Response`, `CycleMetrics` and `ActionDecision`. | Uses uncalibrated heuristics; should become tests/contracts, not production truth. |
| `Completar04.txt` | `CODE_INSIGHT` | Large mixed source with many function/class blocks. | Must be split before import; likely contains generated snippets. |
| `Completar05.txt` | `CODE_INSIGHT` | EML and runtime-oriented snippets. | Needs line-level extraction and safety review. |
| `Completar06.txt` | `CODE_INSIGHT` | Compact runtime/code ideas around Phi_eff/R. | Needs line-level extraction and tests. |
| `Completar07.txt` | `CODE_INSIGHT` | Agent/runtime snippets and protocol sections. | Needs line-level extraction and tests. |
| `PR11.txt` | `CODE_INSIGHT` | ActionGate-heavy code/protocol source. | Must compare with Wabi/Sabi before new implementation. |
| `medioevo_info_chemistry_v0_2.zip` | `CODE_INSIGHT` | Archive listing shows JSON data plus `architecture_generator.py` and README. | Quarantined archive intake required; no in-place unpack. |
| `banananana.txt` | `PRIVATE_SECRET_CONFIG` | Provider credential/config lane for NVIDIA/NGC; useful only as evidence that Wabi/Sabi/Claudio need secret-safe provider adapters. | Never copy raw content; never commit values; no direct API call without ActionGate. |

## Blocked Execution Sources

| Source | Why blocked | Allowed extraction |
|---|---|---|
| `uno.py` | Changes process priority, calls standby/cache cleaning, can kill browsers, loops forever and touches host process state. | Policy notes for host health gate, never direct execution. |
| `nucleo.txt` | Contains `uno.py` execution transcript and recommends privileged host setup. | Extract only the idea of local host-health observation with explicit ActionGate. |
| `Para materializar este Pipeline Dir.txt` | Writes shell files, runs generated scripts, installs dependencies and starts apps. | Extract as negative example for SafeExecutor/GhostGate requirements. |
| `The Solution deploy_overlord.shThis.txt` | Generates/executes app files, installs packages, uses external API key pattern and proposes shell payload execution. | Extract only requirements for manual confirmation, redaction and sandboxed runner. |

## Safe Contract Deltas

Candidate contracts to compare against existing Wabi/Sabi before any implementation:

| Contract | Source evidence | Existing target to compare |
|---|---|---|
| `ObservationEnvelope` / task observation | `medioevo_agent_core.py`, `medioevo_core_v01.py` | `apps/local/wabi-sabi/wabi_sabi/core/task_spec_planner.py`, `tool_registry.py` |
| `ActionGate` table-driven decision | `medioevo_agent_core.py`, `medioevo_core_v01.py`, `PR11.txt` | `apps/local/wabi-sabi/wabi_sabi/core/browser_gate.py`, `safe_executor.py`, `claim_contract.py` |
| `GhostGate` simulation before action | `medioevo_agent_core.py`, `Completar*` | `apps/local/wabi-sabi/wabi_sabi/core/patch_planner.py`, `rollback_store.py` |
| `Handoff` / state fingerprint | `medioevo_agent_core.py`, `medioevo_core_v01.py` | `apps/local/wabi-sabi/wabi_sabi/core/decision_log.py`, `memory.py` |
| R/Phi_eff scoring | `medioevo_agent_core.py`, `medioevo_core_v01.py`, experiment JSON/CSV | `apps/local/wabi-sabi/wabi_sabi/core/eml.py`, `geodia_math_core.py` |

## Update 2026-05-13

- `medioevo_agent_core.py` and `medioevo_core_v01.py` were converted into
  Wabi/Sabi contract tests, not production imports.
- `Completar04.txt`, `Completar07.txt` and `PR11.txt` remain spec/evidence
  inputs only.
- Evidence: `FORMAL_WABI_CONTRACT_COMPARISON_2026-05-13.md`,
  `tests/test_formal_contract_intake.py`.

## Decision

- No code import.
- No script execution.
- No package install.
- No daemon launch.
- Implemented Wabi/Sabi-safe provider scaffolding: `provider-status`, local `chat`, redaction, cloud adapters blocked by default and Claudio gateway tests.
- Next safe step: write a focused comparison/test plan for `medioevo_agent_core.py` and `medioevo_core_v01.py` against Wabi/Sabi contracts, then extract only non-duplicative interfaces.
