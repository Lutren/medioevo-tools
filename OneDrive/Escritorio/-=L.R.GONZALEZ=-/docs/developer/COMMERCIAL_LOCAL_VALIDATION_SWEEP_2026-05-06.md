# Commercial Local Validation Sweep - 2026-05-06

Estado: `LOCAL_VALIDATION_ONLY / NO_PUBLICATION`

Este barrido valida el carril comercial solo en local. No se publico, no se
hizo push, no se hizo deploy, no se genero instalador, no se cambio licencia,
no se abrio checkout y no se tocaron secretos.

## Gate

| item | valor |
|---|---|
| host gate inicial | `MIXTO/REVIEW` |
| accion permitida | `verify` |
| `R` | `0.431` |
| `Phi_eff` | `0.563` |
| `lambda_sat` | `0.805` |
| dominante | `r_io` |

Lectura: se permiten checks ligeros locales. No se permite publicacion externa,
build comercial final, instaladores, firmas, cambios de licencia ni checkout.

## Manifest Y Secret Scan

| target | class | files | blocked | excluded | secret scan |
|---|---|---:|---:|---:|---:|
| `argus-desktop` | `COMMERCIAL_OR_INTERNAL` | 52 | 0 | 0 | 0 |
| `asistente-negocio` | `COMMERCIAL` | 37 | 0 | 223 | 0 |
| `flujocrm` | `COMMERCIAL` | 20 | 0 | 244 | 0 |
| `mini-office` | `COMMERCIAL` | 53 | 0 | 12 | 0 |

## Checks Ejecutados

| target | comando | resultado |
|---|---|---|
| `mini-office` | `python -m pytest tests -q` | `22 passed in 0.13s` |
| `asistente-negocio` | `npm run check` | `public_safe check passed` |
| `flujocrm` | `npm run check` | main/preload/renderer smoke passed |
| `argus-desktop` | `npm run typecheck` | `ENV_MISSING`: `tsc` no reconocido |

## Lectura Por Producto

- `mini-office`: check local OK; venta sigue bloqueada por legal, clean-machine,
  soporte/privacidad/reembolso y checkout.
- `asistente-negocio`: public-safe check OK; venta amplia sigue bloqueada por
  legal, clean-machine y decision de firma/unsigned.
- `flujocrm`: smoke local OK; primera direccion sigue Windows-first standalone.
  No abrir GitHub/free release ni checkout sin decision de licencia,
  clean-install proof y legal/support.
- `argus-desktop`: manifest y scan OK, pero el typecheck actual no corre porque
  el entorno local no expone `tsc`. No instalar dependencias en este ciclo.

## Gate De Cierre

ActionGate comercial: `REVIEW`.

Permite:

- documentar evidencia local;
- repetir checks cuando el host este estable;
- preparar paquetes de revision.

Bloquea:

- venta amplia;
- Gumroad/checkout;
- build final de instaladores;
- firma/unsigned decision;
- cambio de licencia;
- publicacion externa;
- instalacion de dependencias con red sin revision.
