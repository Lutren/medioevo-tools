# Hipocampo / Handoff Persistence Engine

## Principio

La continuidad no depende de recordar todo. Depende de externalizar
lo mínimo necesario para reconstruir.

## Mecanismo

1. **Predicción:** El sistema predice el siguiente estado desde memoria OSIT.
2. **Residuo:** Calcula diferencia entre predicción y realidad.
3. **Compresión:** Guarda solo el residuo (vector comprimido).
4. **Reconstrucción:** Estado = Predicción + Residuo.

## Ventaja

- Estado completo: ~10KB
- Residuo comprimido: ~200 bytes
- Ratio de compresión: 50:1

Ideal para sesiones que guardan en localStorage o disco.
