# Paid Apps - Paquetes Fuente Locales

Fecha: 2026-05-01

Decision: `REVIEW comercial local`. Se generaron ZIPs fuente privados por allowlist para las apps comerciales. Son artefactos internos de QA, no entregables cliente por defecto. No se subieron a Gumroad, no se publicaron en website y no sustituyen QA/legal.

## Comandos

| Comando | Resultado |
|---|---|
| `python tools\release\package_paid_apps.py --execute` | 4 ZIPs escritos en `releases\paid-apps` |
| `python tools\release\package_paid_apps.py --product flujocrm --execute` | `flujocrm.zip` regenerado tras README/listing QA |
| `python tools\release\scan_secrets.py --artifact releases\paid-apps\argus-desktop.zip --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --artifact releases\paid-apps\asistente-negocio.zip --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --artifact releases\paid-apps\flujocrm.zip --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --artifact releases\paid-apps\mini-office.zip --json --fail-on-findings` | `count_reported=0` |

## Artefactos

| ZIP | bytes | sha256 | scan |
|---|---:|---|---|
| `releases\paid-apps\argus-desktop.zip` | 7006395 | `b8b8bf292e4d72267a6c3a6683cf759e5b60f514e4c710f5880e5770f0c9bbfb` | 0 findings |
| `releases\paid-apps\asistente-negocio.zip` | 6780591 | `ce6a77299363ff66c7b33ef6542a0f1f3eeb1fea9955f00b0f91eacdfc41d4af` | 0 findings |
| `releases\paid-apps\flujocrm.zip` | 99795 | `f4c4be4aadfee141993047ad383fb263c6ead7b5fbb9dde7b6dca753e628e3c4` | 0 findings |
| `releases\paid-apps\mini-office.zip` | 81438 | `fe05d7997b7a4b8a8237a876fff6e4cdc970acddede750f1e7677dbb67d54ad8` | 0 findings |

## No Cerrado

- FlujoCRM ya tiene instalador Windows x64 QA local, pero no esta firmado ni probado en maquina limpia.
- No hay instaladores finales firmados para el lote completo.
- No se hizo prueba de instalacion en maquina limpia por app.
- Legal/support/privacy/refund/terms siguen pendientes.
- Gumroad/website/listings siguen bloqueados hasta checklist comercial y ActionGate.
