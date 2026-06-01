# Cross-Product Integration Map

Date: 2026-05-31

## Current State

Each product in the MEDIOEVO ecosystem runs independently with no shared
backend or data layer. This document maps integration opportunities.

## Integration Opportunities

### obsai-core → FlujoCRM

obsai-core's OSIT Epistemic Engine can classify CRM pipeline stages as
epistemic states (CERTEZA / INFERENCIA / INCOGNITA / BLOQUEADO) to help
salespeople identify which deals need evidence.

```
Pipeline stage → classify-text → epistemic label → dashboard badge
```

### obsai-core → Argus Desktop

ActionGate can filter agent actions before execution, providing a safety
layer for desktop automation.

### obsai-core → DUAT Lite Dashboard

Already partially integrated: DUAT Lite (`tools/duat-lite`) uses the OSIT
Epistemic Engine API for claim classification.

### DUAT Genesis → Commercial Apps

DUAT Genesis simulation runs can generate synthetic CRM data for FlujoCRM
demo/training mode.

### Unified CLI

Proposal: create `medioevo` CLI at root level that wraps:

- `medioevo status` → shows R, Phi_eff, regime from obsai-core
- `medioevo classify <text>` → OSIT epistemic classification
- `medioevo gate <action>` → ActionGate evaluation
- `medioevo fingerprint` → session fingerprint

## Implementation Priority

1. obsai-core + DUAT Lite (already done, deepen integration)
2. Unified CLI (low effort, high visibility)
3. obsai-core → FlujoCRM (pipeline classification)
4. DUAT Genesis → FlujoCRM (synthetic demo data)
5. obsai-core → Argus Desktop (action safety gate)

## Status

All integration points are `LOCAL_DESIGN_ONLY` — no code changes made to
commercial apps in this cycle. Publication gates remain `BLOCK`.