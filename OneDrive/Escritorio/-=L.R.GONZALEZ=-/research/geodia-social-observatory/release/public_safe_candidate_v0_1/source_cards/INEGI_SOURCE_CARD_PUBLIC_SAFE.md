# INEGI Source Card - Public-Safe Summary

package_id: GEODIA_PUBLIC_SAFE_PACKAGE_CANDIDATE_v0.1
publication_gate: BLOCK

## Source

- Name: INEGI ENOE indicadores estrategicos mensuales.
- Official data URL: https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/tabulados/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx
- Official discovery URL: https://www.inegi.org.mx/app/descarga/default.html
- Terms URL: https://www.inegi.org.mx/inegi/terminos.html
- Access date: 2026-05-14.
- Format at source: XLSX.

## Public-safe handling

- Raw XLSX is not included in this candidate package.
- Internal file paths, workbook extraction logs, and raw data files are excluded.
- License status remains `TERMS_DOCUMENTED_HUMAN_REVIEW_REQUIRED`.
- Source intake used network access only in the internal fixture creation step; harmonization runtime remains offline.

## Technical caveat

INEGI unemployment is treated as `STRONG_PROXY`, not `EXACT`, in the internal GEODIA crosswalk.

## Attribution draft

Fuente: INEGI, Encuesta Nacional de Ocupacion y Empleo (ENOE), Indicadores estrategicos mensuales. Procesamiento propio para fixture tecnico GEODIA.
