# DUAT Multidimensional Filter Ecology v0.1

publication_gate: BLOCK
external_publication: false

## Premisa corregida

Mas informacion sin arquitectura puede aumentar R. Mas informacion con filtros
especializados puede aumentar `H_eff` si cada fuente, residuo y metodo entra con
ruta, peso, gate y falsificador.

DUAT no usa un filtro unico. Usa una ecologia de filtros por dimension de R.

## R vector

- `R_cognitive`: ambiguedad, asociaciones no lineales, saltos conceptuales.
- `R_entertainment`: distraccion, estimulo, viralidad y captura de atencion.
- `R_social_manipulative`: propaganda, presion social, framing, tribalismo.
- `R_temporal`: datos viejos, rezagos, drift y cambios de schema.
- `R_source`: procedencia debil, licencia dudosa o reproducibilidad baja.
- `R_contra`: contradicciones entre senales o instrucciones.
- `R_sensitive`: secretos, PII, politica electoral, legal o material privado.
- `R_model`: overfit, leakage, mala calibracion o causalidad no probada.
- `R_user_style`: forma cognitiva, metafora, intuicion y preferencia de salida.
- `R_agent_operational`: instrucciones confusas para agentes.

`R_structured` no se suma automaticamente como ruido. Se conserva si puede
traducirse a decision, prioridad, estilo, interfaz o hipotesis verificable.

## Flujo

Input humano + datos externos + senales predictivas pasan por:

1. Filter Ecology Router.
2. Dual-Lane Filter.
3. Specialized Filter Bank.
4. Recomposition Layer.
5. Predictive Registry.
6. ForecastGate + Backtest.
7. CleanResult + UserAdaptedResult + Handoff.

## Formula

```text
R_vector = [
  R_cognitive,
  R_entertainment,
  R_social_manipulative,
  R_temporal,
  R_source,
  R_contra,
  R_sensitive,
  R_model,
  R_user_style,
  R_agent_operational
]

R_total = weighted_norm(R_vector, task_context)
H_eff = H_raw * FilterFit * SourceQuality * Freshness * Coverage * Phi_eff * CalibrationScore
FilterFit = matched_filters / required_filters
```

## Gates

- `BLOCK`: secretos, PII, material privado, prediccion electoral, ranking de
  personas, causalidad no demostrada o fuente no primaria como verdad.
- `REVIEW`: residuo estructurado alto sin traduccion operativa, falta de
  SourceCard, falta de backtest, R medio, licencia incompleta.
- `APPROVE`: senal limpia, residuo clasificado, filtros requeridos presentes y
  output claro.
