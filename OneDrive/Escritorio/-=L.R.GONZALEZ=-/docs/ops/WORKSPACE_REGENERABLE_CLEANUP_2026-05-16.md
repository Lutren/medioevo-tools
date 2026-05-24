# WORKSPACE_REGENERABLE_CLEANUP 2026-05-16

## Alcance

Raiz: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

Limpieza ejecutada solo sobre residuos regenerables:

- `__pycache__`
- `.pytest_cache`
- `.ruff_cache`
- `.mypy_cache`
- caches de pruebas locales allowlisted por `tools/release/cleanup_regenerable_cache.py`
- `apps/local/wabi-sabi/wabi_sabi_local_agents.egg-info`, ignorado por `.gitignore` y regenerable

No se hizo push, deploy, publicacion, empaquetado publico ni movimiento de rutas privadas.

## Gates

ActionGate: `APPROVE` para caches regenerables dentro del workspace y metadatos `*.egg-info` ignorados.

ActionGate: `BLOCK/NO_TOCADO` para:

- rutas privadas TCG/juego
- secretos, `.env`, credenciales o sesiones
- repos Git, vendors, releases, builds comerciales, `node_modules` y entornos
- logs/evidencia runtime que no sea cache
- movimientos o borrados ambiguos

## Evidencia

```powershell
python tools\release\pending_review.py --write --quiet
```

Resultado: `active_dedup=18`, `claudio_open=0`. Artefactos:

- `qa_artifacts/pending/pending_review_2026-05-16.json`
- `qa_artifacts/pending/pending_review_latest.json`
- `docs/pending/PENDING_REVIEW_2026-05-16.md`
- `docs/pending/PENDING_REVIEW_LATEST.md`

```powershell
python tools\release\cleanup_regenerable_cache.py --json-out qa_artifacts\release_validation\seto-cache-cleanup-dry-run-2026-05-16.json
```

Resultado dry-run: `approved=55`, `blocked=0`, `approved_files=349`,
`approved_bytes=4546849`, `errors=0`.

```powershell
python tools\release\cleanup_regenerable_cache.py --execute --json-out qa_artifacts\release_validation\seto-cache-cleanup-result-2026-05-16.json
```

Resultado ejecutado: `deleted=55`, `deleted_files=349`,
`deleted_bytes=4546849`, `errors=0`.

Retiro manual verificado con PowerShell nativo:

- `tools\release\__pycache__`: 1 archivo, 15553 bytes.
- `apps\local\wabi-sabi\wabi_sabi_local_agents.egg-info`: 5 archivos, 2194 bytes.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -B tools\release\cleanup_regenerable_cache.py --json-out qa_artifacts\release_validation\seto-cache-cleanup-final-posttest-2026-05-16.json
```

Resultado final post-test: `approved=0`, `blocked=0`, `bytes=0`,
`errors=0`.

## Verificacion Wabi-Sabi

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -B -m pytest -q -p no:cacheprovider
```

Resultado: `209 passed in 72.40s`.

Verificacion local de residuos Wabi-Sabi: sin `__pycache__`, `.pytest_cache`,
`.mypy_cache`, `.ruff_cache` ni `*.egg-info`.

## Decision

El workspace queda limpio de los caches regenerables aprobados por el limpiador
seguro. El arbol sigue siendo un workspace grande y sucio por cambios reales,
docs, runtime, staging y trabajo no relacionado; eso no debe tratarse como
basura sin ficha, migration map y ActionGate especifico.

## Proxima accion verificable

Elegir un carril concreto del arbol sucio y producir ficha/migration map antes
de mover, archivar o borrar cualquier elemento no regenerable.
