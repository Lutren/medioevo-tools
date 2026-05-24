# RISKS

## 2026-05-22 - Smallville-DUAT Evidence Refresh

- La evidencia sintetica no debe presentarse como validacion predictiva real.
- Los planes remotos del modulo no autorizan ejecucion externa.
- Los artefactos QA no son paquete publicable ni dataset redistribuible.

| id | severidad | riesgo | mitigacion |
|---|---|---|---|
| DS-R-001 | ALTA | Subir workspace privado a Colab/Kaggle | notebook manual con `publication_gate=BLOCK`; crear export sanitizado antes de uso |
| DS-R-002 | ALTA | Confundir simulacion sintetica con prediccion social real | claims `NOT_ALLOWED`, `NOT_CLAIMED`, `AUDITABLE_NOT_ABSENT` y falsadores |
| DS-R-003 | MEDIA | SimScale usado para agentes sociales | constraint `physical_simulation_only`; solo microclima/CFD/FEA |
| DS-R-004 | MEDIA | Datos reales sin licencia/comparabilidad | SourcePack con hash, licencia, comparability y leakage preflight |
| DS-R-005 | MEDIA | GPU/cloud genera dependencia operativa | `local_cpu` sigue como ruta canonica reproducible |
| DS-R-006 | MEDIA | Ledgers v0.2 grandes por 1440 ticks x 25 agentes | conservar como artefactos auditables; no incluir en publicacion |
| DS-R-007 | ALTA | Confundir SignalSourcePack sintetico con datos reales | boundary `uses_real_data=false`, no-real-data falsifier y PublicationGate BLOCK |
| DS-R-008 | MEDIA | Contradicciones ambientales ocultas por promedio | falsador `contradiction_preservation`; gate minimo REVIEW |
