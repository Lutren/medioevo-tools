# PIXEL FIELD QA v0.7

Fingerprint: `DUAT-VISUAL-QA-ASSET-ALLOWLIST-v0.7`
Date: 2026-05-19

## Scope

The pixel/cell physics field does not simulate every screen pixel as a full particle. It uses a low-resolution discrete field with active-cell updates:

- water falls and spreads;
- smoke rises;
- fire emits smoke/light;
- dust falls;
- light decays;
- inactive cells are skipped.

This preserves the design intent that every logical cell can carry material/physics state without making the browser render impossible.

## Evidence

- Test: `src/tests/pixelFieldQA.test.ts`
- Screenshot: `docs/screenshots/v0_7/osit-debug-pixel-field.png`
- OSIT Debug panel displays active cells, skipped cells, hazards and field R/Phi.

## Result

PASS for v0.7 validation scope. Remaining work is tuning, not expansion: the next step should benchmark larger fields and make field hazards affect visible city events more clearly.
