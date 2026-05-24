# Wabi Provider Status - 2026-05-18

Current documented provider posture:

- Chat runtime: `ollama-cloud / qwen3-coder:480b-cloud` for normal chat only.
- Fallback: `ollama-local`.
- DeepSeek: `REVIEW_QUOTA_OR_BILLING`.
- NVIDIA: `DO_NOT_CALL` pending route/model review.
- Apply gates: unchanged.
- Operational Workbench reports `ACTIVE_CLOUD_ENGINE` with `cloud_context_policy=SUMMARY_ONLY`.
- Provider diagnostic remains NVIDIA route review with `SMOKE_FAIL_REDACTED` and `recommended_next_smoke=DO_NOT_CALL`.

No private workspace, routes, code or runtime material should be sent to cloud
LLM providers. Cloud chat use is allowed only for sanitized chat content under
the current gate.
