# QUATERNARY TIMING CORE v0.9

## Purpose

The quaternary timing core converts two operational bits into a stable diagnostic signal:

- Presence `P`: signal exists or does not exist.
- Difference `D`: signal differs from expectation or prior state.

The resulting state is:

| Q | Meaning | Use |
|---|---|---|
| `00` | stable silence | cache, skip, background |
| `01` | significant absence | missing expected signal, raise review |
| `10` | stable presence | compression, LOD, routine continuity |
| `11` | active event | full update, event expansion |

## Timing Metrics

Each source maintains a bounded timing window:

- `dwellTicks`: consecutive ticks in the same Q state.
- `frequency`: transition rate inside the window.
- `period`: average distance between repeated current-state occurrences.
- `permanence`: dwell normalized by window size.
- `stability`: permanence + inverse frequency + period score.
- `confidence`: output confidence after timing/residue.
- `residue`: noise, oscillation or significant absence pressure.

The implementation is deterministic and testable. It uses explicit ticks, not `Date.now`.

## Gate Behavior

- `00` compresses unless a signal was expected.
- `01` raises R and routes to REVIEW.
- `10` lowers R and supports cached/low LOD state.
- `11` expands only when timing is stable enough; noisy events route to REVIEW.
- High frequency penalizes R and prevents immediate expansion.

## Formal-Lab Boundary

This is software instrumentation. It does not measure electricity, create hardware, prove quantum behavior or assert a new physical theory.

