# DUAT Brain OS v1.4.0
## Fingerprint: DUAT-v1.4.0-BRAIN-OS-COMPLETO

**Estado:** INTERNO_LOCAL / NO_PUBLICAR_SIN_GATE  
**ActionGate:** REVIEW → local reversible

---

## Propósito

Sistema nervioso del motor MEDIOEVO/OSIT. Conecta las 4 cortezas operativas
(lenguaje, audio, visual, matemática) con 8 subsistemas subcorticales.

Para artistas pobres con poca CPU: cada subsistema puede activarse/desactivarse
individualmente. No todos corren a la vez.

---

## Mapa Cerebral

| Parte | Motor | Función | Prioridad |
|-------|-------|---------|-----------|
| Corteza Auditiva | Audio Engine v1.2.1 | Sonido procedural | Crítico |
| Corteza Visual | Render CPU v1.3.0 | Pixel-art, luz, física | Crítico |
| Corteza Matemática | FibMob/EML/OSIT | Matemáticas del motor | Crítico |
| Área de Broca | MEDIOEVO tools | Lenguaje | Crítico |
| **Hipocampo** | **Handoff Persistence** | Memoria comprimida por residuo | **Crítico** |
| **Prefrontal** | **ActionGate Executive** | Gobierno operativo, recursos | **Crítico** |
| **Atención** | **GhostGate** | Filtro inmune de información | **Crítico** |
| Cerebelo | Quaternary Timing Core | Reloj maestro τ | Alto |
| Inmune | TruthGate Test Engine | Falsificadores automáticos | Alto |
| Homeostasis | Resource Regulator | CPU, memoria, batería | Alto |
| Cuerpo Calloso | Cross-Modal Transduction | Luz↔Audio↔Física | Medio |
| Propiocepción | Body Schema | Cámara, atención, sensores | Medio |

---

## Principios

1. **Hipocampo:** No guarda todo. Guarda solo el residuo que los filtros FBI no pudieron predecir. Reconstrucción desde predicción + residuo.
2. **Prefrontal:** Si R_system > 0.5, bloquea nuevas tareas. Si CPU > 80%, baja LOD de render.
3. **GhostGate:** Si la señal aumenta R, se bloquea antes de llegar a las cortezas.
4. **Cerebelo:** Un τ maestro para todos los motores. No cada uno con su delta.
5. **Inmune:** Cada claim tiene test + falsificador. Si falla, BLOQUEO.
6. **Homeostasis:** Si el cuerpo muere (CPU 100%), la mente no importa.
7. **Cuerpo Calloso:** Un campo que se filtra de diferentes maneras. No canales separados.
8. **Propiocepción:** Sin cuerpo no hay perspectiva. Sin perspectiva no hay mundo.

---

## Handoff

**Fingerprint:** DUAT-v1.4.0-BRAIN-OS-COMPLETO  
**Brief:** 8 subsistemas subcorticales implementados: Hipocampo (handoff comprimido), Prefrontal (gobierno operativo), Atención (GhostGate), Cerebelo (timing global), Inmune (TruthGate), Homeostasis (regulador de recursos), Cuerpo Calloso (cross-modal), Propiocepción (body schema).  
**NextAction:** Integrar con motor v1.3.0 y audio v1.2.1. Validar en escena de prueba.
