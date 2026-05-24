# DUAT Smallville Remote Compute v0.1

Estado: `LOCAL_RESEARCH / PUBLICATION_GATE_BLOCK`.

Este carril implementa una primera simulacion tipo Smallville para DUAT sin
GPU y sin ejecucion externa automatica. El objetivo es aumentar capacidad de
laboratorio con parametros auditables, no declarar prediccion publica ni sesgo
ausente.

## Componentes

- `smallville_lab.py`: escenario sintetico con 25 agentes, zonas, memoria local,
  reflexion corta, plan, clima, presion atmosferica, geologia, rotacion,
  traslacion y presion social/media.
- `remote_compute.py`: plan gated para `local_cpu`, `colab_notebook`,
  `kaggle_kernel` y `simscale`.
- Schemas en `research/duat-predictive-registry/schemas/` para scenario,
  source pack, remote run spec y run ledger.

## Comandos

Desde `research/geodia-social-observatory`:

```powershell
python -m geodia_social_observatory.cli smallville-duat --seed duat-smallville-v0-1 --days 2 --ticks-per-day 6 --pretty --out ..\..\qa_artifacts\release_validation\duat-smallville-sim-lab-v0-1-ledger.json
python -m geodia_social_observatory.cli smallville-falsify --ledger ..\..\qa_artifacts\release_validation\duat-smallville-sim-lab-v0-1-ledger.json --pretty --out ..\..\qa_artifacts\release_validation\duat-smallville-sim-lab-v0-1-falsifier.json
python -m geodia_social_observatory.cli remote-compute-plan --pretty --out ..\..\qa_artifacts\release_validation\duat-remote-compute-plan-v0-1.json
python -m geodia_social_observatory.cli remote-notebook-template --pretty --out ..\..\qa_artifacts\release_validation\duat-smallville-colab-kaggle-template-v0-1.ipynb
```

## Gates

- `local_cpu`: `APPROVE_LOCAL`.
- `colab_notebook`: `REVIEW`; plantilla manual solamente.
- `kaggle_kernel`: `REVIEW`; requiere presencia de credenciales fuera del repo.
- `simscale`: `REVIEW`; fisica/microclima solamente, no cognicion social.
- `publication_gate`: `BLOCK` en todos los outputs.

## Falsadores

- replay determinista con mismo seed;
- hash-chain valida;
- 25 agentes sinteticos;
- valores acotados;
- sin rutas privadas, tokens ni secretos;
- sin publicacion externa;
- claim de sesgo limitado a `AUDITABLE_NOT_ABSENT`.

## Evidencia 2026-05-17

- `python -m pytest tests -q` en GEODIA: `58 passed`.
- `python -m pytest tests -q` en DUAT predictive registry: `117 passed`.
- Artefactos generados en `qa_artifacts/release_validation/`:
  - `duat-smallville-sim-lab-v0-1-ledger.json`
  - `duat-smallville-sim-lab-v0-1-falsifier.json`
  - `duat-remote-compute-plan-v0-1.json`
  - `duat-smallville-colab-kaggle-template-v0-1.ipynb`

## Limites

No publicar, no subir notebook publico, no montar Drive privado, no pegar
credenciales, no usar datos reales sin SourceCard/licencia/hash, no hacer
ranking, causalidad, prediccion electoral/social ni afirmacion de ausencia de
sesgo.
