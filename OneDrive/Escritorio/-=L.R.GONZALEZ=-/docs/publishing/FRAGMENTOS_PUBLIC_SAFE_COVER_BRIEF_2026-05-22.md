# Fragmentos Public-Safe Cover Brief - 2026-05-22

PublicationGate: BLOCK
ActionGate: REVIEW_ASSET_PRODUCTION

Este brief prepara direccion visual para revision humana. No genera imagen, no
selecciona asset existente, no usa manuscrito, no toca Gumroad/KDP/web y no
autoriza publicacion.

## Libro

- id: `03_FRAGMENTOS`
- titulo base: `MEDIOEVO: Fragmentos`
- serie: `MEDIOEVO`
- uso previsto: portada candidata para revision interna, no tienda publica
- estado local: export interno y QA automatizado completos
- paquete relacionado:
  `docs\publishing\FRAGMENTOS_CALIBRACION_HUMAN_PUBLICATION_GATE_PACKET_2026-05-22.md`

## Direccion visual

Una composicion sobria de archivo reconstruido: piezas dispersas que empiezan a
formar un mapa o constelacion de memoria. Debe sentirse literaria, misteriosa y
humana, no tecnica ni cientifica. La imagen debe sugerir recomposicion y rastro,
no explicar lore privado.

## Elementos permitidos

- Fragmentos abstractos de papel sin texto legible.
- Mapa incompleto o cuadricula editorial sin coordenadas reales.
- Luz tenue, polvo, marcas de archivo o materialidad de biblioteca.
- Formas modulares que sugieran memoria parcial.
- Paleta contenida: negro, marfil, azul profundo, gris papel, acento oro viejo
  o rojo muy discreto.

## Elementos prohibidos

- Texto real del manuscrito o paginas internas legibles.
- Diagramas privados, formulas, runtime, Observacionismo tecnico o claims.
- Personajes, assets o iconografia RPG/TCG.
- Logos internos, rutas locales, capturas de pantalla, prompts o metadata
  sensible.
- Simbolos que prometan ciencia validada, AGI, prediccion o metodo propietario.

## Copy de portada candidato

- Titulo: `FRAGMENTOS`
- Serie pequeña: `MEDIOEVO III`
- Autor: `Luis Rene Gonzalez`

No incluir subtitulos tecnicos ni frases de marketing en la primera version.

## Requisitos tecnicos antes de producir asset

- Registrar fuente/procedencia del asset.
- Exportar master editable privado y PNG/JPEG final de revision.
- Verificar dimensiones segun plataforma destino antes de staging.
- Ejecutar metadata strip si se usa imagen raster.
- Ejecutar secret/boundary scan sobre carpeta de staging local.
- Mantener `PublicationGate=BLOCK` hasta aprobacion humana por destino.

## Prompt visual interno opcional

Usar solo como guia para un diseñador o generador local aprobado:

> Portada literaria sobria para una novela llamada Fragmentos, archivo
> reconstruido, piezas abstractas de papel sin texto legible formando un mapa
> incompleto, atmosfera de biblioteca silenciosa, memoria parcial,
> composicion elegante, alto contraste suave, paleta negro marfil azul profundo
> con acento oro viejo, sin personas, sin texto interno, sin simbolos tecnicos,
> sin diagramas, sin ciencia-ficcion estridente.

## Decision humana requerida

- Aprobar o modificar direccion visual.
- Confirmar si se genera asset nuevo o se selecciona asset existente fichado.
- Confirmar plataforma objetivo antes de dimensiones finales.
- Confirmar si el primer staging sera solo mockup interno o portada lista para
  tienda.

## Estado final

Brief listo para revision. No se creo ni publico ningun asset.
