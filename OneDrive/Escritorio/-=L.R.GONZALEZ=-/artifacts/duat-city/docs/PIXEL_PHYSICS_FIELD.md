# PIXEL_PHYSICS_FIELD

## Scope

This is not a real physics engine and does not claim physical novelty. It is a pragmatic low-resolution cell field used to feed visuals, hazards, agent pressure and RPG export.

## Files

- `src/physicsField/pixelTypes.ts`
- `src/physicsField/materials.ts`
- `src/physicsField/pixelField.ts`
- `src/physicsField/cellularPhysics.ts`
- `src/physicsField/fluidLite.ts`
- `src/physicsField/fireSmoke.ts`
- `src/physicsField/lightMatter.ts`
- `src/physicsField/fieldMetrics.ts`
- `src/physicsField/fieldRendererAdapter.ts`

## Rules

- Water falls and spreads laterally.
- Smoke rises.
- Dust falls.
- Fire creates smoke and light.
- Light decays.
- Inactive cells are skipped.
- Agents are sampled into the field but remain lightweight physics bodies, not fluids.

## Metrics

`activeCells`, `updatedCells`, `skippedCells`, `heat`, `pressure`, `unresolvedField`, `R_field`, `Phi_field`.

## Tests

`src/tests/pixelField.test.ts`
