# Paid Templates Local Integrity Sweep - 2026-05-06

Estado: `LOCAL_INTEGRITY_ONLY / NO_GUMROAD_ACTION`

Este barrido revisa solo integridad local de paquetes pagos ya definidos. No se
abrio Gumroad, no se cambio listing, no se genero ZIP nuevo, no se subio nada y
no se ejecuto accion externa.

## Targets

| target | lane | files | blocked | excluded | secret scan |
|---|---|---:|---:|---:|---:|
| `medioevo-agent-ops-pack` | `paid-templates` | 10 | 0 | 0 | 0 |
| `duat-templates` | `paid-templates` | 8 | 0 | 0 | 0 |

## Comandos

```powershell
python tools\release\product_manifest.py --product medioevo-agent-ops-pack --hash
python tools\release\scan_secrets.py --product medioevo-agent-ops-pack --json
python tools\release\product_manifest.py --product duat-templates --hash
python tools\release\scan_secrets.py --product duat-templates --json
```

## Resultado

- Ambos targets tienen `blocked_count=0`.
- Ambos scans focalizados reportan `count_reported=0`.
- El resultado no autoriza venta nueva, cambios de precio, listing, deploy,
  redes, Gumroad ni release externo.

## Siguiente Gate

Para cualquier accion externa sobre paquetes pagos:

- ActionGate por target.
- Host no bloqueante.
- Verificacion de listing actual.
- Path/claims scan del artefacto exacto.
- Confirmacion post-accion con URL/API/screenshot no secreto.
