# Fragmentos / Calibracion Human Publication Gate Packet - 2026-05-22

PublicationGate: BLOCK
ActionGate: REVIEW_HUMAN_EDITORIAL

Este packet no publica, no sube, no despliega, no modifica Gumroad/KDP/web y
no contiene excerpts de manuscritos. Resume evidencia local y prepara una
revision humana/comercial para decidir si alguno de los dos libros avanza a
staging publico.

## Estado local verificado

| libro | export interno | QA automatizado | estado |
|---|---|---|---|
| `03_FRAGMENTOS` | `books\editorial\internal_exports\FRAGMENTOS_INTERNAL_EXPORT_2026-05-22` | Word pages `688`, rendered pages `688`, blank `0`, edge `0` | LISTO_PARA_REVIEW_HUMANO |
| `04_CALIBRACION` | `books\editorial\internal_exports\CALIBRACION_INTERNAL_EXPORT_2026-05-22` | Word pages `477`, rendered pages `477`, blank `0`, edge `0` | LISTO_PARA_REVIEW_HUMANO |

Evidencia:

- `qa_artifacts\editorial_docx_word_visual_qa\EDITORIAL_DOCX_WORD_FULL_QA_20260522\EDITORIAL_DOCX_WORD_VISUAL_QA_REPORT_2026-05-22.md`
- `books\editorial\internal_exports\FRAGMENTOS_INTERNAL_EXPORT_2026-05-22\INTERNAL_EXPORT_MANIFEST.json`
- `books\editorial\internal_exports\CALIBRACION_INTERNAL_EXPORT_2026-05-22\INTERNAL_EXPORT_MANIFEST.json`

## Decision humana requerida

Antes de cualquier accion externa, una persona debe decidir:

| decision | Fragmentos | Calibracion |
|---|---|---|
| Avanza a staging publico | REVIEW | REVIEW |
| Titulo comercial final | REVIEW | REVIEW |
| Precio ebook | REVIEW | REVIEW |
| Plataforma inicial | REVIEW | REVIEW |
| Portada public-safe | REVIEW | REVIEW |
| Metadata/listing final | REVIEW | REVIEW |
| Muestra publica permitida | REVIEW | REVIEW |
| Revision legal/comercial | REVIEW | REVIEW |

## Draft de metadata public-safe

### Fragmentos

- Titulo base: `MEDIOEVO: Fragmentos`
- Serie: `MEDIOEVO`, libro `3`
- Idioma: `es`
- Short description:
  `Un volumen MEDIOEVO sobre piezas, memoria parcial y la reconstruccion de una continuidad que nunca llega completa.`
- Long description:
  `Fragmentos presenta una entrada literaria de MEDIOEVO centrada en rastros, partes y recomposicion. Su promesa publica debe mantenerse contenida: una lectura sobre ordenar senales incompletas sin convertir la incertidumbre en certeza falsa.`
- Keywords:
  `medioevo`, `fragmentos`, `memoria`, `archivo`, `reconstruccion`, `ficcion literaria`, `observacion`
- Categorias candidatas:
  `Fiction / Literary`, `Fiction / Science Fiction / General`, `Fiction / Psychological`
- Precio placeholder:
  `USD 4.99`, `MXN 89`, `EUR 4.49`

### Calibracion

- Titulo base: `MEDIOEVO: Calibracion`
- Serie: `MEDIOEVO`, libro `4`
- Idioma: `es`
- Short description:
  `Una entrega MEDIOEVO sobre ajuste, criterio y el costo de decidir desde estados incompletos.`
- Long description:
  `Calibracion conecta el costado narrativo de MEDIOEVO con un lenguaje humano de criterio, ajuste y memoria. El copy publico debe quedarse en terreno literario y evitar promesas de ciencia validada, AGI, fisica o metodologia propietaria.`
- Keywords:
  `medioevo`, `calibracion`, `criterio`, `decision`, `memoria`, `observacion`, `ficcion especulativa`
- Categorias candidatas:
  `Fiction / Science Fiction / General`, `Fiction / Literary`, `Technology & Engineering / Social Aspects`
- Precio placeholder:
  `USD 4.99`, `MXN 89`, `EUR 4.49`

## Brief de portada public-safe

| libro | direccion visual | evitar |
|---|---|---|
| Fragmentos | archivo, piezas, mapa reconstruido, memoria parcial, composicion de fragmentos sin texto legible del manuscrito | texto de paginas internas, diagramas privados, lore protegido, personajes/asset RPG/TCG |
| Calibracion | instrumento, alineacion de senal, umbral, ajuste fino, escala o patron abstracto sobrio | formulas, runtime internals, claims de fisica/metodo propietario, logos internos |

Requisitos minimos de portada antes de staging:

- Imagen final con procedencia registrada.
- Dimension/formato revisado para plataforma destino.
- Sin texto privado, secretos, diagramas internos ni assets RPG/TCG.
- Derechos/licencia claros.
- Aprobacion humana antes de usar en tienda.

## Matriz de accion

| accion | gate | estado |
|---|---|---|
| Mantener exports internos y QA local | APPROVE_LOCAL_EVIDENCE | CERRADO |
| Preparar copy/metadata interna | APPROVE_LOCAL_METADATA | CERRADO_EN_ESTE_PACKET |
| Crear portada nueva o seleccionar asset existente | REVIEW_ASSET_PRODUCTION | PENDIENTE |
| Crear staging publico local allowlisted | REVIEW_PUBLIC_STAGING | PENDIENTE |
| Subir a KDP/Gumroad/web/redes | BLOCK_PUBLICATION | BLOQUEADO |
| Git push/deploy/public ZIP | BLOCK_PUBLICATION | BLOQUEADO |

## Checklist para abrir staging publico local

Solo si hay decision humana:

1. Elegir un libro: Fragmentos o Calibracion, no ambos a la vez.
2. Confirmar titulo, precio, plataforma y copy.
3. Confirmar portada public-safe o crear brief definitivo.
4. Definir muestra publica exacta, si aplica.
5. Crear carpeta de staging local allowlisted.
6. Copiar solo artefactos aprobados al staging; no usar globs.
7. Ejecutar secret scan focal.
8. Ejecutar boundary scan: no manuscrito completo si la decision es preview.
9. Registrar ActionGate por destino.
10. Mantener upload/push/deploy bloqueados hasta instruccion explicita por target.

## Recomendacion operativa

Siguiente paso mas seguro: elegir un solo candidato para portada public-safe.
Fragmentos es mas bajo riesgo por enfoque literario/archivo. Calibracion es
potente, pero requiere mas cuidado para no sonar a claim tecnico o teoria
propietaria.

## Estado final

No hay accion externa ejecutada. Este packet deja el material listo para una
decision humana informada, no para publicacion automatica.
