# PUSH_AUDIT_2026-05-15

Fecha: 2026-05-15

Alcance: auditoria de repos Git bajo `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` despues del despliegue de blog/prompts en `medioevo.space`.

## Resumen

- `publish_staging\medioevo-duat-public-release`: publicado, desplegado y verificado en vivo.
- `publish_staging\github-profile-lutren-2026-05-01`: empujado a GitHub profile `Lutren`.
- `publish_staging\hackathons\google-rapid-agent-2026-public-safe`: no habia push pendiente; estaba 1 commit detras del remoto y se actualizo por fast-forward.
- `-=MEDIOEVO=-\-=LIBROS\claudio\publish_staging\github\claudio-system-regulator-2026-05-02`: no habia push pendiente; estaba 1 commit detras del remoto y se actualizo por fast-forward.
- No queda ningun repo public-safe limpio con `ahead > 0` detectado en esta pasada.

## Acciones Ejecutadas

### MEDIOEVO DUAT public release

- Ruta: `publish_staging\medioevo-duat-public-release`
- Remoto: `https://github.com/Lutren/medioevo-duat-public-release.git`
- Commits empujados:
  - `06a864d` `feat: publish prompt campaign and handoff surfaces`
  - `dca3c79` `fix: remove clean-url redirect loop`
  - `5bddd1a` `docs: record prompt campaign deploy evidence`
- Ramas actualizadas:
  - `origin/public-identity-ai-discovery`
  - `origin/main`
- Deploy:
  - `npx wrangler pages deploy dist --project-name=medioevo-site --branch=main`
  - Deployment URL: `https://83605973.medioevo-site.pages.dev`
- Verificacion viva:
  - `https://medioevo.space/blog`: HTTP 200, contiene `Los 3 prompts`, `ahorro de tokens`, `Handoff`.
  - `https://medioevo.space/blog/prompts-definitivos`: HTTP 200, contiene `Scanner de seguridad local`.
  - `https://medioevo.space/prompts`: HTTP 200.
  - `https://medioevo.space/prompts/01_scanner_seguridad_local.md`: HTTP 200.
  - `https://medioevo.space/sitemap.xml`: contiene `/blog/prompts-definitivos` y `/prompts`.

### GitHub profile Lutren

- Ruta: `publish_staging\github-profile-lutren-2026-05-01`
- Remoto: `https://github.com/Lutren/Lutren.git`
- Commit empujado: `3a95b41` `Align public MEDIOEVO identity and AI discovery surfaces`
- Ramas actualizadas:
  - `origin/public-identity-ai-discovery`
  - `origin/main`
- Gates:
  - `scan_secrets.py --path publish_staging\github-profile-lutren-2026-05-01 --json --fail-on-findings`: `count_reported=0`
  - `git diff --check origin/main...HEAD`: PASS
  - busqueda focalizada de secretos/rutas privadas: sin coincidencias bloqueantes

### Fast-forward local de repos ya publicados

- `publish_staging\hackathons\google-rapid-agent-2026-public-safe`
  - Antes: local detras de `origin/main` por 1 commit.
  - Accion: `git pull --ff-only`
  - Nuevo HEAD: `67586fd` `Add sponsor goal and tiers to hackathon README`
  - Tests: `python -m pytest -q` -> `4 passed`
  - Secret scan focalizado: `count_reported=0`
- `-=MEDIOEVO=-\-=LIBROS\claudio\publish_staging\github\claudio-system-regulator-2026-05-02`
  - Antes: local detras de `origin/main` por 1 commit.
  - Accion: `git pull --ff-only`
  - Nuevo HEAD: `ef08251` `Strengthen GitHub positioning copy`
  - Tests: `python -m pytest -q` -> `2 passed`
  - Secret scan focalizado: `count_reported=0`

## Repos Sin Accion De Push

### Bloqueados por mezcla, secretos o frontera privada

- `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`
  - Rama: `codex/curador-seto-loops-2026-05-05`
  - Remoto: ninguno detectado
  - Estado: sucio, 497 cambios al cierre de la pasada anterior; no publicable por workspace global.
- `-=MEDIOEVO=-\-=LIBROS`
  - Rama: `imagenes`
  - Remoto: ninguno detectado
  - Estado: `1796` cambios locales en auditoria Git; mezcla canon, website, Claudio y privados.
- `-=MEDIOEVO=-\-=LIBROS\claudio`
  - Remoto: `https://github.com/Lutren/claudio-fixes.git`
  - Estado: `961` cambios locales y `0 12` frente a `origin/fix/claudio-cli-latency`; no se empuja desde arbol sucio.
- `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg`
  - Clasificacion: `PRIVATE_BLOCK`
  - Estado: 123 cambios locales; no publicar ni empujar por esta lane.
- `publish_staging\medioevo-site`
  - Estado: 5 modificados y 1 no trackeado (`despertar-preview.html`)
  - Bloqueo: `scan_secrets.py --path publish_staging\medioevo-site --json --fail-on-findings` reporto `count_reported=6`.
  - Hallazgos: `medioevo-auth.js`, `stripe-store.js`, `functions/api/create-checkout.js`, mapas con `secreto` en nombre y `netlify/functions/create-checkout.js`.
  - Frontera: todavia contiene referencias RPG/TCG y legacy checkout; no cumple gate de publicacion limpia.

### Sin remoto o repos de revision

- `publish_staging\github\flujocrm-free-review`: limpio, sin remoto configurado; no hay destino de push.
- `-=MEDIOEVO=-\-=LIBROS\claudio\mini_office`: sin remoto, 37 modificados; no publicable por esta lane.
- `-=MEDIOEVO=-\-=LIBROS\llm-wiki`: fork/upstream externo `karpathy/llm.c`, 56 cambios locales; no empujar.

### Vendor o terceros

- `tools\claw-code`: vendor, 1 no trackeado; no empujar.
- `-=MEDIOEVO=-\-=LIBROS\claudio\core\sadtalker`: vendor, sucio; no empujar.
- `-=MEDIOEVO=-\-=LIBROS\claudio\core\wav2lip`: vendor, sucio; no empujar.
- `-=MEDIOEVO=-\-=LIBROS\claudio\github-modules\open-higgsfield-ai`: vendor, limpio; no empujar.

## Estado Final De Repos Public-Safe Revisados

- `publish_staging\medioevo-duat-public-release`: `0 0`, limpio, HEAD `5bddd1a`.
- `publish_staging\github-profile-lutren-2026-05-01`: `0 0`, limpio, HEAD `3a95b41`.
- `publish_staging\hackathons\google-rapid-agent-2026-public-safe`: `0 0`, limpio, HEAD `67586fd`.
- `-=MEDIOEVO=-\-=LIBROS\claudio\publish_staging\github\claudio-system-regulator-2026-05-02`: `0 0`, limpio, HEAD `ef08251`.
- `publish_staging\open-dev\*` y `publish_staging\github-public-sanitized\*`: auditados despues de fetch; `0 0` y limpios en esta pasada.

## Proxima Accion Verificable

Resolver `publish_staging\medioevo-site` solo si se decide que ese repo sigue siendo fuente activa. El paso minimo seguro es aislar los cambios de DESPERTAR en una rama/commit con allowlist de archivos tocados, remover o documentar la frontera RPG/TCG, y lograr `scan_secrets` focalizado sin hallazgos antes de cualquier push.
