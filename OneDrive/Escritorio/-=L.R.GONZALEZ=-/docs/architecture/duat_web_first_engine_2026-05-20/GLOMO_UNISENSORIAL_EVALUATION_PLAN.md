# GLOMO_UNISENSORIAL_EVALUATION_PLAN

## Hipotesis

El glomo unisensorial puede funcionar como representacion intermedia compartida multimodal si se define como envelope tipado, auditable y con perdida controlada. No debe venderse como mejora hasta medirlo.

## Modelo propuesto

```txt
GLOMOFrame {
  frame_id,
  timestamp,
  channel_origin,
  spatial_ref,
  semantic_tokens,
  signal_features,
  confidence,
  missingness,
  contradiction,
  R,
  Phi_eff,
  grounding_refs,
  raw_ref_hash
}
```

Funcion:
- Normaliza camera/audio/text/world events a un lenguaje de observacion comun.
- Mantiene hash/referencia al raw source sin cargar raw media por defecto.
- Alimenta `SharedReality`.

## Riesgo

- Puede mejorar memoria/coherencia por compresion.
- Puede empeorar grounding si elimina rasgos de canal.
- Puede esconder contradicciones si el envelope es demasiado agresivo.

## Benchmark

Comparar 3 arquitecturas:

1. Baseline late-fusion multimodal tradicional.
2. GLOMO mid-fusion unisensorial.
3. Hibrido: GLOMO + retention selectiva de rasgos por canal.

Datasets locales:
- fixture sintetico de Wabi multimodal.
- escena DUAT con eventos visuales, audio proxy y texto.
- WorldState con contradicciones inducidas.

Metricas:
- Latencia por frame/evento.
- Memoria pico.
- Costo compute/token si aplica.
- Coherencia multimodal.
- Grounding contra evidencia.
- Resolucion de contradicciones.
- Estabilidad de replay.
- Task success en agentes.

Decision gate:
- Adoptar solo si gana en al menos 3 metricas sin perder grounding/replay.

