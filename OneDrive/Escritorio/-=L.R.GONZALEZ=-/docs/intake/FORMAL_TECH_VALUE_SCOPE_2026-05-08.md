# Formal Tech Value Scope - 2026-05-08

## Estado

CERTEZA:
- `Formal` is now a 50-file intake lane in the latest recheck; earlier pass
  counted 48 after adding `banananana.txt`.
- The folder is not a duplicate mirror by exact SHA256 against PSI/master/runtime index.
- The strongest value is not in a single file; it is the convergence of formal claims, agent contracts, evidence artifacts and model-routing policy.
- No file from `Formal` was moved, deleted, executed or imported wholesale into canon.

INFERENCIA:
- The technology value is `HIGH_INTERNAL_RESEARCH_VALUE` and `MEDIUM_PUBLIC_PRODUCT_VALUE` after claim and secret gates.
- The plausible advanced technology is a control plane for agents and models: `ObservationEnvelope`, `ActionGate`, `GhostGate`, handoff fingerprints, R/Phi_eff/EML metrics and provider fallback.
- It is not yet evidence of new validated physics, autonomous AGI or safe model-weight modification.

INCOGNITA:
- Whether R/Phi_eff/EML claims survive calibrated datasets and falsifiers.
- Whether `medioevo_agent_core.py` and `medioevo_core_v01.py` add non-duplicative contracts beyond Wabi/Sabi.
- Whether cloud providers materially improve local work once redaction, cost, privacy and host gates are enforced.

## Scope by Lane

| Lane | Sources | Value | Gate |
|---|---|---|---|
| Formal claims | `report.md`, `OI_P6R_paper_v0_1.md`, `paper_observacionismo_inverso.md`, `Auto.txt` | Method and theory deltas for Observacionismo/OI | `RESEARCH_ONLY` until falsifiers and excerpt comparison pass |
| Code contracts | `medioevo_agent_core.py`, `medioevo_core_v01.py`, `Completar04-07.txt`, `PR11.txt` | Candidate contracts for ActionGate, GhostGate, Handoff, Phi_eff, R | `CODE_INSIGHT`; extract tests/interfaces only |
| Evidence | JSON/CSV/PNG/PDF/ZIP artifacts | Traceable experiment and figure evidence | `REVIEW_EXTRACTION_REQUIRED` before claims |
| Secret provider config | `banananana.txt` | Confirms cloud-provider credential lane exists | `PRIVATE_SECRET_CONFIG`; redact always |
| Blocked execution | `uno.py`, `nucleo.txt`, shell/deploy text | Negative requirements for SafeExecutor | `BLOCKED_EXECUTION` |

## Implementation Outcome

- Wabi/Sabi now exposes `provider-status` as a real command, separate from general prompts.
- `chat`/`hablar` now uses local conversational response instead of accidentally routing to the diagnostic agent.
- NVIDIA NIM and Qwen cloud adapters exist as mockable provider adapters, blocked by default with `WABI_ALLOW_CLOUD_PROVIDERS=1` required for any real network call.
- A central redactor masks secret-like env values and sensitive fields in Wabi artifacts/status.
- Claudio now has `core/wabi_gateway.py` as a local bridge to Wabi/Sabi status/auto queries, without granting autonomy or printing secrets.

## Value Decision

State: `ADVANCED_INTERNAL_TECH_CANDIDATE / NOT_PUBLIC_SCIENCE_CLAIM`.

Recommended next move:
- Extract contracts and tests from the two Python modules first.
- Keep model modification as a later phase; begin with prompts, router policy, datasets and evaluation gates.
- Treat cloud models as fallback/contrast providers, not as the canonical brain or source of truth.
