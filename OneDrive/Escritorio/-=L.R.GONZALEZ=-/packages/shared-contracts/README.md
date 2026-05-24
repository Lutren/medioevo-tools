# MEDIOEVO Shared Contracts P0

Estado: local P0, no release publico.

PublicationGate: `BLOCK`

Este paquete define contratos, validadores, fixtures sinteticos y replay hash
determinista para conectar Wabi-Sabi, DUAT, Forge y el portal public-safe sin
mutacion directa entre capas.

`HypothesisPacket` agrega el carril de conjetura/falsador: toda afirmacion
relevante debe declarar contraafirmacion, falsadores, evidencia requerida,
ActionGate y frontera de publicacion antes de convertirse en canon, producto o
codigo aplicado.

## Fronteras

- Wabi-Sabi propone y aplica solo mediante `ActionGateDecision`.
- DUAT conserva `WorldState`, `AgentState`, replay y simulacion.
- Forge emite specs y previews; no muta DUAT directamente.
- Portal solo recibe exports `public_safe`.
- No contiene RPG/TCG/canon protegido, prompts raw, datasets privados,
  secretos, `.env`, tokens o credenciales.

## Estructura

```txt
packages/shared-contracts/
  schemas/
  fixtures/
  src/shared_contracts/
  tests/
```

## QA

```powershell
python -m unittest discover packages\shared-contracts\tests -v
```

## Uso minimo

```python
from shared_contracts import validate_contract, replay_hash

validate_contract("WorldState", payload)
digest = replay_hash(seed="demo-seed", payload=payload)
```
