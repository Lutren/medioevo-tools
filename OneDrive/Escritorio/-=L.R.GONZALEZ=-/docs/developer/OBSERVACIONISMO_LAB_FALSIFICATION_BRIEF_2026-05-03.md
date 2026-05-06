# Observacionismo Lab Falsification Brief 2026-05-03

Status: `LOCAL_RESEARCH_EVIDENCE / PUBLIC_COPY_READY_AFTER_GATE`

This brief converts the current PSI/Sensorium work into a public-safe research
story for GitHub, LinkedIn and the MEDIOEVO site. It is deliberately low-claim.

## What Was Verified

- `psi_chi_lab_v8.py` and `psi_chi_lab_v9.py` have local fichas and hashes.
- SPARC data exists locally as `C:\Users\L-Tyr\data\Rotmod_LTG.zip`.
- The v8 SPARC run found `rar` ahead of `psichi`, `pop_nfw` and `newton`.
- The v8 SPARC cross-validation also favored `rar`.
- The v9 extended leaderboard added MOND variants and NFW baselines; `rar`
  still ranked first in the recorded run.
- `sensorium_inversion_lab_pack.zip` is registered as a synthetic observer-audit
  lab.
- `sensorium_psi_bridge_pack.zip` is now registered as research-only bridge
  material, not proof.
- `research/observacionismo-lab/observacionismo_lab.py` now exists as a local
  corrected harness; see
  `docs/developer/OBSERVACIONISMO_LAB_SMOKE_RESULTS_2026-05-03.md`.
- The requested Downloads insights were registered in
  `docs/intake/OBSERVACIONISMO_LAB_V3_INSIGHTS_INTAKE_2026-05-03.md`.
  The useful extraction is observer formalization, negative controls,
  anti-false-certainty weighting and adversarial/scientific-community observer
  profiles.

## Current Numerical Result

From `docs/developer/PSI_CHI_SPARC_RESULTS_2026-05-03.md`:

| run | winner | nearest competitor | margin |
|---|---|---|---:|
| v8 SPARC leaderboard | `rar` | `psichi` | delta BIC `5871.208` |
| v8 SPARC cross-validation | `rar` | `psichi` | mean test BIC gap `2733.198` |
| v9 extended SPARC leaderboard | `rar` | `mond_simple` | delta BIC `229.707` |
| v9 extended vs `psichi` | `rar` | `psichi` | delta BIC `9641.295` |

## Correct Interpretation

`CERTEZA`: In the recorded local runs, the PSI Chi model did not meet the
protocol threshold. It neither won nor tied SPARC within delta BIC <= 6.

`CERTEZA`: RAR/McGaugh-style acceleration relation was the strongest baseline
in these runs.

`INFERENCIA`: The current lab is useful as a falsifier architecture: it can
turn a speculative model into a tested model with visible failures.

`INCOGNITA`: This does not settle gravity, MOND, dark matter, cosmology or new
physics. Stronger nuisance modeling, priors, independent review, dataset
citation and cross-domain tests are still required.

## Engineering Takeaway For Claudio

The valuable result is not "Psi is true" or "RAR is final". The valuable result
is a reusable pattern:

```text
claim -> source ficha -> declared observer/proxy -> falsifier -> leaderboard
-> cross-validation -> claim downgrade or promotion -> public-safe copy
```

This pattern should become a Claudio rule for AI engineering:

- every agent claim needs evidence before promotion;
- every imported source needs a ficha;
- every benchmark needs negative controls;
- every observer/proxy needs a declared limitation;
- every public post needs a claim boundary.

## Public Copy Boundary

Allowed:

> I am building Observacionismo Lab: a falsification workflow for testing
> whether claims survive changes in observer, proxy, noise, baseline and
> held-out evidence.

Allowed:

> The current SPARC run is a useful negative result for my PSI Chi hypothesis:
> it did not win against RAR/McGaugh-style baselines in the local leaderboard.

Blocked:

- "I proved RAR is the first universal invariant."
- "PSI Chi is disproven forever."
- "Newton/Einstein are false."
- "Sensorium proves hidden physical structures."
- "The lab predicts the real world."

## Next Technical Closures

1. PARTIAL DONE: shuffled baryon and shuffled velocity controls now exist in
   `research\observacionismo-lab\observacionismo_lab.py`.
2. PARTIAL DONE: the harness avoids duplicating evidence for attention and now
   reports margins, rank stability, residual signatures and held-out galaxy
   residuals; explicit point-level metadata is still pending.
3. DONE locally: add no-network `selftest`; latest run returned `ok=true`.
4. Promote only the tested harness pattern into public repos.
5. Keep raw Downloads packages out of GitHub releases.
