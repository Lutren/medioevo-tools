# DUAT Genesis

DUAT Genesis is a public, dependency-free synthetic sandbox for observable
simulation experiments.

It is not DUAT Geodia. DUAT Geodia remains a private MEDIOEVO research/runtime
lane. This package exposes only generic simulation contracts, synthetic state
updates, falsifier scaffolds and reports that can be modified for safe research
experiments.

## What It Does

- creates deterministic synthetic worlds from a seed;
- applies generic observation and rule pressure to bounded numeric state;
- emits reproducible `SimulationRun` reports;
- runs basic falsifiers for determinism, bounded values and claim safety;
- provides a small CLI for `run`, `report` and `falsify`;
- exposes public-safe Run 8 helpers: DUAT Module Registry, ActionGate v2,
  WitnessLog v2, source cards, public prompts, handoff validation and legacy
  transfer checklists.

## What It Does Not Do

- it does not predict real social, biological, neurological or physical systems;
- it does not include private DUAT Geodia engineering;
- it does not include MEDIOEVO RPG/TCG assets, lore, scenes or game runtime;
- it does not provide medical, scientific or safety guarantees.

## CLI

```powershell
python -m duat_genesis.cli run --seed demo --size 8 --ticks 5
python -m duat_genesis.cli report --seed demo --ticks 5
python -m duat_genesis.cli falsify --seed demo --ticks 5
```

## Public Run 8 Helpers

```python
from duat_genesis import ActionGateInput, action_gate_v2, get_public_modules

modules = get_public_modules()
result = action_gate_v2(
    ActionGateInput(
        evidence=0.9,
        risk=0.1,
        reversibility=0.9,
        authorization=0.9,
        phi_eff=0.8,
        r_delta_expected=-0.2,
        touches_secrets=False,
        external_publish=False,
        destructive=False,
    )
)
```

## Public Claim

Allowed: "synthetic sandbox for observable simulation and falsifier examples."

Do not claim validated science, real-world prediction, diagnosis, private DUAT
Geodia engineering, or RPG living-world runtime.
