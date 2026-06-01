# obsai-core

**Dependency-free evidence core for local-first AI agents.**

Zero dependencies. Pure Python. MIT license.

obsai-core is the canonical public library for evidence envelopes, action gates, residue scoring, witnessable decisions and epistemic classification. It powers the Observacionismo / PSI-IA operational stack and is the recommended starting point for any agent safety toolkit.

```python
# One-liner: block or allow an action
from obsai_core import evaluate_action
result = evaluate_action(action="delete project folder")
# → {"decision": "BLOCK", "reason": "high_risk_low_reversibility"}
```

## Why obsai-core?

- **Dependency-free** — no pip install chain, no npm, no framework lock-in
- **Local-first** — no cloud, no telemetry, no API keys
- **Witnessed** — every decision writes to a local audit trail
- **Epistemic** — built-in claim classification with TruthGate, C-GATE, PhysicsHonestyGate
- **Tested** — 72 unit tests, all passing
- **Public-safe** — clean boundary from private MEDIOEVO research and RPG/TCG

## Quick Start

```bash
pip install .
python demo_agent_action.py --action "summarize README"
# → {"decision": "APPROVE", "witness_log": "witness/..."}
python demo_agent_action.py --action "delete project folder"
# → {"decision": "BLOCK", "reason": "high_risk_low_reversibility"}
```

## CLI

```bash
python -m obsai_core.cli triage --signals circularity corrections unresolved_tasks
python -m obsai_core.cli evaluate-action examples/action_review.json
python -m obsai_core.cli classify-text --text "El observador no observa desde cero"
python -m obsai_core.cli serve-epistemic-engine --host 127.0.0.1 --port 8789
python -m obsai_core.cli fingerprint --session-id demo-001
```

## Capabilities

| Feature | CLI | API | Description |
|---------|-----|-----|-------------|
| Residue scoring | `triage` | — | Estimate R from operational signals |
| Regime classification | `triage` | — | OPTIMO → FUNCIONAL → PRE_JAMMING → JAMMING |
| Action gate | `evaluate-action` | — | APPROVE / REVIEW / BLOCK with evidence |
| Claim classification | `classify-text` | POST /classify | Epistemic engine with 4-state output |
| Observation envelopes | `validate-envelope` | — | PROV-O/SHACL-lite contract validation |
| Session fingerprints | `fingerprint` | — | Deterministic state fingerprints |
| World simulation | `simulate-world` | — | Deterministic synthetic worlds |
| HTTP server | `serve-epistemic-engine` | GET /health, POST /classify | Local ephemeral API |

## Where It Fits

```
obsai-core          → canonical primitives and tests (this package)
residueos           → dashboard/API for review surfaces
duat-genesis        → synthetic research labs and falsifier demos
observacionismo-gate → SDK with zero dependencies
claudio-agent-runtime → DUAT Operator Shell kernel
```

## Test

```bash
python -m pytest tests -q    # 72 passed
python -m unittest discover -s tests
```

## Claims Boundary

- Engineering control layer, not proof of consciousness.
- Thresholds are DEMO_ONLY until calibrated with real datasets.
- Research claims belong in the research-boundary lane with falsifiers.
- Patent-derived material used as abstract software pattern; LEGAL_REVIEW_REQUIRED.

## License

MIT — see [LICENSE](LICENSE). Third-party notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).