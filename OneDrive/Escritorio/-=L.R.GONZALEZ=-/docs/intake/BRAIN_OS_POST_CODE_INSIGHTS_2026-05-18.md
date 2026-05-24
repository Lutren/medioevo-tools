# BRAIN_OS POST Code Insights - 2026-05-18

Source:
`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt`

SHA256:
`F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B`

Status: `CODE_INSIGHT_ONLY`

ActionGate: `APPROVE_LOCAL_DOCS_ONLY`

PublicationGate: `BLOCK`

RuntimeImport: `BLOCK`

## Boundary Decision

The source is an unregistered POST prototype. This pass extracts comparison
insights only. No class, function, demo, benchmark or raw text from the source
is imported into Wabi-Sabi, Claudio or open-dev runtime.

## Comparison Map

| source pattern | source evidence | existing target | integration posture |
|---|---|---|---|
| `OSITMath` entropy/R/Phi helpers | source lines 54-90 and 127-160 | `apps/local/wabi-sabi/wabi_sabi/core/geodia_math_core.py` | compare formulas only; do not replace tested helpers |
| `PSIState` | source lines 240-262 | Wabi observation/runtime state docs | possible vocabulary alignment only |
| `ObservationEnvelope` | source lines 266-294 | `apps/local/wabi-sabi/wabi_sabi/core/observation.py` | keep existing Wabi envelope; compare missing fields only |
| `RCalibrator` | source lines 301-310 and 381-400 | `packages/open-dev/claudio-agent-runtime/claudio_agent_runtime/rphi_budget.py` and `rphi_calibration.py` | benchmark fixture inspiration only |
| `Handoff` | source lines 419-469 | `SESSION_FINGERPRINT.json`, `NEXT_SESSION_BRIEF.md`, Claudio handoff docs | preserve continuity idea; no code import |
| `GhostGate` | source lines 485-540 and 721-751 | ActionGate/GhostGate planning lane in Claudio agent runtime | design comparison only; future test first |

## Defects Recorded As Evidence

| defect | evidence | consequence |
|---|---|---|
| Benchmark is not fully passing | audit run output: `SCORE: 5/6 (83%)` | cannot mark prototype validated |
| `F1_regime_prediction` fails | audit run output: expected `FUNCIONAL`/`PRE_JAMMING`, got `JAMMING` for three cases | calibrator/regime thresholds need review before reuse |
| Handoff overstates benchmark result | source line 923 and audit output: handoff says `Benchmark 5/5 OK` after score `5/6` | handoff truth must be generated from actual benchmark result |
| Windows console needs UTF-8-safe execution | audit command used `PYTHONIOENCODING=utf-8` to preserve symbols in PowerShell output | any future runner should set explicit UTF-8 output or avoid non-ASCII demo symbols |
| Stable trajectory tolerance bug | audit output: stable trajectory prints `lambda=0.0000 -> INESTABLE` | Lyapunov status needs epsilon/tolerance before use |

## Useful Deltas

- Keep an explicit distinction between pre-action simulation (`GhostGate`) and
  execution permission (`ActionGate`).
- Keep benchmark cases as negative fixtures, especially failing regime
  prediction and false handoff success.
- Keep session continuity fields: R close, Phi close, regime, decisions,
  open tasks, blocked claims and next action.
- Keep entropy/R/Phi vocabulary only as comparison material against tested
  Wabi/Claudio helpers.

## Rejected Material

- Whole-file import.
- Replacing `geodia_math_core.py`, `rphi_budget.py` or `rphi_calibration.py`
  from the prototype.
- Treating benchmark output as `PASS`.
- Treating `Benchmark 5/5 OK` as true.
- Publishing, packaging or moving the POST prototype.

## Next Runtime Gate

Future runtime work remains `REVIEW`. It must start from a small failing test in
the target lane, not from copying this source.
