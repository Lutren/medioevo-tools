# GEODIA Claims Boundary

release_id: GEODIA_INTERNAL_RELEASE_RC_v0.1
publication_gate: BLOCK

## CERTEZA

- GEODIA harmonization corre offline con tres fuentes: World Bank, Eurostat e INEGI ENOE.
- Los fixtures oficiales estan descargados o documentados con fuente, manifest y hash cuando aplica.
- El crosswalk usa clases conservadoras como `STRONG_PROXY`, `REVIEW` y `NOT_COMPARABLE`.
- QA local es reproducible por comando.
- El modulo bloquea ranking, prediccion y causalidad como claims externos.

## INFERENCIA

- GEODIA puede funcionar como capa tecnica para armonizacion geosocial offline.
- INEGI ENOE desempleo funciona como `STRONG_PROXY` tecnico para la familia de desempleo, sujeto a diferencias metodologicas.
- La comparacion multi-fuente es util para validar forma, trazabilidad y compatibilidad, no para concluir jerarquias sociales.

## INCOGNITA

- Revision legal final de terminos y redistribucion.
- Equivalencia metodologica estricta entre instituciones y series.
- Robustez de la capa con mas fuentes, periodos y paises.
- Validez para dominios distintos a los indicadores actuales.

## BLOQUEO

- Claim bloqueado: GEODIA predice votos o resultados electorales.
- Claim bloqueado: INEGI, World Bank o Eurostat validaron GEODIA.
- Claim bloqueado: una relacion social o politica queda causada por el output.
- Claim bloqueado: `STRONG_PROXY` o `REVIEW` equivalen a `EXACT`.
- Claim bloqueado: el RC interno esta listo para publicacion externa.
- Claim bloqueado: la licencia comercial final esta aprobada sin revision humana/legal.
