# INEGI Source Card - GEODIA Third Official Fixture

ID: `GEODIA-INEGI-ENOE-MEX-2018-2023`

Nombre de fuente: Instituto Nacional de Estadística y Geografía (INEGI), Encuesta Nacional de Ocupación y Empleo (ENOE), indicadores estratégicos mensuales.

URL oficial: https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/tabulados/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx

URL de descubrimiento oficial: https://www.inegi.org.mx/app/descarga/default.html

URL de términos: https://www.inegi.org.mx/inegi/terminos.html

Fecha de acceso: 2026-05-14

Tipo de fuente: descarga oficial pública de tabulado estadístico.

Formato descargado: XLSX.

Archivo bruto local: `fixtures/source_intake/inegi/raw/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx`

SHA256 bruto: `0add6e88da29b8f5eddcafe889f94c353edaab8a9d5ec272565a55c84cae8bd5`

Tamaño bruto: `3746724` bytes.

Cobertura temporal fuente: 2005 Ene a 2026 Mar, según listado de Descarga Masiva.

Cobertura temporal fixture: 2018-2023, agregada como promedio anual de 12 valores mensuales por año.

Cobertura geográfica: Estados Unidos Mexicanos / México nacional.

Campos usados:
- `Tasa de desocupación`, hoja `1.2`, fila 289.
- `Tasa de participación`, hoja `1.2`, fila 287.
- `Tasa de informalidad laboral 1 (TIL1)`, hoja `1.2`, fila 297.

Licencia/términos encontrados:
- La página de Datos Abiertos de INEGI describe archivos de información estadística y geográfica con formato de Datos Abiertos bajo la Norma Técnica correspondiente.
- La página de Términos de uso de INEGI indica términos de libre uso de la información, preservación de metadatos, crédito a INEGI y no implicar aval, patrocinio o postura oficial de INEGI.
- Estado GEODIA: `REVIEW_TERMS_DOCUMENTED`; no se afirma permiso comercial final ni autorización de redistribución pública.

## GHOSTGATE

1. Fuente oficial usada: INEGI Descarga Masiva / ENOE indicadores estratégicos mensuales.
2. Descarga pública o token: descarga pública sin token; Banco de Indicadores API quedó fuera porque requiere token y `INEGI_API_TOKEN` no estaba disponible.
3. Términos/licencia encontrados: términos de libre uso documentados por INEGI; redistribución pública/comercial sigue en REVIEW.
4. Cobertura 2018-2023: sí, mediante serie mensual 2005-2026 y promedios anuales 2018-2023.
5. Fixture mínimo verificable: sí; hash bruto, ruta oficial, filas de workbook y conteos mensuales preservados.
6. Reversibilidad: sí; artefactos nuevos locales y crosswalk additive.
7. Riesgo de secretos/IP privada: bajo; no se usaron credenciales, no se imprimieron tokens y outputs usan rutas relativas.
8. publication_gate: `BLOCK`.

## CERTEZA

- La fuente y el archivo bruto provienen de dominio oficial INEGI.
- El archivo bruto fue descargado localmente y su SHA256 está registrado.
- El fixture deriva tres indicadores desde filas identificadas del workbook.
- La armonización permitida para INEGI se limita a desempleo como `STRONG_PROXY`, no `EXACT`.
- `publication_gate=BLOCK`.

## INFERENCIA

- El promedio anual de valores mensuales es una transformación técnica local para compatibilidad anual con fixtures World Bank/Eurostat.
- La tasa de desocupación ENOE es proxy fuerte, no equivalencia exacta, frente a unemployment-rate fixtures de otros proveedores.

## INCÓGNITA

- Revisión legal final de términos para publicación, distribución pública o uso comercial de este extracto GEODIA.
- Diferencias metodológicas exactas entre ENOE, World Bank ILO estimate y Eurostat por población/edad/metodología.

## BLOQUEO

- No publicar.
- No push/deploy/Gumroad/DNS/redes sociales.
- No ranking México vs Alemania ni ranking entre fuentes.
- No causalidad ni predicción social/electoral/personal.
- No afirmar que INEGI validó GEODIA.
- No afirmar licencia comercial aprobada.

## Decisión de uso

`APPROVE_LOCAL_WITH_OFFICIAL_SOURCE` para fixture local offline y QA técnica.

`publication_gate=BLOCK` para todo uso externo.

## Atribución recomendada

Fuente: INEGI, Encuesta Nacional de Ocupación y Empleo (ENOE), indicadores estratégicos mensuales, archivo `enoe_indicadores_estrategicos_2005_2026_mensual.xlsx`, consultado el 2026-05-14.
