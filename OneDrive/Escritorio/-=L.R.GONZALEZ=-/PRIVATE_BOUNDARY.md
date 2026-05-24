# PRIVATE_BOUNDARY

Fecha: 2026-05-06
Estado: frontera activa, no publicar, no mover.

## Regla

El juego, TCG, lore privado, assets privados, bridges internos, builds del
juego y material editorial completo no entran en releases tecnicos, repos open,
Gumroad tecnico ni paquetes gratuitos.

## Rutas Privadas

- `game-private\**`
- `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg\**`
- `-=MEDIOEVO=-\-=LIBROS\claudio\tcg\**`
- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\game_bridge\**`
- `PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG\**` hasta revision manual
- libros completos, vaults editoriales y canon privado no aprobado

## Fuente Canonica

- `docs/private/PRIVATE_GAME_BOUNDARY.md`
- `VISIBILITY_MATRIX.md`
- `PRODUCT_MAP.md`
- `RISK_REGISTER.md`

## ActionGate

Clasificacion por defecto:

- leer nombres/rutas para auditoria: `APPROVE`
- copiar contenido privado a open/comercial: `BLOCK`
- publicar o empaquetar privado: `BLOCK`
- mover o borrar privado: `REVIEW` o `BLOCK`, segun alcance y evidencia

## Decision

Este ciclo no toca rutas privadas. La frontera queda reafirmada para agentes
posteriores.
