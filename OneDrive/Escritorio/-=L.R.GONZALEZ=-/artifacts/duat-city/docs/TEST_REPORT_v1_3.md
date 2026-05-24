# TEST_REPORT_v1_3

Fingerprint: DUAT-v1.3-GAME-OS-DISK-FORENSICS-LANGUAGE-CORTEX

## Baseline

- Baseline tests: PASS, 71 files / 260 tests.
- Baseline typecheck: PASS.
- Baseline build: PASS.
- Baseline HTTP smoke: 200.

Logs:
`qa_artifacts/release_validation/RUN_DUAT_GAME_OS_v1_3_20260520/`

## Final QA

- Tests: PASS, 84 files / 280 tests.
- Typecheck: PASS.
- Build: PASS.
- HTTP smoke: 200.

## Boundary Scan

- High-confidence secret count: 0.
- publication_allowed=true assignment count: 0.
- Wabi execution true assignment count: 0.
- unknown_code_executed=true assignment count: 0.
- reviewed-assets/v1_3 copied file count: 0.

## Notes

The broad lexical scan produced false positives for words such as tokens in style-token docs. The refined high-confidence scan is the release evidence.
