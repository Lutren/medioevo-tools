# OBS Antigravity Runtime Review - 2026-05-01

Status: `REVIEWED_KEEP_GATED`

Source:

- `C:\Users\L-Tyr\Downloads\obs_antigravity_runtime.zip`
- SHA256: `d38f8c5114a34979748eaa3f50d4680ae905a7e2d9b51783b0ad612bb1625ede`
- Size: `62003` bytes
- ZIP entries: `34`
- Extracted for review only under `%TEMP%`.

## Verdict

This is useful for the workspace if treated as a research/claim-gating runtime,
not as an antigravity product or physics claim.

The strongest reusable parts are generic:

- `EvidenceRecord` and evidence tiers.
- `EvidenceStore` / evidence scoring.
- `PACGate` abstention and review logic.
- `PhysicsConsistencyValidator` as a pattern for domain-specific claim gates.
- `OntologyGraph` / handoff export for next-session continuity.
- `CalibrationNetwork` as a simulation-only fixture for `C_ij` behavior.

Do not copy the package wholesale into a public repo. Extract patterns into
`obsai-core`, `ResidueOS Lite` or `ActionGate` only after renaming the domain
from "antigravity" to a neutral `extraordinary_claims` or `research_claims`
adapter.

## Local Verification

Command:

```powershell
$env:PYTHONPATH=$projectRoot
python -m unittest discover -s tests -v
```

Result:

```text
Ran 4 tests in 0.001s
OK
```

CLI smoke checks also worked:

- `python -m obs_antigravity.cli list`
- `python -m obs_antigravity.cli simulate --mode repulsion --n 20`
- `python -m obs_antigravity.cli evaluate anti-h-falls-normally`

Windows console output showed mojibake for accented Spanish text in one CLI
run. If kept, set UTF-8 output or use ASCII-safe public CLI messages.

## Scientific Boundary

The package correctly avoids claiming physical antigravity. CERN's 2023 ALPHA
release says the antihydrogen result is compatible with ordinary attractive
gravity within the experiment precision, and notes the Nature paper from the
same day.

Use that as a conservative validator source only. Do not turn it into a claim
that all antimatter gravity questions are fully closed, and do not use it to
sell antigravity technology.

Primary source:

- https://home.web.cern.ch/news/press-release/physics/alpha-experiment-cern-observes-influence-gravity-antimatter

## Risks

- The package name can attract speculative interpretation. Public-facing copy
  must say "epistemic filter for extraordinary claims".
- The ZIP includes `__pycache__` and `.pyc` bytecode. Remove before any
  packaging, commit or publication.
- `PACGate.required_samples` currently reports a high theoretical requirement
  while decisions use `min_samples` and validator count as practical samples.
  Document this clearly before using it as an authority metric.
- `EvidenceScorer` can produce `1.0` evidence score for a single strong source;
  keep final decisions in `REVIEW` unless replicated evidence exists.
- `OntologyGraph` is operational, not formal OWL/PROV-O. It is useful for
  handoff, but it should not be presented as a full ontology engine.

## Apply To Current Work

Immediate application:

- Add an `extraordinary_claim` or `scientific_claim` gate to ActionGate.
- Use `EvidenceTier` and `ClaimStatus` as the shared vocabulary for research
  claims.
- Reuse the `Decision.status` set: `PROCEED`, `REVIEW`, `ABSTAIN`, `RESET`,
  `BLOCK`.
- Use `ObservationEnvelope` to store evidence, validator output, PAC output and
  decision state in SQLite.
- Add a fixture modeled on the antimatter claim: strong primary evidence still
  produces `REVIEW`, not marketing certainty.

Deferred application:

- Convert `OntologyGraph` edges into PROV-O-like provenance relations.
- Map `process`, `artifact`, `mixed` classification into the DOLCE-lite layer.
- Keep `C_ij` as a synthetic simulation benchmark for drift/claim inflation.

Do not apply:

- Do not publish an "antigravity runtime" product page.
- Do not make LinkedIn/GitHub claims about antigravity.
- Do not include the ZIP raw or bytecode in public packages.
