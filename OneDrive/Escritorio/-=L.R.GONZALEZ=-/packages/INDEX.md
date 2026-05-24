# packages INDEX

## Proposito

Paquetes tecnicos separados por allowlist.

## Reglas

- `packages/open-dev` puede ser public-safe solo por paquete verificado.
- `packages/paid` es comercial/propietario salvo decision explicita.
- Todo paquete requiere manifest, tests, scan de secretos y claims boundary
  antes de publicacion.

## No Incluir

- Rutas privadas.
- Runtime local.
- Sesiones.
- `.env` o credenciales.
- Vendors no revisados.
