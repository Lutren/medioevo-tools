# Global License Review Packet - 2026-05-06

Estado: `LEGAL_REVIEW_REQUIRED`

Este documento no es asesoria legal. Su funcion es separar la decision de
licencia global de los releases locales verificables.

## Evidencia

| fuente | lectura |
|---|---|
| `PRODUCT_MAP.md` | existen carriles `OPEN`, `COMMERCIAL`, `INTERNAL_RESEARCH`, `BOOKS_EDITORIAL`, `PRIVATE` y `VENDOR_REVIEW` |
| `VISIBILITY_MATRIX.md` | la publicacion se decide por ruta/target, no por workspace completo |
| `docs/legal/COMMERCIAL_LEGAL_REVIEW_PACKET_2026-05-06.md` | los productos comerciales siguen en revision legal antes de venta amplia |
| `RELEASE_CHECKLIST.md` | no existe licencia global decidida para todo el workspace |

## Postura Segura Hasta Revision

| capa | postura operativa actual | no hacer |
|---|---|---|
| `packages/open-dev/*` | MIT solo cuando el paquete tiene `LICENSE`, notices, tests y secret scan focalizado | aplicar MIT al workspace completo |
| `apps/commercial/*` | propietario/comercial con revision legal por producto | abrir checkout sin EULA/terminos/privacidad |
| libros/canon | propietario/editorial; publicar solo muestras aprobadas | regalar libros completos |
| research interno | interno hasta claims/licencia/fuentes revisadas | publicar como ciencia validada |
| privado/juego/TCG | excluido de releases publicos | copiar a paquetes Claudio/open-dev |
| vendors/terceros | revision de licencia y notices | vendorear como propio sin revision |

## Decisiones Pendientes

- Confirmar si habra un documento central de licencia por capas o solo
  licencias por target.
- Confirmar texto publico para la frontera `MIT + propietario`.
- Confirmar si los paquetes open-dev deben compartir una plantilla unica de
  `LICENSE`, `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md` y `THIRD_PARTY_NOTICES.md`.
- Confirmar EULA/terminos/privacidad/reembolso por app comercial antes de venta
  amplia.
- Confirmar tratamiento de research interno antes de extraer algo a open-dev.

## Gate

ActionGate: `REVIEW`.

La preparacion local puede continuar por target. Cualquier cambio de licencia,
publicacion, venta, checkout o repo publico requiere revision explicita y
evidencia actual del target.
