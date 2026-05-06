# Observacionismo Lab v3 Insights Intake 2026-05-03

Status: `RESEARCH_ONLY_SELECTIVE_EXTRACTION`

These Downloads sources were requested by Luis Rene Gonzalez Lopez for the
current Claudio/Wabi-Sabi run. They are not public artifacts and are not
publication evidence.

## Sources

| source | exists | bytes | lines | sha256 | classification | allowed use |
|---|---:|---:|---:|---|---|---|
| `C:\Users\L-Tyr\Downloads\He construido el laboratorio unific.txt` | yes | 55524 | 1201 | `70F77199A9B30831FF968FC2EE45FB523C8E8532808AB38F283761DCF688FFB7` | OBSERVACIONISMO_LAB_SYNTHESIS_NOTE | Extract methodology and claim-boundary lessons only. |
| `C:\Users\L-Tyr\Downloads\Destrucción de los Grados de Libert.txt` | yes | 47219 | 603 | `6667EAACBDECD64CFEFBBC410ECCEDD00D6F74396C86913C674ADA7947FE237B` | OBSERVACIONISMO_LAB_CRITIQUE_AND_V2_NOTE | Extract anti-false-certainty, negative-control and observer-formalization lessons only. |
| `C:\Users\L-Tyr\Downloads\observacionismo_lab_v3.py` | yes | 39237 | 839 | `231A020B167E95B7F98F04D1C3306CD64BADAD571FD29DB289D00AD9DE707936` | OBSERVACIONISMO_LAB_V3_CODE_SOURCE | Inspect and selectively port design patterns after tests/scan; do not publish raw. |

## Useful Tech

`CERTEZA`:

- The notes emphasize the same correction already applied locally: do not
  duplicate points as evidence; increase uncertainty or track metadata instead.
- The notes call for negative controls, SPARC/BIG-SPARC support, adversarial
  observers and residual diagnostics.
- `observacionismo_lab_v3.py` contains a cleaner class-based design:
  `TruthModel`, observer classes, `ScientificCommunityObserver`,
  `AdversarialObserver`, candidate models and repeated experiment summaries.

`INFERENCIA`:

- The v3 source can inform the next local harness refactor, but should not
  replace the already-tested `research/observacionismo-lab` harness without
  focused tests and claim boundaries.
- The most useful Claudio extraction is not physics code; it is the process:
  source ficha, observer contract, negative controls, baseline comparison and
  honest downgrade when a model fails.

`INCOGNITA`:

- The v3 file still needs current local execution, static review and comparison
  against `psi_chi_lab_v9.py`.
- Scientific claims remain provisional until real-data loaders, nuisance
  models, dataset citations and independent review are added.

## Boundaries

- Do not copy the raw notes into GitHub or product copy.
- Do not claim RAR, PSI Chi, MOND, dark matter, Newton or Einstein are settled.
- Do not use these sources to justify public deploys while ActionGate is
  `REVIEW` or `BLOCK`.
- If v3 code graduates, extract only tested pieces into a clean local research
  package with `CLAIMS.md`, tests and synthetic fixtures.

## Next Extraction Tasks

1. DONE locally: add `scientific_community` and `adversarial_observer`
   profiles to the local Observacionismo Lab harness.
2. DONE locally: add shuffled controls via
   `--control none|shuffled_baryons|shuffled_velocities`.
3. DONE locally: add `winner_rate`, `mean_margin_to_second_delta_bic`,
   `rank_stability`, per-profile `residual_signature` and `heldout_report`.
4. DONE locally: add a no-network `selftest` command for free local usage.
5. TODO: feed the remaining task list to the local Qwen CLI when host pressure
   allows.

Evidence: `docs\developer\OBSERVACIONISMO_LAB_SMOKE_RESULTS_2026-05-03.md`,
section `Update - v3 Insight Extraction Smoke`.
