# DUAT v0.6 Boundary Evidence

publication_gate: BLOCK
run_id: DUAT_NESTED_DOMAIN_BACKTEST_v0_6

v0.6 is boundary evidence: the current calibration does not generalize out-of-sample on short fixtures. The correct next action is not additional tuning on the same short history, but official long-history data readiness and provenance review.

## What Was Tested

DUAT v0.6 ran a nested walk-forward backtest over three real fixtures:

- economy.real_growth_rate
- labor_market.unemployment_rate.total
- demography.life_expectancy_at_birth.total

The nested design separated inner calibration from outer out-of-sample evaluation and kept the outer test fold outside parameter selection.

## What Happened

- BacktestLeakageGuard: PASS.
- LeakageCheck: PASS.
- SchemaValidation: PASS.
- ClaimsScan: PASS.
- All three indicators returned OOS_METRICS_WORSE.
- OutOfSampleGate: REVIEW.
- ForecastGate: REVIEW.
- publication_gate: BLOCK.

## What Cannot Be Claimed

- No public predictive claim is authorized.
- No ranking, causal claim or electoral prediction is authorized.
- No statement of predictive superiority is authorized.
- No claim that DUAT is ready for external publication is authorized.

## What Was Learned

- The short fixtures are useful as mechanics tests, but not as robust predictive evidence.
- Reducing operational residue inside the same fixture is not enough.
- Out-of-sample behavior is the current boundary.
- More tuning on the same short history risks overfitting.

## Why This Reduces R

This result reduces R by preventing false closure. It records that the current model path reached a boundary, preserves the uncomfortable evidence, and redirects the next run toward data provenance and long-history readiness instead of parameter chasing.

## Requirement Before Another Benchmark

Before another benchmark, DUAT needs official long-history data with:

- documented source URL;
- license or terms review;
- temporal coverage audit;
- gap and unit review;
- comparability review;
- leakage preflight;
- enough observations for stable walk-forward folds.
