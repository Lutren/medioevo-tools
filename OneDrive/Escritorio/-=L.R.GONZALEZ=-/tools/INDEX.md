# tools INDEX

## Proposito

Herramientas locales de auditoria, release, migracion y soporte Codex.

## Reglas

- Ejecutar herramientas en modo local y no destructivo por defecto.
- No instalar dependencias nuevas con red sin ficha y review.
- No publicar vendors, caches, builds ni herramientas ofensivas sin revision
  especifica.

## Comandos Seguros Frecuentes

```powershell
python tools\release\pending_review.py --write --quiet
python tools\release\scan_secrets.py --json
```
