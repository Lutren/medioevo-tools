# Public-Safe Review Runbook

package_id: GEODIA_PUBLIC_SAFE_PACKAGE_CANDIDATE_v0.1
publication_gate: BLOCK

## Local review steps

1. Review `README.md` and `CLAIMS_BOUNDARY_PUBLIC_SAFE.md`.
2. Review `ATTRIBUTION_AND_TERMS_REVIEW.md` with human/legal reviewer.
3. Confirm `EXCLUDED_FROM_PUBLIC_SAFE.md` remains true.
4. Confirm the package zip contains only `release/public_safe_candidate_v0_1/` files.
5. Re-run internal QA from the full GEODIA repo before any publication decision.

## Internal QA commands

```powershell
python -m pytest
python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty
python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty --fixtures research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json
```

## External release gate

Do not publish until a separate human/legal ActionGate approves external distribution.
