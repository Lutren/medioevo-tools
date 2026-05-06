# Curador SETO Tree Absorption

Generated UTC: `2026-05-06T07:06:27.021582+00:00`

Estado: `FICHADO / ABSORBIDO_A_ATLAS / LIMPIEZA_SEGURA_PARCIAL`

## Rutas

- `documentos`: `C:\Users\L-Tyr\OneDrive\Documentos`

## Resumen

- Archivos registrados: `56`
- Duplicados exactos detectados: `4` archivos en grupos duplicados
- Eliminados seguros en este pase: `3`

## Estados

| estado | archivos |
|---|---:|
| `CANONICAL_DUPLICATE_KEEP` | 2 |
| `FICHADO` | 49 |
| `RETIRADO_A_QUARANTINE` | 3 |
| `REVIEW` | 2 |

## Carriles

| carril | archivos |
|---|---:|
| `cleanup` | 3 |
| `curaduria` | 37 |
| `duat-geodia` | 16 |

## Decisiones

| decision | archivos |
|---|---:|
| `ABSORB_TO_ATLAS` | 49 |
| `DELETE_REGENERABLE_AFTER_LOG` | 3 |
| `KEEP_CANONICAL` | 2 |
| `REVIEW_DUPLICATE` | 2 |

## Veredicto

- La absorcion de este pase crea fichas por archivo y manifest estructurado.
- `Downloads` se trata como zona de amenaza: nada descargado se ejecuta, extrae o publica antes de clasificar riesgo.
- Lo unico que puede retirarse automaticamente es duplicado exacto o basura regenerable con hash y gate.
- Los documentos unicos, privados, de claims fuertes o con frontera de publicacion quedan `REVIEW` o `BLOQUEADO`; no se borran.

## Archivos eliminados

| sha256 | ruta retirada | copia canonica | motivo |
|---|---|---|---|
| `954B525BE189A7FE` | `C:\Users\L-Tyr\OneDrive\Documentos\desktop.ini` | `` | `DELETE_REGENERABLE_AFTER_LOG` |
| `3D7A76CEE046F3AD` | `C:\Users\L-Tyr\OneDrive\Documentos\Zoom\2025-08-11 08.56.03 Luis Renè Gonzalez's Zoom Meeting\audio1657680373.m4a.tmp` | `` | `DELETE_REGENERABLE_AFTER_LOG` |
| `82CB1DC78332F30A` | `C:\Users\L-Tyr\OneDrive\Documentos\Zoom\2025-08-11 08.56.03 Luis Renè Gonzalez's Zoom Meeting\video1657680373.mp4.tmp` | `` | `DELETE_REGENERABLE_AFTER_LOG` |

## Siguiente limpieza permitida

1. Revisar `REVIEW_DUPLICATE` que no estaban en carpeta archive/copia.
2. Convertir fuentes unicas grandes en fichas de concepto antes de archivo frio.
3. No publicar ni abrir OSIT-QG/OSIT-AG/GEODIA sin falsadores y claims boundary.
4. Si una carpeta queda solo como archivo frio ya absorbido, moverla completa en una fase separada con rollback.
