# PSI Chi SPARC Results 2026-05-03

Status: `LOCAL_RESEARCH_EVIDENCE`

This report records the local falsification run for `psi_chi_lab_v8.py` and the
derived `psi_chi_lab_v9.py`. It is not a publication claim.

## Registered Sources

- Source ficha: `docs/intake/PSI_CHI_SPARC_LAB_INTAKE_2026-05-03.md`
- Dataset: `C:\Users\L-Tyr\data\Rotmod_LTG.zip`
- v8 source: `C:\Users\L-Tyr\Downloads\psi_chi_lab_v8.py`
- v9 derived script: `C:\Users\L-Tyr\psi_chi_lab_v9.py`

## v9 Implementation Notes

- Added `leaderboard-extended`.
- Added MOND variants: `mond_simple`, `mond_standard`.
- Added NFW baselines: `nfw_local`, `nfw_hier`.
- Added `--path` and `--limit` support to `leaderboard-extended`.
- Corrected the NFW virial-radius approximation in v9:
  `r200 = v200/(10*H0)` with `H0 ~= 0.07 km/s/kpc`, so `r200_kpc = v200/0.7`.

## Commands

```powershell
python Downloads\psi_chi_lab_v8.py leaderboard-sparc --path data\Rotmod_LTG.zip --samples 5000
python Downloads\psi_chi_lab_v8.py crossval-sparc --path data\Rotmod_LTG.zip --samples 3000 --folds 5
python psi_chi_lab_v9.py leaderboard-extended --truth rar --samples 800 --seed 42
python psi_chi_lab_v9.py leaderboard-extended --path data\Rotmod_LTG.zip --samples 3000 --seed 42
```

## Artifacts

| artifact | sha256 |
|---|---|
| `docs/developer/psi_chi_results/psi_chi_v8_leaderboard_sparc_2026-05-03.csv` | `1E93FC79F4C2AFD4A5DC2F3A217809050906470B56A979D7DBEDF783728A2ABA` |
| `docs/developer/psi_chi_results/psi_chi_v8_crossval_sparc_2026-05-03.csv` | `0E8E28D946959727A6A97CA753941CFEC81177EDDD099F6058F58F8843606B81` |
| `docs/developer/psi_chi_results/psi_chi_v9_leaderboard_extended_sparc_2026-05-03.csv` | `5470C50ED4328140EDC9CC832DC9A82AD29A978399C4530329F532230E33F787` |
| `C:\Users\L-Tyr\psi_chi_lab_v9.py` | `726FEA131C31EB6A40B34E3C06BE79E5838D29C0413014B1190C8E1FF0F9AA2F` |

## v8 SPARC Leaderboard

SPARC points: `3391`; galaxies: `175`.

| rank | model | BIC | delta_BIC | reduced_chi2 | rms_frac_velocity |
|---:|---|---:|---:|---:|---:|
| 1 | `rar` | 27804.637 | 0.000 | 8.1996 | 0.29801 |
| 2 | `psichi` | 33675.845 | 5871.208 | 9.9347 | 0.27885 |
| 3 | `pop_nfw` | 103322.502 | 75517.865 | 30.5026 | 0.37861 |
| 4 | `newton` | 103659.213 | 75854.577 | 30.5822 | 0.37667 |

## v8 SPARC Cross-Validation

| model | mean_test_BIC | median_test_BIC | folds |
|---|---:|---:|---:|
| `rar` | 5639.145 | 5853.539 | 5 |
| `psichi` | 8372.343 | 8099.403 | 5 |
| `pop_nfw` | 20688.950 | 21212.272 | 5 |
| `newton` | 20741.622 | 20850.378 | 5 |

## v9 Extended SPARC Leaderboard

SPARC points: `3391`; galaxies: `175`.

| rank | model | BIC | delta_BIC | reduced_chi2 | rms_frac_velocity | k_params |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `rar` | 27804.637 | 0.000 | 8.1996 | 0.29801 | 3 |
| 2 | `mond_simple` | 28034.343 | 229.707 | 8.2674 | 0.30006 | 3 |
| 3 | `mond_standard` | 28349.789 | 545.153 | 8.3605 | 0.29926 | 3 |
| 4 | `nfw_hier` | 29099.333 | 1294.697 | 8.5824 | 0.30372 | 8 |
| 5 | `psichi` | 37445.932 | 9641.295 | 11.0488 | 0.32920 | 7 |
| 6 | `nfw_local` | 39729.754 | 11925.118 | 12.1318 | 0.27029 | 352 |
| 7 | `pop_nfw` | 44876.331 | 17071.695 | 13.2415 | 0.29499 | 5 |
| 8 | `newton` | 103659.213 | 75854.577 | 30.5822 | 0.37667 | 2 |

## Verdict

- `CERTEZA`: `rar` wins the v8 SPARC leaderboard and the v9 extended SPARC leaderboard.
- `CERTEZA`: `rar` wins the v8 SPARC cross-validation.
- `CERTEZA`: `psichi` does not meet the protocol threshold of win/tie within `delta_BIC <= 6`.
- `INFERENCIA`: NFW hierarchical is a meaningful stronger baseline after the v9 `r200` correction, but it still trails `rar` by `delta_BIC = 1294.697` in this run.
- `INCOGNITA`: The NFW local grid is still coarse and descriptive; a more serious dark-matter comparison needs a fitter with wider priors, nuisance terms and independent review.

Operational conclusion: do not publish PSI Chi as validated physics from this evidence. Keep it as a falsifiable research harness and improve baselines before any public claim.
