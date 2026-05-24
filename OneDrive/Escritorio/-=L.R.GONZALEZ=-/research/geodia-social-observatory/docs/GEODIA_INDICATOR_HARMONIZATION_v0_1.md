# GEODIA Indicator Harmonization v0.1

Estado: `LOCAL_QA_ONLY / PUBLICATION_BLOCK`.

Esta capa permite comparar compatibilidad tecnica entre fixtures oficiales
offline. No autoriza ranking, causalidad, prediccion social, inferencia
electoral, inferencia personal, publicacion externa ni claims cientificos.

## Que Se Puede Comparar

- Si dos indicadores comparten `canonical_indicator_id`, se puede evaluar su
  compatibilidad tecnica.
- Si las unidades, frecuencia y polaridad son cercanas pero no identicas, el
  resultado debe ser `STRONG_PROXY`, `WEAK_PROXY` o `REVIEW`.
- Los valores originales pueden revisarse dentro del fixture offline con hash.
- La salida interpretativa se mantiene como `INFERENCIA`.

## Que No Se Puede Comparar

- No se comparan paises como ranking.
- No se concluye que Mexico este mejor o peor que Alemania.
- No se infiere causalidad social desde movimientos de indicadores.
- No se mezclan indicadores de dominios distintos; desempleo contra esperanza
  de vida, por ejemplo, es `NOT_COMPARABLE`.
- No se usan APIs con credenciales ni FRED en esta capa.

## Armonizacion Tecnica No Es Conclusion Social

La armonizacion tecnica solo dice si dos columnas pueden entrar al mismo
contrato operativo. Una conclusion social requeriria hipotesis, diseno
estadistico, licencia, falsadores, contexto historico y revision humana. Esta
v0.1 no hace eso.

## Reglas De Polaridad

- `positive`: valores mayores se conservan como mejora tecnica.
- `negative`: valores mayores significan deterioro tecnico; para calculos
  internos se puede invertir el signo, pero se preserva la polaridad original.
- `neutral` y `review`: no se transforman sin decision posterior.

Ejemplo: desempleo conserva `polarity_canonical=negative`; un valor `3.2`
puede representarse como `-3.2` en una vista alineada a beneficio, sin borrar el
valor bruto.

## Reglas De Unidad

- `unit_original` conserva la unidad del proveedor.
- `unit_canonical` solo agrupa unidades suficientemente cercanas para QA.
- Si el significado cambia, como PIB per capita contra PIB agregado, el
  indicador queda en `REVIEW`.
- No se convierten unidades con formula no documentada.

## Reglas De Frecuencia Temporal

- Esta v0.1 solo aprueba comparabilidad directa para series `annual`.
- Series mensuales, trimestrales, irregulares o con cortes deben quedar en
  `REVIEW` hasta definir agregacion.
- El rango 2018-2023 se conserva como parte de la evidencia, no como garantia
  de equivalencia semantica.

## Reglas De Fuente

- Cada fuente debe estar en allowlist GEODIA.
- Cada fixture debe ser offline, hashable y sin credenciales.
- `publication_gate=BLOCK` es obligatorio en crosswalk, reportes y salidas.
- Licencia y terminos quedan en REVIEW antes de redistribucion publica o
  comercial.

## Falsificadores

- Un indicador dudoso marcado `EXACT` invalida la capa v0.1.
- Un reporte con ranking entre paises invalida la capa v0.1.
- Un reporte con causalidad, prediccion o inferencia electoral/personal queda
  `BLOCK`.
- Cualquier uso de credenciales, FRED, secretos o rutas privadas exportables
  queda `BLOCK`.
- Cualquier artifact nuevo sin `publication_gate=BLOCK` queda `FAIL`.

## Ejemplos 2026-05-14

| dominio | World Bank Mexico | Eurostat Germany | clase v0.1 | razon |
|---|---|---|---|---|
| desempleo | `SL.UEM.TOTL.ZS` | `une_rt_a` | `STRONG_PROXY` | Ambos son tasas de desempleo, pero difieren en definicion y edad. |
| economia | `NY.GDP.PCAP.KD.ZG` | `tec00115` | `REVIEW` | Per capita real GDP growth no es igual a real GDP volume growth agregado. |
| demografia | `SP.DYN.LE00.IN` | `demo_mlexpec` | `STRONG_PROXY` | Ambos aproximan esperanza de vida al nacer total, con caveats de fuente/status. |

## Claim Boundary

Claim permitido: "la capa v0.1 detecta compatibilidad tecnica entre indicadores
de fixtures oficiales offline".

Claims bloqueados: "GEODIA predice epocas sociales", "Alemania supera a
Mexico", "World Bank y Eurostat validan DUAT" o cualquier causalidad social.
