# Observacionismo Lab Smoke Results 2026-05-03

Status: `LOCAL_SMOKE_EVIDENCE`

## Commands

```powershell
python -m py_compile research\observacionismo-lab\observacionismo_lab.py
python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --galaxies 6 --samples 80 --out qa_artifacts\research\observacionismo_lab_demo_2026-05-03.json
python research\observacionismo-lab\observacionismo_lab.py demo --truth psichi --galaxies 6 --samples 80 --out qa_artifacts\research\observacionismo_lab_demo_psichi_2026-05-03.json
```

## Artifacts

| artifact | sha256 |
|---|---|
| `qa_artifacts\research\observacionismo_lab_demo_2026-05-03.json` | `1D3D44D7E189691846D754570CC532D364EBB81C6E4D90A769948B0BC9F840F3` |
| `qa_artifacts\research\observacionismo_lab_demo_psichi_2026-05-03.json` | `4484706B9FB1BAFA87655AD23FD6B4AB2FB6AFBFEFD162BEAD410AC381041453` |

## Result Summary

| truth | profiles | winner counts | reading |
|---|---:|---|---|
| `rar` | 3 | `rar: 3` | the corrected observer/proxy audit recovered RAR under this small synthetic smoke |
| `psichi` | 3 | `psichi: 2`, `pop_nfw: 1` | the control is not perfectly stable at this small size/sample budget; use as a warning, not a victory claim |

## Verdict

- `CERTEZA`: the corrected harness runs and writes reproducible JSON evidence.
- `CERTEZA`: the old shallow-copy, non-deterministic hash seed and fractional
  completion issues were addressed in the new local harness.
- `INFERENCIA`: the RAR toy smoke is stable under the three default proxies.
- `INCOGNITA`: the PSI control needs larger sample budgets, extended baselines
  and residual checks before it can be used as strong validation of the
  observer-audit protocol.

## Public Boundary

Do not publish this smoke as physics evidence. It is engineering evidence that
the local harness works and that the system is willing to report an unstable
control instead of inventing success.

## Update - v3 Insight Extraction Smoke

Implemented in `research\observacionismo-lab\observacionismo_lab.py`:

- `scientific_community` observer profile.
- `adversarial_observer` stress-test profile.
- `--control none|shuffled_baryons|shuffled_velocities`.
- Per-profile `margin_to_second_delta_bic`, ranking list, `winner_rate`,
  `mean_margin_to_second_delta_bic` and `rank_stability`.

Commands:

```powershell
python -m py_compile research\observacionismo-lab\observacionismo_lab.py
python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --galaxies 5 --samples 40 --profiles visual_proxy,scientific_community,adversarial_observer,instrument_balanced --out qa_artifacts\research\observacionismo_lab_profiles_smoke_2026-05-03.json
python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --galaxies 5 --samples 40 --control shuffled_baryons --profiles instrument_balanced,scientific_community,adversarial_observer --out qa_artifacts\research\observacionismo_lab_shuffled_baryons_smoke_2026-05-03.json
```

Artifacts:

| artifact | sha256 |
|---|---|
| `research\observacionismo-lab\observacionismo_lab.py` | `EB22414716B4369C772E1B47E501415F7A679AB86AB9AAC00C33FF6CE8F5C7C9` |
| `qa_artifacts\research\observacionismo_lab_profiles_smoke_2026-05-03.json` | `5E5DD6D0F5724EE2EE5E52A79B5DB86125D170E33948C4BEFDF1F24F53480AEE` |
| `qa_artifacts\research\observacionismo_lab_shuffled_baryons_smoke_2026-05-03.json` | `3266B3B14C7DF1552B7D2298B5C953F4FA5C248013225008044672A053B94B77` |
| `qa_artifacts\research\observacionismo_lab_selftest_2026-05-03.json` | `D8428C4953FFA22E7C91A7579051E9636CA604F7EBCC53E7572BA4E0050D72F7` |
| `qa_artifacts\research\observacionismo_lab_heldout_smoke_2026-05-03.json` | `0DA993A17D7186D5258B1E7DA6D50F0F60DF0C2A3D840D2751265823EDEE7A05` |

Result summary:

| run | control | profiles | winner counts | winner rate | mean margin | rank stability | reading |
|---|---|---:|---|---:|---:|---:|---|
| profile smoke | `none` | 4 | `rar: 4` | 1.0 | 1503.486 | 0.5 | RAR remains winner, but full ranking is not invariant across proxies |
| negative control | `shuffled_baryons` | 3 | `pop_nfw: 3` | 1.0 | 813.391 | 1.0 | broken baryon link changes the winner; this is useful falsifier behavior, not physics evidence |

Validation:

- `python -m py_compile ...`: passed.
- `python research\observacionismo-lab\observacionismo_lab.py selftest --out qa_artifacts\research\observacionismo_lab_selftest_2026-05-03.json`:
  `ok=true`, normal winner `rar`, shuffled-baryons control winner `pop_nfw`.
- `python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --galaxies 6 --samples 35 --profiles instrument_balanced,scientific_community,adversarial_observer --heldout-frac 0.2 --out qa_artifacts\research\observacionismo_lab_heldout_smoke_2026-05-03.json`:
  `winner_counts={"rar":3}`, `winner_rate=1.0`, `rank_stability=0.6667`,
  and every profile reported `heldout_report.ok=true`.
- `python tools\release\scan_secrets.py --path research\observacionismo-lab --json --fail-on-findings`: `count_reported=0`.
- Scanning the JSON artifacts through `scan_secrets.py` reports `denylist path`
  because `qa_artifacts` is intentionally blocked for publication staging; this
  is path policy, not a content secret finding.
