# Metric Observation + DUAT Predictive Methods Ficha - 2026-05-06

Estado epistemologico: `INFERENCIA` para teoria de dimensiones metricas; `CERTEZA` para el contrato de software agregado y tests locales.

## Decision

Se integra la idea como contrato operativo publico-seguro en `obsai-core`, no como claim fisico ni conciencia artificial.

Artefactos:

- `packages/open-dev/obsai-core/obsai_core/metric_observation.py`
- `packages/open-dev/obsai-core/obsai_core/predictive_methods.py`
- `packages/open-dev/obsai-core/tests/test_metric_observation.py`

## Insight Absorbido

La parte util de la propuesta es representar observaciones como vectores con:

- eje metrico;
- unidad;
- rango normalizado;
- sensor autorizado;
- evidencia;
- timestamp local;
- confianza;
- residuo;
- fingerprint estable.

Esto encaja con Claudio, GEODIA y DUAT porque fuerza a los agentes a dejar evidencia antes de actuar.

## Limite De Claims

Bloqueado:

- conciencia demostrada;
- nueva fisica probada;
- prediccion social garantizada;
- diagnostico medico;
- accion externa automatica.

Permitido:

- vectores operacionales;
- calibracion entre observadores;
- consenso con residuo;
- escenarios probabilisticos;
- falsadores y backtests.

## Chronos / Chronos-2 Para DUAT

Chronos es util como motor de series temporales probabilisticas. La version `Chronos-2` se describe publicamente como modelo fundacional de 120M parametros para forecasting zero-shot, con soporte para tareas univariadas, multivariadas y covariables. Para DUAT esto sirve como generador de escenarios, no como oraculo.

Decision DUAT:

- `Chronos`: `REVIEW` por dependencia externa/modelo pesado/provenance.
- `Local baseline forecast`: `APPROVE` como piso de comparacion.
- `State-space/Kalman`: `APPROVE` para tracking local.
- `Agent-based counterfactual`: `APPROVE` para laboratorio sintetico.
- `Causal impact/synthetic control`: `REVIEW` por supuestos fuertes.
- `Early-warning anomaly`: `APPROVE` como senal de revision, no decision final.
- `Ensemble scenario gate`: `APPROVE` para combinar metodos y exponer desacuerdo.

## Regla Para Claudio/GEODIA

Claudio puede consumir `ObservationVector` como evidencia para `WitnessLog` y `ActionGate`. GEODIA/DUAT puede consumir `select_duat_predictive_methods()` para decidir que motor usar en laboratorio local.

Nada de esto ejecuta modelos externos, descarga pesos, publica resultados ni toma acciones reales.
