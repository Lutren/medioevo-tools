# PSI / Wabi-Sabi Tech Intake - 2026-05-07

## Scope

Request: analyze selected PSI/CEREBRO sources for technology not yet implemented and verify whether Wabi/Sabi has the required pieces to behave like a local-first coding agent comparable in workflow to Claude Code, Codex CLI, Cursor Agent, Copilot Workspace or OpenCode/OpenClaw.

ActionGate: local read, selective extraction, no publication, no bulk extraction, no secret exposure, no private game/TCG touch.

## Sources Read

| Source | SHA256 | Intake decision |
|---|---|---|
| `-=CEREBRO=-\-=PSI=-\ReplitExport-lutren.tar.gz` | `CCAC616E3076026284B3E3B5AD25E331FB66340D4ED992831AD5D8059E9AABE2` | `UNKNOWN_REVIEW_REQUIRED`; read as dirty Replit export, no bulk import |
| `-=CEREBRO=-\-=PSI=-\Proyecto MEDIOEVO — Documento Maestro Unificado TUIP-Σ OSIT.docx` | `6D0AD2AE4C728D161EB80967EDE647ECC1C9A4B075C80E65CA5FBC58BD476CCA` | canon/master reference; selective operational extraction only |
| `-=CEREBRO=-\-=PSI=-\escaner sigiloso.txt` | `0C7CDDAA915D42C43D2303583A3E0B737BEEB53A54F574EE382AEFFD371E3D4E` | `BLOCK` for implementation; contains stealth network scanning pattern |
| `-=CEREBRO=-\-=PSI=-\Actúa como AGENTE MISSION CONTROL.txt` | `A12446FC68DF56C5DEF5C87EA51DAA01667928399928B5C233C352B2DE3D903D` | useful local orchestration spec; no dangerous automation |
| `-=CEREBRO=-\-=PSI=-\He analizado con lupa las matemátic.txt` | `0AE66E6A85F16BF4A0A80D9BF0C53B91A26220F6A855065B74F8C318CF25A7CC` | useful math/runtime caution source; research claims remain gated |

Note: the path provided by the user used two spaces before `Documento` and omitted the em dash. The actual file on disk is `Proyecto MEDIOEVO — Documento Maestro Unificado TUIP-Σ OSIT.docx`.

## High-Signal Technology Found

### Already Implemented or Partially Present in Wabi/Sabi

- CLI routing, local agents, memory JSONL, ObservationEnvelope, ActionGate and e2e smoke path exist in `apps/local/wabi-sabi`.
- Provider orchestration existed but previously treated Ollama/Qwen as optional instead of primary.
- COMMS/decision/workpack surfaces exist as local artifacts and are gate-bound.
- Local coding-agent posture exists as scoped workpacks and dry-run/patch flows, but should not be claimed as unrestricted autonomy.

### Gaps Closed in This Pass

- `BASE_MODEL` / `MODEL_ENDPOINT` runtime contract is now represented by Wabi/Sabi provider status.
- Default local provider order now becomes `ollama, codex, dry-run` when the installed base model is available.
- Default base model resolves to `BASE_MODEL`, `WABI_BASE_MODEL`, `WABI_OLLAMA_BASE_MODEL`, or `qwen2.5-coder:3b`.
- Cloud Ollama models are filtered by default, so `qwen3-coder:480b-cloud`, `nemotron-3-super:cloud`, `GLM-5.1:cloud` and `qwen3.5:cloud` do not masquerade as installed local base models.
- Local smoke verified `qwen2.5-coder:3b` with `fallback_used=false`.
- EML is now integrated only as a `RESEARCH_ONLY` helper: `safe_eml`, `window_load_eml`, `jamming_margin_eml`, and a CLI `wabi eml` command.

### Technology Not Integrated by Design

- `escaner sigiloso.txt`: stealth SYN/ARP scanning and evasion language is not integrated. Safe alternative is passive/local inventory only, never stealth scanning.
- Replit `Duat-Geodia` UI/API is not imported wholesale. Useful candidates remain: React/Vite agent lab panels, WitnessLog API routes, handoff routes, OpenAPI/Zod contracts, falsifier panel, EML panel and simulation snapshots.
- OSIT-QG physics claims remain research-only. No public/commercial claim or core runtime dependency should be added without falsification and source review.
- Wabi/Sabi is not declared as an AGI or complete autonomous programmer. The correct status is local coding-agent shell with ActionGate, base-model route, workpacks, tests and evidence.

## Wabi/Sabi Capability Matrix

| Requirement | Current status | Evidence |
|---|---|---|
| Understand repo / inspect files | `PARTIAL/OK` | CLI agents, parser/router, filesystem tools |
| Edit files safely | `PARTIAL/OK` | scoped local patch path exists; broad autonomy still gated |
| Shell/tests/build | `PARTIAL/OK` | local tests pass; external actions remain gated |
| Direct base model | `OK` | `auto_provider=ollama`, `base_model=qwen2.5-coder:3b`, smoke `OK` |
| Fallback policy | `OK` | provider order `ollama, codex, dry-run`; attempts recorded |
| ActionGate | `OK` | local gate before routes; dangerous prompts blocked/reviewed |
| Witness/continuity | `OK/PARTIAL` | local logs, decision log, workpack, COMMS plans |
| EML | `RESEARCH_ONLY/OK` | helper module and CLI added; not daily core |
| Mission Control city view | `PARTIAL` | specs and state docs exist; Replit dashboard not absorbed |
| Stealth scanner | `BLOCK` | not safe or needed for Wabi/Sabi coding-agent goal |

## Next Safe Backlog

1. Add a real `PatchPlanner -> RollbackStore -> SafeExecutor` regression path if broad code edits are desired.
2. Add a Wabi `/tools` or `tool-registry` status command that enumerates filesystem, shell, git, tests, browser/MCP availability without exposing secrets.
3. Add a non-destructive project scanner that reports package managers, test commands and repo boundaries for the current workspace.
4. Keep EML behind explicit `wabi eml` / research mode only.
5. Do not import the Replit export directly; extract specific contracts into Wabi only if a target feature needs them.
