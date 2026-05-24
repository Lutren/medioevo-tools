# DESPERTAR_GUMROAD_MEDIOEVO_SPACE_PUBLICATION_REPORT_2026-05-14

## Estado

`READY_LOCAL_PUBLICATION_GATED_BY_ACTIONGATE_BLOCK`

## Lectura Humana

Aceptada por el operador en chat. Se habilito preparacion local de publicacion.

## Anti Texto IA

- Herramienta: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\08_QA_WITNESSLOG\anti_ai_text_review.py`
- Reporte: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\08_QA_WITNESSLOG\ANTI_AI_TEXT_REVIEW_20260513_232758\ANTI_AI_TEXT_REVIEW.md`
- Resultado: `PASS`
- Items: `DESPERTAR_SAMPLE`, `ONE_SENTENCE_PROMISE`, `BACK_COVER_DRAFT`, `CATEGORY_POSITIONING`
- Nota: heuristica editorial local; no es detector externo ni prueba absoluta.

## Gumroad

### Preparado localmente

- Producto: `MEDIOEVO: Despertar Preview`
- Listing: `PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES\despertar-preview-gumroad_20260513_232758\commerce\gumroad_listing.json`
- ZIP: `releases\books\MEDIOEVO_DESPERTAR_PREVIEW_20260513_232758.zip`
- ZIP SHA256: `5BC6F9F900D798FDAB945FC0C1C7E4957127F3C22085B8607080536F01650196`
- ZIP QA: `testzip=None`, executables `0`, nested_zips `0`
- Secret scan package/artifact: `count_reported=0`
- Curador preflight after ficha: `REGISTERED_CONTINUE_WITH_BOUNDARY`
- Release manifest: `release_manifests\medioevo-despertar-preview.json`
- Manifest QA: `blocked_count=0`
- Path scrub: `ok=true`
- Claims scan: `ok=true`
- Dry-run ActionGate: `gumroad:dmqgzi` => `pass`
- Real publish ActionGate: `blocked`, decision `6f2ab2e7-8b8d-4607-aa21-e0d0196b55be`

### No ejecutado

No se llamo Gumroad API, no se subio archivo y no se publico/actualizo producto. El script de publicacion detuvo la ejecucion antes de leer token o tocar API porque ActionGate devolvio `JAMMING/BLOCK`.

## medioevo.space

### Live source correction

After the first staging pass, current live HTML showed that `medioevo.space` is serving the DUAT public app, not the separate static `publish_staging\medioevo-site` tree. The real source updated in the continuation pass is:

`publish_staging\medioevo-duat-public-release`

Additional staging changes:

- Added `/despertar-preview` SPA route.
- Added `/despertar-preview.html` normalization.
- Added DESPERTAR to `src\content\gumroadProducts.ts`, `src\content\products.ts`, `src\content\books.ts`.
- Added `src\content\despertarStore.test.ts`.
- Updated `public\sitemap.xml` and `public\llms.txt`.
- Added crawlable static pages: `public\store.html`, `public\despertar-preview.html`, `public\gumroad.html`, `public\books.html`.
- Report: `publish_staging\medioevo-duat-public-release\qa\DESPERTAR_STORE_STAGING_REPORT_2026-05-14.md`.

Additional QA:

- `npm test`: `5 passed`, `32 passed`.
- `npm run build`: PASS.
- `npm audit --audit-level=moderate`: `0 vulnerabilities`.
- Focused source/public secret scans: `count_reported=0`.
- Focused `dist` secret scan: `count_reported=0`.
- SEO audit on built `dist`: no major findings; `robots.txt`, `sitemap.xml` and `llms.txt` present.
- Local preview routes `/`, `/store`, `/gumroad`, `/books`, `/despertar-preview`, `/despertar-preview.html`, `/sitemap.xml`, `/llms.txt`: HTTP `200`.
- Local static preview routes `/store.html`, `/despertar-preview.html`, `/gumroad.html`, `/books.html`, `/sitemap.xml`, `/llms.txt`: HTTP `200`.
- Website deploy dry-run ActionGate: `cloudflare-pages:medioevo-site` => `pass`.
- Website deploy real ActionGate: `blocked`, decision `8bc78e64-33e8-471b-9760-b1ba1cffcdc4`.

Additional live finding:

- `https://medioevo.space/sitemap.xml` currently returns the app HTML fallback, not XML `urlset`.
- `https://medioevo.space/despertar-preview` currently returns the previous deployed app shell and does not yet show `Despertar Preview`.
- Deploy remains blocked by ActionGate because host state is `JAMMING/BLOCK`.

### Staging actualizado

Ruta: `publish_staging\medioevo-site`

Archivos:

- `despertar-preview.html`
- `index.html`
- `pricing.html`
- `linea-bestseller.html`
- `sitemap.xml`
- `store-integration.js`

Cambios:

- Agregada pagina `despertar-preview.html`.
- Tienda corregida a productos/rutas public-safe.
- Eliminadas compras directas de `Saga Completa`, `TCG` y badge `BESTSELLER` del catalogo dinamico.
- Agregado DESPERTAR Preview a home/pricing/sitemap.
- Copy actualizado: no claim bestseller real, no ciencia externa, no archivo privado completo como compra directa.

### QA local

- `node --check store-integration.js`: PASS
- Local HTTP server `127.0.0.1:8787`: `/`, `/despertar-preview.html`, `/pricing.html`, `/linea-bestseller.html`, `/sitemap.xml`, `/store-integration.js` => `200`
- Secret scan staged site files: `count_reported=0`

### Live check

- `https://medioevo.space/` => `200`
- `https://medioevo.space/pricing.html` => `200`
- `https://medioevo.space/sitemap.xml` => `200`
- `https://lrgonzalez.gumroad.com/l/dmqgzi` => `200`

La ruta nueva `/despertar-preview.html` esta en staging local, no en live, porque deploy externo quedo bloqueado por host gate.

## Host Gate

Comando:

`python tools\host_observacionista.py --no-write`

Resultado:

- status: `JAMMING`
- gate: `BLOCK`
- R: `0.698`
- Phi_eff: `0.353`
- memory_pct: `89.8`
- disk_pct: `95.5`
- reasons: `memoria_alta`, `disco_alto`, `residuo_alto`
- latest real Gumroad publish ActionGate: `blocked`
- latest real website deploy ActionGate: `blocked`

## Bloqueos

- Gumroad API create/update/upload/publish: `BLOCK` mientras host gate sea `BLOCK`; owner override no aplica en `JAMMING/BLOCK`.
- Cloudflare/Wrangler deploy: `BLOCK` mientras host gate sea `BLOCK`.
- Push GitHub: `BLOCK` mientras host gate sea `BLOCK`.
- Claim "bestseller real": `BLOCK` hasta evidencia de mercado.

## Reentrada cuando host gate no sea BLOCK

1. Repetir host gate desde Claudio:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio"
python tools\host_observacionista.py --no-write
```

2. Si no devuelve `BLOCK`, ejecutar ActionGate especifico para Gumroad y Cloudflare.

3. Gumroad target:

```powershell
C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES\despertar-preview-gumroad_20260513_232758\commerce\gumroad_listing.json
```

4. Deploy target:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\publish_staging\medioevo-duat-public-release"
npm test
npm run build
npx wrangler pages deploy dist --project-name=medioevo-site --branch=main
```

No ejecutar esos pasos si host gate sigue `BLOCK`.
