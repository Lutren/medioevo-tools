# FlujoCRM Free GitHub Staging - 2026-05-06

Estado: `MIT_STAGING_READY / EXTERNAL_BLOCKED`

El operador pidio dar el CRM gratis en GitHub y luego definio `MIT siempre`.
Se preparo un staging local seguro y se aplico MIT solo al staging. No se
ejecuto push ni se cambio la licencia del producto comercial activo.

## Staging

- Ruta: `publish_staging\github\flujocrm-free-review`
- Fuente: `apps\commercial\flujocrm`
- Commit inicial: `dbead56 Initial FlujoCRM free GitHub review staging`
- Commit MIT: `a16c019 Apply MIT license to FlujoCRM free staging`
- Archivos visibles fuera de `.git`: `20`
- Tamano visible: `282882` bytes
- Publicacion permitida: `false`

## Incluido

- Fuente Electron principal: `main.js`, `preload.js`, `index.html`,
  `mockup.html`.
- `package.json` y `package-lock.json` originales para trazabilidad.
- Smoke tests de main/preload/renderer.
- Docs comerciales existentes solo como evidencia de estado actual.
- Docs nuevos de staging:
  - `PUBLICATION_GATE.md`
  - `README_PUBLIC_DRAFT.md`
  - `LICENSE_DECISION_REQUIRED.md`
  - `SOURCE_ALLOWLIST_MANIFEST.json`

## Excluido

- `dist`
- `node_modules`
- installers
- runtime databases
- `.env`
- secrets/tokens/credentials
- Gumroad/Stripe/account state
- private game/TCG, book vaults or Claudio runtime

## Validacion

Comandos ejecutados:

```powershell
python -m py_compile tools\release\stage_flujocrm_free_candidate.py
python tools\release\stage_flujocrm_free_candidate.py --verify-existing --write --json
python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json
python tools\release\scan_secrets.py --artifact tools\release\stage_flujocrm_free_candidate.py --json
node --check main.js
node --check preload.js
node scripts\smoke-main.cjs
node scripts\smoke-preload.cjs
node scripts\smoke-renderer.cjs
python -m json.tool publish_staging\github\flujocrm-free-review\package.json
python -m json.tool publish_staging\github\flujocrm-free-review\SOURCE_ALLOWLIST_MANIFEST.json
python -m json.tool qa_artifacts\release_validation\flujocrm-free-github-review-staging-2026-05-06.json
rg -n "C:\\|C:/|Users\\|OneDrive|-=L\.R|L-Tyr|Escritorio" publish_staging\github\flujocrm-free-review --glob "!.git/**"
git -C publish_staging\github\flujocrm-free-review log --oneline -1
git -C publish_staging\github\flujocrm-free-review status --short
```

Resultados:

- Staging tool: `ok=true`.
- Git staging repo: limpio; `status --short` sin salida.
- Secret scan staging: `count_reported=0`.
- Secret scan del script via `--artifact`: `count_reported=0`. El modo
  `--path` sobre `tools\release` reporta `denylist path` por diseno del
  scanner, no por contenido secreto.
- Local-path scrub: sin rutas locales (`rg` retorno `1`, sin coincidencias).
- Smoke main: `flujocrm main smoke passed`.
- Smoke preload: `flujocrm preload smoke passed`.
- Smoke renderer: `flujocrm renderer smoke passed`.
- JSON package/manifest/report: validos.
- License readiness posterior: `publication_ready=true`.
- Bloqueos de licencia: ninguno.

## Bloqueos Restantes

- Host/ActionGate: `JAMMING/BLOCK`.
- Publicacion externa: no hacer push hasta que `github-flujocrm-free-release`
  pase ActionGate.

## Proxima Accion

Cuando el host no este en `BLOCK`, reintentar ActionGate y generar el repo
remoto solo desde `publish_staging\github\flujocrm-free-review`.
