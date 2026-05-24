# PENDIENTES_MASTER Reconciliation - 2026-05-17

Estado: cierre local de reconciliacion. No autoriza publicacion, push, deploy,
Gumroad, KDP, redes, ZIP publico ni exposicion de manuscritos privados.

## Fuente revisada

- `PENDIENTES_MASTER.md` raiz tenia 7 checkboxes de cola local y 3 checkboxes
  de bloqueos permanentes.
- `docs/pending/PENDING_REVIEW_LATEST.md` reporto `active_dedup=19` y
  `claudio_open=0`.
- `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/observacionista/active_workpack.json`
  reporto `selected_items=[]` y COMMS `action_gate=BLOCK`.
- `-=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md` no tiene pendiente local
  abierto en el carril Obsidian/LLM Wiki/MemPalace.

## Reconciliacion

| pendiente anterior | resultado | razon |
|---|---|---|
| Review legal/humana WDI | REVIEW_EXTERNAL | no se puede cerrar localmente; World Bank/WDI sigue bloqueado para redistribucion o claim externo |
| Review metodologica WDI | CERRADO_LOCAL_REVIEW | v0.8.1 ya genero governance review, DataGate REVIEW y BacktestOpenGate REVIEW_ONLY_DRY_RUN |
| Review comercial Deriva/Fragmentos/Calibracion | CERRADO_PAQUETE_INTERNO | se creo paquete local de revision; la aprobacion humana/comercial sigue fuera de este cierre |
| Completar assets locales de tres libros | REVIEW_ASSET_PRODUCTION | se creo checklist/brief local; no se generaron exports ni portadas finales |
| Mantener otros 31 libros como backlog | CERRADO_INVENTARIO | control board de 35 filas y missing-assets report ya registran el backlog |
| Resolver o aislar arbol git sucio | CERRADO_AISLAMIENTO_LOCAL | se documento el estado y el write-set; no se hizo staging ni commit |
| MTS con preregistro previo | CERRADO_LOCAL_SINTETICO | el cierre del 2026-05-15 registro preregistro, fixtures sinteticos y tests sin datos reales |
| Publicacion/upload/deploy/push/Gumroad/KDP/redes/ZIP publico | BLOCK_PUBLICATION | gate permanente; no debe contar como tarea local ejecutable |
| Exponer manuscritos/canon/secretos | BLOCK_PRIVACY | gate permanente; no debe contar como tarea local ejecutable |
| Sensores/datos personales/telemetria/biometria en MTS | BLOCK_MTS_REAL_DATA | gate permanente; no debe contar como tarea local ejecutable |

## Evidencia principal

- `docs/ops/MEDIOEVO_LOCAL_QUEUE_CLOSEOUT_2026-05-15.md`
- `docs/publishing/BOOK_METADATA_SPRINT_DERIVA_FRAGMENTOS_CALIBRACION_2026-05-15.md`
- `docs/publishing/BOOK_PUBLICATION_CONTROL_BOARD_2026-05-15.md`
- `docs/publishing/BOOK_PUBLICATION_MISSING_ASSETS_2026-05-15.md`
- `research/duat-predictive-registry/reports/duat-world-bank-wdi-governance-review-v0-8-1.json`
- `TEST_REPORT.md`
- `ACTION_GATES.md`

## Resultado operativo

`PENDIENTES_MASTER.md` queda como estado de gates y cierres con evidencia, no
como lista de checkboxes abiertos. La cola viva debe medirse con:

```powershell
python tools\release\pending_review.py --write --quiet
```

El siguiente trabajo local recomendado es una de estas dos rutas:

1. Un export interno de un solo libro candidato, sin upload.
2. Briefs/asset checklist de portada para los tres candidatos, sin usar assets privados no fichados.
