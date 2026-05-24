# SECRET_SCAN_REPORT

Fecha: 2026-05-06
Raiz: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

## Resultado Actual

Estado global: `NO APTO PARA PUBLICACION DIRECTA`.

Comando ejecutado:

```powershell
python tools\release\scan_secrets.py --json --limit 500
```

Resultado resumido:

- `count_reported=223`
- `truncated_at=500`
- `default_workspace_scan=True`

El scanner declara que no imprime valores de secretos; este reporte tampoco
copia valores, tokens ni contenido sensible.

## Fuente Canonica

El reporte historico detallado esta en:

- `docs/security/SECRET_SCAN_REPORT.md`
- `docs/security/GLOBAL_SENSITIVE_SCAN_TRIAGE_2026-05-06.md`

Este wrapper existe porque el prompt maestro exige `SECRET_SCAN_REPORT.md` en
la raiz. La politica sigue siendo:

- no publicar el workspace completo;
- no comprimir por glob amplio;
- usar allowlist por producto;
- excluir `.env`, tokens, credenciales, sesiones locales, vendors, privados,
  TCG/juego y releases generados;
- repetir scan focalizado antes de cualquier paquete, push, deploy o release.

## Decision

El scan global bloquea cualquier accion externa nueva. Los productos ya
publicados o verificados conservan solo su evidencia especifica; no autorizan
targets nuevos.
