# Book Release Review Packet - Deriva, Fragmentos, Calibracion

PublicationGate: BLOCK
ActionGate: APPROVE_LOCAL_REVIEW_PACKET_ONLY

No se leyeron ni copiaron manuscritos completos. No se modifico Gumroad, KDP,
medioevo.space, redes, deploy, ZIP publico ni store page.

## Entrada

- Metadata base: `docs/publishing/BOOK_METADATA_SPRINT_DERIVA_FRAGMENTOS_CALIBRACION_2026-05-15.md`
- Control board: `docs/publishing/BOOK_PUBLICATION_CONTROL_BOARD_2026-05-15.md`
- Faltantes: `docs/publishing/BOOK_PUBLICATION_MISSING_ASSETS_2026-05-15.md`
- Cola local: `docs/publishing/BOOK_PUBLICATION_NEXT_ACTIONS_2026-05-15.md`

## Estado por libro

| id | titulo | estado local | siguiente accion segura |
|---|---|---|---|
| `02_DERIVA` | MEDIOEVO: Deriva | metadata draft existe; falta export, portada, precio humano y store approval | preparar export interno EPUB/PDF desde fuente editorial aprobada o brief de portada |
| `03_FRAGMENTOS` | MEDIOEVO: Fragmentos | metadata draft existe; falta export, portada, precio humano y store approval | preparar export interno EPUB/PDF desde fuente editorial aprobada o brief de portada |
| `04_CALIBRACION` | MEDIOEVO: Calibracion | metadata draft existe; falta export, portada, precio humano y store approval | preparar export interno EPUB/PDF desde fuente editorial aprobada o brief de portada |

## Metadata revisable

### Deriva

- Enfoque: continuacion public-safe sobre perdida de rumbo, memoria,
  orientacion, continuidad y reconstruccion de sentido.
- Keywords base: `medioevo`, `ficcion especulativa`, `observacion`, `memoria`,
  `continuidad`, `sistemas`, `deriva`.
- Categoria candidata: Fiction / Science Fiction / General; Fiction / Literary;
  Philosophy / Mind & Body.
- Precio placeholder: USD 4.99 ebook, MXN 89 ebook, EUR 4.49 ebook.
- Riesgo de copy: no prometer ciencia validada, AGI, prediccion ni teoria
  propietaria.

### Fragmentos

- Enfoque: memoria parcial, partes, rastros y recomposicion de continuidad.
- Keywords base: `medioevo`, `fragmentos`, `memoria`, `archivo`,
  `reconstruccion`, `ficcion literaria`, `observacion`.
- Categoria candidata: Fiction / Literary; Fiction / Science Fiction / General;
  Fiction / Psychological.
- Precio placeholder: USD 4.99 ebook, MXN 89 ebook, EUR 4.49 ebook.
- Riesgo de copy: evitar convertir incertidumbre narrativa en certeza tecnica o
  promesa metodologica.

### Calibracion

- Enfoque: ajuste, criterio, residuo, memoria y decision desde estados
  incompletos.
- Keywords base: `medioevo`, `calibracion`, `criterio`, `decision`, `memoria`,
  `observacion`, `ficcion especulativa`.
- Categoria candidata: Fiction / Science Fiction / General; Fiction / Literary;
  Technology & Engineering / Social Aspects.
- Precio placeholder: USD 4.99 ebook, MXN 89 ebook, EUR 4.49 ebook.
- Riesgo de copy: no exponer runtime interno, formulas, diagramas privados ni
  claims fuertes.

## Checklist de export interno

Para cada libro:

- Fuente editorial aprobada identificada por ruta y hash.
- Export EPUB generado localmente.
- PDF de prueba generado localmente.
- DOCX interno solo si hace falta revision humana.
- KPF solo despues de cover/metadata review.
- EPUB revisado con validador local disponible.
- Secret/private-boundary scan focal antes de enviar a revision humana.
- No upload, no store edit, no public URL hasta gate nuevo.

## Briefs de portada public-safe

| libro | direccion visual | evitar |
|---|---|---|
| Deriva | umbral, navegacion, deriva, senal/ruido, orientacion perdida | simbolos privados, RPG/TCG, ciencia claim-heavy |
| Fragmentos | archivo, piezas, mapa reconstruido, memoria parcial | texto de manuscrito, diagramas privados, lore protegido |
| Calibracion | instrumento, alineacion de senal, umbral, ajuste fino | formulas, runtime internals, claims de fisica/metodo propietario |

## Decision pendiente humana

- Confirmar si los tres mantienen precio uniforme.
- Elegir el primer libro para export interno.
- Confirmar si las portadas se generan desde assets existentes fichados o desde
  briefs nuevos public-safe.
- Aprobar copy comercial antes de cualquier storefront.

## Proxima accion verificable

Elegir un solo libro candidato y crear su export interno EPUB/PDF con hash,
sin upload y con `PublicationGate=BLOCK`.
