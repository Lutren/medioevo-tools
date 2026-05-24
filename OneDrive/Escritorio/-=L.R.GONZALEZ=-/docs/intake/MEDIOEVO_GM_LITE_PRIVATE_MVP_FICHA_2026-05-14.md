# MEDIOEVO GM Lite Private MVP - Ficha

Fecha: 2026-05-14

## Fuente

- ZIP: `C:\Users\L-Tyr\Downloads\medioevo-gm-lite-private-mvp.zip`
- SHA256: `0421D51E6C1EB76E7F060A589169DC8E42E7B22336F63C5E38B79D74D0CEF57C`
- Tamano ZIP: `25705` bytes
- Entradas: `32`
- Total descomprimido observado: `50450` bytes

## Clasificacion

- Producto: `MEDIOEVO GM Lite`
- Capa: `PRIVATE_REPO_CANDIDATE`
- Publicacion publica: `BLOCK`
- Repo privado GitHub: `REVIEW`, pendiente de host gate `APPROVE` u override explicito para este ZIP.

## Evidencia local

- `python tools\release\curador_preflight.py --path C:\Users\L-Tyr\Downloads\medioevo-gm-lite-private-mvp.zip`
  - Resultado: `NEEDS_FICHA_BEFORE_USE`
- `tar -tf C:\Users\L-Tyr\Downloads\medioevo-gm-lite-private-mvp.zip`
  - Resultado: proyecto unico `medioevo_gm_lite`
- Escaneo focalizado del ZIP:
  - `findings_count=3` por menciones de seguridad en docs/scripts, no por valores impresos.
- Staging local:
  - `publish_staging\github-private\medioevo-gm-lite-private-mvp`
  - `git check-ignore`: cubierto por regla raiz `publish_staging/`
- `python tools\release\scan_secrets.py --path publish_staging\github-private\medioevo-gm-lite-private-mvp --json`
  - Resultado: `count_reported=0`
- `npm run lint:boundary`
  - Resultado: `Boundary check PASS`

## Revision requerida

- `npm install` y `npm run build` no se ejecutaron porque instalar dependencias con red queda en `REVIEW`; `package.json` usa dependencias `latest` y no hay lockfile.
- `gh repo create` / `git push` no se ejecutaron porque el host gate actual dio `CONTAMINADO/REVIEW` con `R=0.537`, `Phi_eff=0.449`, `lambda_sat=0.892`.
- Repos GitHub revisados:
  - `Lutren/medioevo-gm-lite`: `REPO_NOT_FOUND_OR_NO_ACCESS`
  - `Lutren/medioevo-gm-lite-private-mvp`: `REPO_NOT_FOUND_OR_NO_ACCESS`

## Proxima accion

Si el host gate vuelve a `APPROVE` o el operador emite override explicito para este ZIP privado, ejecutar desde:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\publish_staging\github-private\medioevo-gm-lite-private-mvp"
npm install
npm run build
npm run lint:boundary
git init
git add .
git commit -m "Initial private MVP: MEDIOEVO GM Lite"
gh repo create medioevo-gm-lite --private --source=. --remote=origin --push
gh repo view Lutren/medioevo-gm-lite --json name,visibility,url
```

## Actualizacion: cierre ejecutado

- Override explicito recibido: `si y verifica todos los pendientes y continua`.
- ActionGate shell command PASS: `e90290a9-b7d5-4d0a-8c39-2e6cf283cc83`.
- Repo privado creado: `https://github.com/Lutren/medioevo-gm-lite`.
- GitHub API: `private=true`, `visibility=private`, default branch `main`.
- Commit inicial: `ec755ca64ed3fb949ce5908036f0be01f3e51fd8`.
- Validacion final: `npm install`, `npm run build`, `npm audit --audit-level=moderate`, `npm run lint:boundary`, secret scan focalizado `count_reported=0`.
- Publicacion publica/deploy: `NO_EJECUTADO`.
