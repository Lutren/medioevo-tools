# DUAT Genesis

**Synthetic sandbox for observable simulation experiments.**

Zero dependencies. Pure Python. MIT license. [Published on GitHub](https://github.com/Lutren/duat-genesis).

DUAT Genesis creates deterministic synthetic worlds, applies observation rules, and emits reproducible simulation reports. It is a **public, dependency-free** lab for testing falsifiers, action gates, and epistemic patterns.

> Not DUAT Geodia. DUAT Geodia remains a private MEDIOEVO research lane. This package only exposes generic simulation contracts and synthetic state.

## Quick Start

```bash
pip install .
python -m duat_genesis.cli run --seed demo --size 8 --ticks 5
python -m duat_genesis.cli report --seed demo --ticks 5
python -m duat_genesis.cli falsify --seed demo --ticks 5
```

## What It Does

- Creates deterministic synthetic worlds from a seed
- Applies bounded numeric observation and rule pressure
- Emits reproducible `SimulationRun` reports with full provenance
- Runs basic falsifiers for determinism, bounded values and claim safety
- Provides CLI commands: `run`, `report`, `falsify`
- Exposes public-safe Run 8 helpers: ActionGate v2, WitnessLog v2, source cards, handoff validation

## What It Does NOT Do

- Does not predict real social, biological, neurological or physical systems
- Does not include private DUAT Geodia engineering
- Does not include MEDIOEVO RPG/TCG assets, lore or game runtime
- Does not provide medical, scientific or safety guarantees

## Public Claim

**Allowed:** "synthetic sandbox for observable simulation and falsifier examples."
**Blocked:** validated science, real-world prediction, diagnosis, private engineering claims.

## Run 8 Helpers

```python
from duat_genesis import ActionGateInput, action_gate_v2, get_public_modules

modules = get_public_modules()
result = action_gate_v2(ActionGateInput(
    evidence=0.9, risk=0.1, reversibility=0.9,
    authorization=0.9, phi_eff=0.8, r_delta_expected=-0.2,
    touches_secrets=False, external_publish=False, destructive=False,
))
```

## Test

```bash
python -m pytest tests -q
```

## License

MIT — see [LICENSE](LICENSE).