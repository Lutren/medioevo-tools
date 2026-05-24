# FlujoCRM License Patch Options - 2026-05-07

Estado: `APPLIED_TO_STAGING / MIT_RECORDED`

Este paquete conserva los diffs revisables. La opcion MIT ya fue aplicada al
staging. No se cambio el producto activo y no se creo un repo remoto.

## Current Gate

- Host: `JAMMING/BLOCK`, `R=0.558`, `Phi_eff=0.435`.
- `pending_review`: `active_dedup=0`, `claudio_open=0`.
- Staging: `publish_staging\github\flujocrm-free-review`, commit `a16c019`,
  limpio, sin remoto.
- License readiness actual: `publication_ready=true`.

## Recommended Option

La recomendacion tecnica sigue siendo `MIT` o `Apache-2.0` para cumplir "CRM
gratis en GitHub" con confianza publica, y mantener Gumroad/Sponsors para
soporte, plantillas, instaladores y servicios.

Decision registrada: `MIT siempre`.

## Option A - MIT

Cambios esperados solo en `publish_staging\github\flujocrm-free-review`:

```diff
diff --git a/package.json b/package.json
@@
-  "license": "UNLICENSED",
-  "private": true,
+  "license": "MIT",
+  "private": false,
@@
-    "copyright": "Copyright 2026 L.R. Gonzalez. All rights reserved.",
+    "copyright": "Copyright 2026 L.R. Gonzalez.",
```

```diff
diff --git a/package-lock.json b/package-lock.json
@@
-      "license": "UNLICENSED",
+      "license": "MIT",
```

```diff
diff --git a/THIRD_PARTY_NOTICES.md b/THIRD_PARTY_NOTICES.md
@@
-FlujoCRM is a proprietary commercial app. It depends on npm packages listed in
-`package-lock.json`.
+FlujoCRM is released under the MIT License in this public source lane. It
+depends on npm packages listed in `package-lock.json`.
```

```diff
diff --git a/README.md b/README.md
@@
-Proprietary. Copyright L.R. Gonzalez. All rights reserved.
+MIT License. Copyright L.R. Gonzalez.
```

Nuevo `LICENSE`:

```text
MIT License

Copyright (c) 2026 L.R. Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Option B - Apache-2.0

Cambios esperados solo en `publish_staging\github\flujocrm-free-review`:

```diff
diff --git a/package.json b/package.json
@@
-  "license": "UNLICENSED",
-  "private": true,
+  "license": "Apache-2.0",
+  "private": false,
@@
-    "copyright": "Copyright 2026 L.R. Gonzalez. All rights reserved.",
+    "copyright": "Copyright 2026 L.R. Gonzalez.",
```

```diff
diff --git a/package-lock.json b/package-lock.json
@@
-      "license": "UNLICENSED",
+      "license": "Apache-2.0",
```

```diff
diff --git a/THIRD_PARTY_NOTICES.md b/THIRD_PARTY_NOTICES.md
@@
-FlujoCRM is a proprietary commercial app. It depends on npm packages listed in
-`package-lock.json`.
+FlujoCRM is released under the Apache License 2.0 in this public source lane.
+It depends on npm packages listed in `package-lock.json`.
```

Nuevo `LICENSE`:

```text
Apache License
Version 2.0, January 2004
https://www.apache.org/licenses/

Use the canonical Apache-2.0 text from the SPDX/Open Source Initiative source
before applying this option.
```

## Required Validation After Applying One Option

```powershell
cd publish_staging\github\flujocrm-free-review
npm run check
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json
python tools\release\audit_flujocrm_free_license_readiness.py --write --json
git -C publish_staging\github\flujocrm-free-review diff --check
git -C publish_staging\github\flujocrm-free-review status --short
```

Expected result after a correct license transition:

- `publication_ready=true`
- secret scan `count_reported=0`
- `npm run check` passed
- staging has no unexpected files
- ActionGate still required before any external publication

## Boundaries

- Do not change `apps\commercial\flujocrm` in this step.
- Do not change `COMMERCIAL_LICENSE.md` in the active commercial tree.
- Do not run `gh repo create` or `git push`.
- Do not deploy website copy.
- Do not announce LinkedIn/Gumroad/social until the repo exists and is verified.
