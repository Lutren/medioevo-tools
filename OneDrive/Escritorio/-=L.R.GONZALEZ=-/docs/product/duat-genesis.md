# DUAT Genesis

Estado: `OPEN_SYNTHETIC_SANDBOX / NOT_PUBLISHED_THIS_RUN`.

Fuente local: `packages\open-dev\duat-genesis`.

DUAT Genesis es el carril publico de DUAT: un sandbox sintetico modificable para
experimentos de simulacion, observacion y falsacion. No contiene DUAT Geodia
privado, datos reales, RPG/TCG, Claudio runtime privado ni claims cientificos.

## Contratos publicos

- `GenesisState`
- `GenesisRule`
- `Observation`
- `Observer`
- `SimulationRun`
- `FalsifierResult`

## Comandos

```powershell
python -m pytest tests -q
python -m duat_genesis.cli run --seed demo --size 8 --ticks 5
python -m duat_genesis.cli report --seed demo --ticks 5
python -m duat_genesis.cli falsify --seed demo --ticks 5
```

## Claim permitido

Sandbox sintetico para explorar simulacion observable, reportes reproducibles y
falsadores.

## Claim bloqueado

Prediccion social, diagnostico neurologico, medicina, biologia validada,
proteinas reales, nueva fisica probada, DUAT Geodia publico o runtime vivo del
RPG.
